package utils

import (
	"auth-service/config"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

func GenerateAccessToken(userId primitive.ObjectID) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"userId": userId,
		"exp":    time.Now().Add(time.Hour * 3).Unix(),
		"iat":    time.Now().Unix(),
		"type":   "access",
	})

	tokenString, err := token.SignedString([]byte(config.GetEnv("JWT_SECRET", "")))
	if err != nil {
		fmt.Println("Error signing token: ", err)
		return "", err
	}

	return tokenString, nil
}

func GenerateRefreshToken(userId string) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"userId": userId,
		"exp":    time.Now().Add(time.Hour * 3).Unix(),
		"iat":    time.Now().Unix(),
		"type":   "refresh",
		"jti":    generateUniqueTokenID(),
	})

	tokenString, err := token.SignedString([]byte(config.GetEnv("JWT_SECRET", "")))
	if err != nil {
		fmt.Println("Error signing refresh token: ", err)
		return "", err
	}

	return tokenString, nil
}

func generateUniqueTokenID() string {
	return fmt.Sprintf("%d", time.Now().UnixNano())
}
