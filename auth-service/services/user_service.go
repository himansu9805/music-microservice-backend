package services

import (
	"auth-service/models"
	"auth-service/repositories"
	"auth-service/utils"
	"errors"
	"fmt"
)

type UserService struct {
	userRepo *repositories.UserRepository
}

func NewUserService(userRepo *repositories.UserRepository) *UserService {
	return &UserService{userRepo: userRepo}
}

func (s *UserService) CreateUser(user *models.UserRegister) error {
	existingUser, err := s.userRepo.FindByEmail(user.Email)
	if err != nil && err != repositories.ErrNoDocuments {
		fmt.Println("Error finding user by email: ", err)
		return err
	}
	if existingUser != nil {
		return errors.New("Email already registered")
	}

	hashedPassword, err := utils.HashPassword(user.Password)
	if err != nil {
		return err
	}

	_, err = s.userRepo.CreateUser(user, hashedPassword)
	return err
}

func (s *UserService) AuthenticateUser(email, password string) (*models.User, error) {
	user, err := s.userRepo.FindByEmail(email)
	if err != nil {
		return nil, err
	}

	if user == nil {
		return nil, errors.New("User not found")
	}

	if utils.ComparePasswords(user.Password, password) != nil {
		return nil, errors.New("Invalid password")
	}

	return user, nil
}

func (s *UserService) UpdateUser(user *models.UserUpdate) error {
	objectID, err := s.userRepo.FindByEmail(user.Email)
	if err != nil {
		return err
	}

	if objectID == nil {

		return errors.New("User not found")
	}

	_, err = s.userRepo.UpdateUser(user)
	if err != nil {
		return err
	}

	return nil
}

func (s *UserService) GetProfile(userId string) (*models.UserProfile, error) {
	user, err := s.userRepo.FindByID(userId)
	if err != nil {
		return nil, err
	}

	if user == nil {
		return nil, errors.New("User not found")
	}

	return user, nil
}
