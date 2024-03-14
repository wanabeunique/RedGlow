package handler

import (
	"net/http"
)

type Handler interface {
  http.Handler
  Pattern() string
  HTTPMethod() string
}