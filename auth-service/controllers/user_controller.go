package controllers

import (
	"auth-service/config"
	"auth-service/models"
	"auth-service/services"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
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

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"userId": user.ID,
		"exp":    time.Now().Add(time.Hour * 3).Unix(),
	})

	tokenString, err := token.SignedString([]byte(config.GetEnv("JWT_SECRET", "")))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	http.SetCookie(c.Writer, &http.Cookie{
		Name:     "jwt",
		Value:    tokenString,
		Expires:  time.Now().Add(time.Hour * 3),
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
