package auth

import (
	"database/sql"
	"redGlow/internal/database/model"
)

type authRepository struct{
	db *sql.DB
}

func NewAuthRepository(db *sql.DB) *authRepository{
	return &authRepository{
		db: db,
	}
}

func (authRep *authRepository) Create(email, username, password string) error{
	return nil
}

func (authRep *authRepository) Commit(email string) (*model.User, error){
	return nil, nil
}

func (authRep *authRepository) CheckByCredentials(email, password string) (*model.User, error){
	return nil, nil
}

func (authRep *authRepository) ChangePassword(oldPassword, newPassword string, userID int) error{
	return nil
}

func (authRep *authRepository) ChangeForgottenPassword(newPassword string, userID int) error{
	return nil
}