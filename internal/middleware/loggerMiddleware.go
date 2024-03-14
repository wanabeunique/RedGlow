package middleware

import (
	"net/http"

	"github.com/leosunmo/zapchi"
	"go.uber.org/zap"
)

type LoggerMiddleware struct {
	Logger *zap.Logger
}

func NewLoggerMiddleware(logger *zap.Logger) *LoggerMiddleware{
	return &LoggerMiddleware{
		Logger:logger,
	}
}

func (lm *LoggerMiddleware) GetMiddlewareFunc() func(http.Handler) http.Handler{
	return zapchi.Logger(lm.Logger,"")
}