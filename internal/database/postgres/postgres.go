package postgres

import (
	"context"
	"fmt"
	"redGlow/internal/config"
	"redGlow/internal/database"

	"github.com/jackc/pgx/v5/pgxpool"
	"go.uber.org/zap"
)

var _ database.Database = (*postgresDB)(nil)

type postgresDB struct{
    pool *pgxpool.Pool
}

func NewPostgresDB(cfg *config.Config, ctx context.Context, logger *zap.Logger) *postgresDB{
	dbConnectString := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		cfg.PostgresDB.User, cfg.PostgresDB.Password, cfg.PostgresDB.Host,
		cfg.PostgresDB.Port, cfg.PostgresDB.DatabaseName,
	)
	logger.Info(dbConnectString)
    pool, err := pgxpool.New(ctx, dbConnectString)
	if err != nil {
		logger.Fatal("Error to connect to postgresql")
	}
	defer pool.Close()

    return &postgresDB{
        pool: pool,
    }
}

func (postgres *postgresDB) Acquire(ctx context.Context) (*pgxpool.Conn,error){
    return postgres.pool.Acquire(ctx)
}