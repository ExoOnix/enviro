package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
	"os"
)

var prefix string

func init() {
	envID := os.Getenv("ENV_ID")
	if envID == "" {
		log.Println("ENV_ID not set, using default prefix")
		envID = "default"
	}
	prefix = "env-" + envID + "-"
}


func extractPortFromHost(host string) (string, bool) {
	host = strings.Split(host, ":")[0]
	parts := strings.Split(host, ".")
	if len(parts) < 1 {
		return "", false
	}
	subdomain := parts[0]
	if !strings.HasPrefix(subdomain, prefix) {
		return "", false
	}
	port := strings.TrimPrefix(subdomain, prefix)
	return port, true
}

func proxyHandler(w http.ResponseWriter, r *http.Request) {
	port, ok := extractPortFromHost(r.Host)
	if !ok {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	}

	target, err := url.Parse("http://localhost:" + port)
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
