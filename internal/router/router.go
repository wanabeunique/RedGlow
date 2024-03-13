package router

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

func NewChiRouter(routes []Route, middlewares ...func(http.Handler) http.Handler) chi.Router {
	router := chi.NewRouter()
	for _, route := range routes{
		router.Handle(route.Pattern(), route)
	}

	// for _, middleware := range middlewares{
	// 	router.Use(middleware)
	// }
	return router
}