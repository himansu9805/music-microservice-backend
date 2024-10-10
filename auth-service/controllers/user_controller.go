package controllers

import (
	"auth-service/models"
	"auth-service/services"
	"auth-service/utils"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type UserController struct {
	userService *services.UserService
}

func NewUserController(service *services.UserService) *UserController {
	return &UserController{userService: service}
}

func (uc *UserController) CreateUser(c *gin.Context) {
	var userRegister models.UserRegister

	// Bind JSON body to user model
	if err := c.ShouldBindJSON(&userRegister); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Call service to create the user
	if err := uc.userService.CreateUser(&userRegister); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "User created successfully", "user": userRegister})
}

func (uc *UserController) LoginUser(c *gin.Context) {
	var userLogin models.UserLogin

	// Bind JSON body to user login model
	if err := c.ShouldBindJSON(&userLogin); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Call service to authenticate the user
	user, err := uc.userService.AuthenticateUser(userLogin.Email, userLogin.Password)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": err.Error()})
		return
	}

	accessToken, err := utils.GenerateAccessToken(user.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	refreshToken, err := utils.GenerateRefreshToken(user.ID.Hex())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	http.SetCookie(c.Writer, &http.Cookie{
		Name:     "accessToken",
		Value:    accessToken,
		Expires:  time.Now().Add(time.Hour * 3),
		Path:     "/",
		HttpOnly: true,
		Secure:   true,
	})
	http.SetCookie(c.Writer, &http.Cookie{
		Name:     "refreshToken",
		Value:    refreshToken,
		Expires:  time.Now().Add(time.Hour * 24 * 7),
		Path:     "/",
		HttpOnly: true,
		Secure:   true,
	})

	c.JSON(http.StatusOK, gin.H{"message": "User authenticated successfully", "user": user})
}

func (uc *UserController) UpdateUser(c *gin.Context) {
	var userUpdate models.UserUpdate

	// Bind JSON body to user update model
	if err := c.ShouldBindJSON(&userUpdate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err := uc.userService.UpdateUser(&userUpdate)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "User updated successfully", "user": userUpdate})
}

func (uc *UserController) GetProfile(c *gin.Context) {
	userId := c.GetString("userId")

	fmt.Println("userId: ", userId)

	userProfile, err := uc.userService.GetProfile(userId)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Profile retrieved successfully", "user": userProfile})
}
