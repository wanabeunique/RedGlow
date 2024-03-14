package repository

import (
	"redGlow/internal/model"
)

type AuthRepository interface{
	Create(email, username, password string) error
	Commit(email string) (*model.User, error)
	CheckByCredentials(email, password string) (*model.User, error)
	ChangePassword(oldPassword, newPassword string, userID int) error
	ChangeForgottenPassword(newPassword string, userID int) error
}