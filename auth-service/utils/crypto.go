package utils

import (
	"golang.org/x/crypto/bcrypt"

	"fmt"
)

// HashPassword hashes the password using bcrypt
func HashPassword(password string) ([]byte, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("failed to hash password: %v", err)
	}

	return hashedPassword, nil
}

// ComparePasswords compares the hashed password with the plain-text password
func ComparePasswords(hashedPassword []byte, password string) error {
	err := bcrypt.CompareHashAndPassword(hashedPassword, []byte(password))
	if err != nil {
		return fmt.Errorf("failed to compare passwords: %v", err)
	}

	return nil
}
