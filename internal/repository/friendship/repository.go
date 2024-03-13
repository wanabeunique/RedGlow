package friendship

import (
	"database/sql"
)

type friendshipRepository struct{
	db *sql.DB
}

func NewAuthRepository(db *sql.DB) *friendshipRepository{
	return &friendshipRepository{
		db: db,
	}
}
