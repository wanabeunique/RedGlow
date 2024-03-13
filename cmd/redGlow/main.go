package main

import (
	"net/http"
	"redGlow/internal/config"
	"redGlow/internal/handler"
	"redGlow/internal/httpserver"
	"redGlow/internal/router"

	"go.uber.org/fx"
	"go.uber.org/fx/fxevent"
	"go.uber.org/zap"
)


func main(){
    fx.New(
        fx.WithLogger(func (logger *zap.Logger) fxevent.Logger  {
            return &fxevent.ZapLogger{Logger: logger}
        }),
        fx.Provide(
            config.NewConfig,
            zap.NewProduction,
            // router.NewChiRouter,
            fx.Annotate(
                router.NewChiRouter,
                fx.ParamTags(`group:"routes"`),
            ),
            AsRoute(handler.NewAuthenticationHandler),  
            httpserver.NewHTTPServer,
        ),
        fx.Invoke(func(*http.Server) {}),
    ).Run()
}

func AsRoute(f any) any {
  return fx.Annotate(
    f,
    fx.As(new(router.Route)),
    fx.ResultTags(`group:"routes"`),
  )
}