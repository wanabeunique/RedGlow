package database

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Database interface{
	Acquire(ctx context.Context) (*pgxpool.Conn,error)
}