package auth

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"redGlow/internal/service"
)

type signUpHandler struct{
	service service.AuthService
}

func NewSignUp(service service.AuthService) *signUpHandler{
	return &signUpHandler{
		service: service,
	}
}

func (*signUpHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  if _, err := io.Copy(w, r.Body); err != nil {
    fmt.Fprintln(os.Stderr, "Failed to handle request:", err)
  }
}

func (*signUpHandler) Pattern() string {
  return "/users/"
}

func (*signUpHandler) HTTPMethod() string {
	return "GET"
}