package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strconv"
	"strings"
)

var prefix string

// Reserved ports that must never be proxied
var reservedPorts = map[int]struct{}{
	23000: {}, // code-server
	23001: {}, // port_proxy
	2375:  {}, // Docker API
	2376:  {}, // Docker API TLS
	2377:  {}, // Docker Swarm manager
	7946:  {}, // Docker Swarm overlay
	4789:  {}, // Docker VXLAN
	6443:  {}, // Kubernetes API
	10250: {}, // kubelet
	10251: {}, // kube-scheduler
	10252: {}, // kube-controller-manager
	10255: {}, // kubelet read-only
	2379:  {}, // etcd client
	2380:  {}, // etcd peer
}

// check if a port is blacklisted
func isBlacklisted(port int) bool {
	// Block reserved ports
	if _, found := reservedPorts[port]; found {
		return true
	}

	// Optionally block privileged ports (0–1024)
	if port <= 1024 && port != 80 {
		return true
	}

	return false
}

func init() {
	envID := os.Getenv("ENV_ID")
	if envID == "" {
		log.Println("ENV_ID not set, using default prefix")
		envID = "default"
	}
	prefix = "env-" + envID + "-"
}

func extractPortFromHost(host string) (int, bool) {
	host = strings.Split(host, ":")[0]
	parts := strings.Split(host, ".")
	if len(parts) < 1 {
		return 0, false
	}
	subdomain := parts[0]
	if !strings.HasPrefix(subdomain, prefix) {
		return 0, false
	}
	portStr := strings.TrimPrefix(subdomain, prefix)
	port, err := strconv.Atoi(portStr)
	if err != nil {
		return 0, false
	}
	return port, true
}

func proxyHandler(w http.ResponseWriter, r *http.Request) {
	port, ok := extractPortFromHost(r.Host)
	if !ok {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	}

	// Check blacklist
	if isBlacklisted(port) {
		http.Error(w, "Forbidden, this port is blacklisted for security reasons.", http.StatusForbidden)
		log.Printf("Blocked request to blacklisted port: %d", port)
		return
	}

	target, err := url.Parse("http://localhost:" + strconv.Itoa(port))
	if err != nil {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	}

	proxy := httputil.NewSingleHostReverseProxy(target)
	proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, e error) {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
	}
	proxy.ServeHTTP(w, r)
}

func main() {
	log.Printf("Reverse proxy listening on :23001, prefix set: %s", prefix)
	http.HandleFunc("/", proxyHandler)
	log.Fatal(http.ListenAndServe(":23001", nil))
}
