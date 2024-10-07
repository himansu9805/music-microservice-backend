package routes

import (
	"auth-service/controllers"
	"auth-service/services"

	"github.com/gin-gonic/gin"
)

func SetupRoutes(router *gin.Engine, userService *services.UserService) {
	userController := controllers.NewUserController(userService)

	// Route for creating a new user
	router.POST("/users/register", userController.CreateUser)
	router.POST("/users/login", userController.LoginUser)
}
