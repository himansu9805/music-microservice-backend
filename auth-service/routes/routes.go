package routes

import (
	"github.com/gin-gonic/gin"

	"auth-service/controllers"
	"auth-service/middlewares"
	"auth-service/services"
)

func SetupRoutes(router *gin.Engine, userService *services.UserService) {
	userController := controllers.NewUserController(userService)

	// Route for creating a new user
	userRouter := router.Group("/users")
	{
		userRouter.POST("/register", userController.CreateUser)
		userRouter.POST("/login", userController.LoginUser)
	}

	tokenRouter := router.Group("/token")
	{
		tokenRouter.GET("/refresh", userController.RefreshUser)
	}

	accountRouter := router.Group("/account").Use(middlewares.AuthMiddleware())
	{
		accountRouter.PUT("/update", userController.UpdateUser)
		accountRouter.GET("/profile", userController.GetProfile)
	}
}
