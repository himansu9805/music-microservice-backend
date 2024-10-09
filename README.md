# Project Overview

This project consists of multiple microservices, right now only authentication service (`auth-service`) is implemented. Each microservice is responsible for handling specific operations and is built using the Gin Gonic web framework in Go. The project follows a clean architecture to separate concerns for controllers, services, and repositories.

## Directory Structure

The project directory structure is as follows:

```plaintext
/music-microservice-backend
|-- auth-service
|-- music-service       -> [WIP]
|-- user-service        -> [WIP]
|-- create-service.sh
|-- get-service.sh 
|-- README.md
```

## Running the Project

### Prerequisites

- Go 1.19 or later
- Docker
- Docker Compose

### Setting Up the Environment

1. **Clone the repository:** Clone the repository to your local machine.

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up environment variables:** Create a .env file in the root directory and add the necessary environment variables.
3. **Install dependencies:**

    ```sh
    go mod tidy
    ```

### Running the Services for Development

1. Navigate to the service directory:

    ```sh
    cd <service-directory>
    ```

2. Run the service:

    ```sh
    go run ./cmd/server/main.go
    ```

3. The service will be running on `http://localhost:8080`.

### Creating a New Service

Use the `create_service.sh` script to create a new microservice:
  
  ```sh
  . create_service.sh <service-name>
  ```

This script will generate the necessary directory structure and files for the new microservice.
