package main

import (
	"flag"
	"net/http"
	"time"
)

// Usage: go run delay_server.go -addr localhost:8080 -delay 10ms

func main() {
	addr := flag.String("addr", ":8080", "listen address")
	delay := flag.Duration("delay", 0, "response delay (e.g. 50ms, 200ms)")
	flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if *delay > 0 {
			time.Sleep(*delay)
		}
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok"))
	})

	_ = http.ListenAndServe(*addr, nil)
}
