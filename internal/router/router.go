package router

import (
	"redGlow/internal/handler"
	"redGlow/internal/middleware"

	"github.com/go-chi/chi/v5"
)

func NewChiRouter(handlers []handler.Handler, middlewares []middleware.Middleware) chi.Router {
	router := chi.NewRouter()
	for _, middleware := range middlewares{
		router.Use(middleware.GetMiddlewareFunc())
	}
	
	for _, handler := range handlers{
		router.Method(handler.HTTPMethod(),handler.Pattern(),handler)
	}
	
	return router
}