package main

import (
	"auth-service/config"
	"auth-service/repositories"
	"auth-service/routes"
	"auth-service/services"
	"log"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	// Connect to MongoDB
	mongoClient := config.ConnectMongoDB()
	defer mongoClient.Disconnect(nil)

	// Create user repository
	userRepository := repositories.NewUserRepository(mongoClient)

	// Create user service
	userService := services.NewUserService(userRepository)

	// Setup routes
	routes.SetupRoutes(router, userService)

	// Get port from environment or default to 8080
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Starting auth-service on port %s", port)
	router.Run(":" + port)
}
