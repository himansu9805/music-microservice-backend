#!/bin/bash

# Check if service name is passed as an argument
if [ -z "$1" ]; then
    echo "Error: No service name provided."
    echo "Usage: ./create-microservice-with-logs-and-go-commands.sh <service-name>"
    exit 1
fi

# Define service name
SERVICE_NAME=$1

# Function to log progress
log() {
    echo "[INFO] $1"
}

# Create the directory structure for the new microservice
log "Creating directory structure for $SERVICE_NAME..."
mkdir -p $SERVICE_NAME/{cmd/server,controllers,models,repositories,services,routes,config}

# Navigate to the service directory
cd $SERVICE_NAME || exit

# Initialize a Go module
log "Initializing Go module for $SERVICE_NAME..."
go mod init "$SERVICE_NAME"

# Add Gin Gonic dependency
log "Adding Gin Gonic as a dependency..."
go get github.com/gin-gonic/gin

# Add MongoDB dependency
log "Adding MongoDB as a dependency..."
go get go.mongodb.org/mongo-driver/mongo

# Tidy the Go module
log "Tidying Go module..."
go mod tidy

# Go back to the root directory
cd ..

# Create main.go file inside cmd/server
log "Generating main.go file..."
cat <<EOF > $SERVICE_NAME/cmd/server/main.go
package main

import (
    "github.com/gin-gonic/gin"
    "$SERVICE_NAME/routes"
    "log"
    "os"
)

func main() {
    router := gin.Default()

    // Setup routes
    routes.SetupRoutes(router)

    // Get port from environment or default to 8080
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    log.Printf("Starting $SERVICE_NAME on port %s", port)
    router.Run(":" + port)
}
EOF

# Create controller file
log "Creating controller file for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/controllers/${SERVICE_NAME}_controller.go
package controllers

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

func GetExample(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "message": "$SERVICE_NAME is working!",
    })
}
EOF

# Create model file
log "Creating model file for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/models/${SERVICE_NAME}.go
package models

type Example struct {
    ID   uint   \`json:"id"\`
    Name string \`json:"name"\`
}
EOF

# Create repository file
log "Creating repository file for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/repositories/${SERVICE_NAME}_repository.go
package repositories

import "$SERVICE_NAME/models"

type ExampleRepository struct{}

func NewExampleRepository() *ExampleRepository {
    return &ExampleRepository{}
}

func (r *ExampleRepository) GetExamples() []models.Example {
    return []models.Example{
        {ID: 1, Name: "Example 1"},
        {ID: 2, Name: "Example 2"},
    }
}
EOF

# Create service file
log "Creating service file for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/services/${SERVICE_NAME}_service.go
package services

import (
    "$SERVICE_NAME/models"
    "$SERVICE_NAME/repositories"
)

type ExampleService struct {
    repo *repositories.ExampleRepository
}

func NewExampleService(repo *repositories.ExampleRepository) *ExampleService {
    return &ExampleService{repo}
}

func (s *ExampleService) GetExamples() []models.Example {
    return s.repo.GetExamples()
}
EOF

# Create routes file
log "Creating routes file for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/routes/routes.go
package routes

import (
    "github.com/gin-gonic/gin"
    "$SERVICE_NAME/controllers"
)

func SetupRoutes(router *gin.Engine) {
    router.GET("/example", controllers.GetExample)
}
EOF

# Create config file
log "Creating config file for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/config/config.go
package config

import "os"

// GetEnv fetches environment variables with a fallback default value.
func GetEnv(key, defaultValue string) string {
    value := os.Getenv(key)
    if value == "" {
        return defaultValue
    }
    return value
}
EOF

# Create Dockerfile
log "Creating Dockerfile for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/Dockerfile
# Build the Go app
FROM golang:1.19-alpine as build

WORKDIR /app

# Copy go.mod and go.sum
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source files
COPY . .

# Build the Go app
RUN go build -o $SERVICE_NAME ./cmd/server/main.go

# Create a smaller final image
FROM alpine:latest
WORKDIR /root/

# Copy the binary from the builder stage
COPY --from=build /app/$SERVICE_NAME .

# Expose the service port
EXPOSE 8080

# Run the binary
CMD ["./$SERVICE_NAME"]
EOF

# Create README file
log "Creating README.md for $SERVICE_NAME..."
cat <<EOF > $SERVICE_NAME/README.md
# $SERVICE_NAME

## Overview

This microservice is responsible for handling $SERVICE_NAME-specific operations. It is built using the Gin Gonic web framework in Go and follows a clean architecture to separate concerns for controllers, services, and repositories.

## Directory Structure

\`\`\`
/$SERVICE_NAME
├── cmd
│   └── server
│       └── main.go              # Entry point
├── controllers
│   └── ${SERVICE_NAME}_controller.go  # Handles HTTP requests
├── models
│   └── ${SERVICE_NAME}.go             # Defines ${SERVICE_NAME} model
├── repositories
│   └── ${SERVICE_NAME}_repository.go  # Database interactions for $SERVICE_NAME
├── services
│   └── ${SERVICE_NAME}_service.go     # Business logic for $SERVICE_NAME
├── routes
│   └── routes.go                # Registers all routes
├── config
│   └── config.go                # Environment and config handling
├── Dockerfile                   # To containerize the service
└── go.mod                       # Go module for $SERVICE_NAME
\`\`\`

## Running the Service

1. Install dependencies:
   \`\`\`
   go mod tidy
   \`\`\`

2. Run the service:
   \`\`\`
   go run ./cmd/server/main.go
   \`\`\`

3. Build the Docker image:
   \`\`\`
   docker build -t $SERVICE_NAME .
   \`\`\`

4. Run the service with Docker:
   \`\`\`
   docker run -p 8080:8080 $SERVICE_NAME
   \`\`\`

5. **Important:** You may need to source the \`~/.profile\` manually to apply any new environment variables:
   \`\`\`
   source ~/.profile
   \`\`\`

6. Access the service at \`http://localhost:8080/example\`.
EOF

# Notify user of the created service
log "Microservice '$SERVICE_NAME' has been created with the necessary structure and files."

