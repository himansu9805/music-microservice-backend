package routes

import (
	"auth-service/controllers"
	"auth-service/middlewares"
	"auth-service/services"

	"github.com/gin-gonic/gin"
)

func SetupRoutes(router *gin.Engine, userService *services.UserService) {
	userController := controllers.NewUserController(userService)

	// Route for creating a new user
	userRouter := router.Group("/users")
	{
		userRouter.POST("/register", userController.CreateUser)
		userRouter.POST("/login", userController.LoginUser)
	}

	accountRouter := router.Group("/account").Use(middlewares.AuthMiddleware())
	{
		accountRouter.PUT("/update", userController.UpdateUser)
		accountRouter.GET("/profile", userController.GetProfile)
	}
}
