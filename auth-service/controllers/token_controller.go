package controllers

import (
	"net/http"
	"strings"
	"time"

	"auth-service/utils"

	"github.com/gin-gonic/gin"
)

type TokenController struct{}

func NewTokenController() *TokenController {
	return &TokenController{}
}

func (tc *TokenController) RefreshAccessToken(c *gin.Context) {
	authHeader := c.GetHeader("Authorization")

	if authHeader == "" || !strings.HasPrefix(authHeader, "Bearer ") {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header missing or invalid"})
		return
	}

	refreshToken := strings.TrimPrefix(authHeader, "Bearer ")

	newAccessToken, err := utils.ValidateAndRefreshToken(refreshToken)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid refresh token"})
		return
	}

	http.SetCookie(c.Writer, &http.Cookie{
		Name:     "accessToken",
		Value:    newAccessToken,
		Expires:  time.Now().Add(time.Hour * 3),
		Path:     "/",
		HttpOnly: true,
		Secure:   true,
	})

	c.JSON(http.StatusOK, gin.H{"message": "Token refreshed successfully"})
}

func (tc *TokenController) ValidateToken(c *gin.Context) {
	accessToken := c.GetHeader("Authorization")
	if accessToken == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Access token not provided"})
		return
	}

	accessToken = strings.Replace(accessToken, "Bearer ", "", 1)
	_, err := utils.ValidateToken(accessToken)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid access token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Token is valid"})
}
