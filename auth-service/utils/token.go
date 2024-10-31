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

func parseToken(tokenString string) (*jwt.Token, jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return []byte(config.GetEnv("JWT_SECRET", "")), nil
	})

	if err != nil {
		fmt.Println("Error parsing token: ", err)
		return nil, nil, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return token, claims, nil
	}

	return nil, nil, fmt.Errorf("invalid token")
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

func ValidateToken(accessToken string) (string, error) {
	_, claims, err := parseToken(accessToken)
	if err != nil {
		return "", err
	}

	userId := claims["userId"].(string)
	return userId, nil
}

func ValidateAndRefreshToken(refreshToken string) (string, error) {
	_, claims, err := parseToken(refreshToken)
	if err != nil {
		return "", err
	}

	userId := claims["userId"].(string)
	objectID, err := primitive.ObjectIDFromHex(userId)
	if err != nil {
		return "", fmt.Errorf("invalid userId: %v", err)
	}
	return GenerateAccessToken(objectID)
}

func RevokeToken(accessToken string) error {
	_, claims, err := parseToken(accessToken)
	if err != nil {
		return err
	}

	userId := claims["userId"].(string)
	fmt.Println("Revoking token for user: ", userId)
	return nil
}
