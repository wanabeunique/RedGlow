package auth

import (
	"redGlow/internal/model"
	"redGlow/internal/repository"
	"redGlow/internal/service"
)

var _ service.AuthService = (*authService)(nil)

type authService struct {
	repo repository.AuthRepository
}

func NewAuthService(repo repository.AuthRepository) *authService{
	return &authService{
		repo: repo,
	}
}


func (as *authService) SignUp(email, username, password string) error{
	return nil
}

func (as *authService) ConfirmSignUp(email string) (*model.User, error){
	return nil,nil
}

func (as *authService) Login(email, password string) (*model.User, error){
	return nil,nil
}

func (as *authService) ChangePassword(oldPassword, newPassword string, userID int) error{
	return nil
}

func (as *authService) ChangeForgottenPassword(newPassword string, userID int) error{
	return nil	
}
