package httpserver

import (
	"context"
	"net/http"
	"redGlow/internal/config"

	"github.com/go-chi/chi/v5"
	"go.uber.org/fx"
	"go.uber.org/zap"
)

func NewHTTPServer(lc fx.Lifecycle, cfg *config.Config, router chi.Router, logger *zap.Logger) *http.Server {
    server := &http.Server{
		Addr:    cfg.HTTPServer.Address,
        IdleTimeout: cfg.HTTPServer.IdleTimeout,
		Handler: router,
	}

    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            logger.Info("Starting http server")
            go server.ListenAndServe()
            return nil
        },
        OnStop: func(ctx context.Context) error {
            logger.Info("Stoping http server")
            return server.Shutdown(ctx)
        },
    })

    return server
}