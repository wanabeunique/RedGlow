package database

import (
	"database/sql"
	"fmt"
	"redGlow/internal/config"

	_ "github.com/lib/pq"
	"go.uber.org/zap"
)

func NewPostgresDB(cfg *config.Config, logger zap.Logger) *sql.DB{
	dbConnectString := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		cfg.PostgresDB.User, cfg.PostgresDB.Password, cfg.PostgresDB.Host,
		cfg.PostgresDB.Port, cfg.PostgresDB.DatabaseName,
	)
    db, err := sql.Open("postgres", dbConnectString)
    if err != nil {
        logger.Fatal(err.Error())
    }
    defer db.Close()

    err = db.Ping()
    if err != nil {
        logger.Fatal(err.Error())
    }

    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
    return db
}