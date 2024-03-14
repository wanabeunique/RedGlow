package service

import (
	"redGlow/internal/model"
)

type AuthService interface{
	SignUp(email, username, password string) error
	ConfirmSignUp(email string) (*model.User, error)
	Login(email, password string) (*model.User, error)
	ChangePassword(oldPassword, newPassword string, userID int) error
	ChangeForgottenPassword(newPassword string, userID int) error
}