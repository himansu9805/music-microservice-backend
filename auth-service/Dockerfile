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
RUN go build -o auth-service ./cmd/server/main.go

# Create a smaller final image
FROM alpine:latest
WORKDIR /root/

# Copy the binary from the builder stage
COPY --from=build /app/auth-service .

# Expose the service port
EXPOSE 8080

# Run the binary
CMD ["./auth-service"]
