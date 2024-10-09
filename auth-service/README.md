# auth-service

## Overview

This microservice is responsible for handling auth-service-specific operations. It is built using the Gin Gonic web framework in Go and follows a clean architecture to separate concerns for controllers, services, and repositories.

## Directory Structure

```plaintext
/auth-service
├── cmd
│   └── server
│       └── main.go              # Entry point
├── controllers
│   └── auth-service_controller.go  # Handles HTTP requests
├── models
│   └── auth-service.go             # Defines auth-service model
├── repositories
│   └── auth-service_repository.go  # Database interactions for auth-service
├── services
│   └── auth-service_service.go     # Business logic for auth-service
├── routes
│   └── routes.go                # Registers all routes
├── config
│   └── config.go                # Environment and config handling
├── Dockerfile                   # To containerize the service
└── go.mod                       # Go module for auth-service
```

## Running the Service

1. Install dependencies:

   ```
   go mod tidy
   ```

2. Run the service:

   ```
   go run ./cmd/server/main.go
   ```

3. Build the Docker image:

   ```
   docker build -t auth-service .
   ```

4. Run the service with Docker:

   ```
   docker run -p 8080:8080 auth-service
   ```

5. **Important:** You may need to source the `~/.profile` manually to apply any new environment variables:

   ```
   source ~/.profile
   ```

6. Access the service at `http://localhost:8080/example`.
