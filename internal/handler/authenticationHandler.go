package handler

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

type authenticationHandler struct{}

func NewAuthenticationHandler() *authenticationHandler{
	return &authenticationHandler{}
}

func (*authenticationHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  if _, err := io.Copy(w, r.Body); err != nil {
    fmt.Fprintln(os.Stderr, "Failed to handle request:", err)
  }
}

func (*authenticationHandler) Pattern() string {
  return "/echo"
}