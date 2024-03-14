package auth

import (
	"redGlow/internal/database"
	"redGlow/internal/model"
	"redGlow/internal/repository"
)

var _ repository.AuthRepository = (*authRepository)(nil)

type authRepository struct{
	DB database.Database
}

func NewAuthRepository(DB database.Database) *authRepository{
	return &authRepository{
		DB: DB,
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