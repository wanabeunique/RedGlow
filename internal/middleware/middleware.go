package middleware

import "net/http"

type Middleware interface{
	GetMiddlewareFunc() func(http.Handler) http.Handler
}