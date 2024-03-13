package user

import (
	"database/sql"
)

type userRepository struct{
	db *sql.DB
}

func NewAuthRepository(db *sql.DB) *userRepository{
	return &userRepository{
		db: db,
	}
}