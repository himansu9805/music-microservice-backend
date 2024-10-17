package utils

import (
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"go.mongodb.org/mongo-driver/bson/primitive"

	"auth-service/config"
)

func generateUniqueTokenID() string {
	return fmt.Sprintf("%d", time.Now().UnixNano())
}

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

func ValidateAndRefreshToken(refreshToken string) (string, error) {
	token, err := jwt.Parse(refreshToken, func(token *jwt.Token) (interface{}, error) {
		return []byte(config.GetEnv("JWT_SECRET", "")), nil
	})

	if err != nil {
		fmt.Println("Error parsing token: ", err)
		return "", err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		userId := claims["userId"].(string)
		objectID, err := primitive.ObjectIDFromHex(userId)
		if err != nil {
			return "", fmt.Errorf("invalid userId: %v", err)
		}
		return GenerateAccessToken(objectID)
	}

	return "", fmt.Errorf("invalid token")
}
