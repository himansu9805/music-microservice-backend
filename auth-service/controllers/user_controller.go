package controllers

import (
	"auth-service/models"
	"auth-service/services"
	"net/http"

	"github.com/gin-gonic/gin"
)

type UserController struct {
	userService *services.UserService
}

func NewUserController(service *services.UserService) *UserController {
	return &UserController{userService: service}
}

func (uc *UserController) CreateUser(c *gin.Context) {
	var user models.User

	// Bind JSON body to user model
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Call service to create the user
	if err := uc.userService.CreateUser(&user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "User created successfully", "user": user})
}

func (uc *UserController) LoginUser(c *gin.Context) {
	var login models.UserLogin

	// Bind JSON body to login model
	if err := c.ShouldBindJSON(&login); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Call service to authenticate the user
	user, err := uc.userService.AuthenticateUser(login.Email, login.Password)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "User authenticated successfully", "user": user})
}