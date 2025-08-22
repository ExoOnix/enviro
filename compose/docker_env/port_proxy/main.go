package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
)

const prefix = "app-"

func extractPortFromHost(host string) (string, bool) {
	// Remove port if present (e.g., app-8080.test:80)
	host = strings.Split(host, ":")[0]
	parts := strings.Split(host, ".")
	if len(parts) < 2 {
		return "", false
	}
	if !strings.HasPrefix(parts[0], prefix) {
		return "", false
	}
	port := strings.TrimPrefix(parts[0], prefix)
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
	http.HandleFunc("/", proxyHandler)
	log.Println("Reverse proxy listening on :80")
	log.Fatal(http.ListenAndServe(":80", nil))
}
