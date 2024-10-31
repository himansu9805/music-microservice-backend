package repositories

import (
	"auth-service/models"
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

type UserRepository struct {
	collection *mongo.Collection
}

func NewUserRepository(db *mongo.Client) *UserRepository {
	collection := db.Database("music-platform-dev").Collection("users")
	return &UserRepository{collection}
}

// ErrNoDocuments is returned when no documents are found
var ErrNoDocuments = mongo.ErrNoDocuments

// FindAll finds all users from MongoDB collection
func (r *UserRepository) FindAll() ([]models.User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	cursor, err := r.collection.Find(ctx, bson.M{})
	if err != nil {
		log.Println("Failed to retrieve users: ", err)
		return nil, err
	}
	defer cursor.Close(ctx)

	var users []models.User
	for cursor.Next(ctx) {
		var user models.User
		err := cursor.Decode(&user)
		if err != nil {
			log.Println("Failed to decode user: ", err)
			return nil, err
		}
		users = append(users, user)
	}

	return users, nil
}

// CreateUser inserts a new user into the MongoDB collection
func (r *UserRepository) CreateUser(user *models.UserRegister, hashedPassword []byte) (*mongo.InsertOneResult, error) {
	var newUser models.User = models.User{
		ID:        primitive.NewObjectID(),
		Email:     user.Email,
		Name:      user.Name,
		Password:  hashedPassword,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	result, err := r.collection.InsertOne(ctx, newUser)
	return result, err
}

// FindUserByEmail finds a user by email from the MongoDB collection
func (r *UserRepository) FindByEmail(email string) (*models.User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	var user models.User

	err := r.collection.FindOne(ctx, bson.M{"email": email}).Decode(&user)
	if err != nil {
		log.Println("Failed to retrieve user: ", err)
		return nil, err
	}

	return &user, nil
}

// UpdateUser updates a user in the MongoDB collection
func (r *UserRepository) UpdateUser(user *models.UserUpdate) (*mongo.UpdateResult, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	result, err := r.collection.UpdateOne(ctx, bson.M{"email": user.Email}, bson.M{"$set": bson.M{"name": user.Name}})
	if err != nil {
		log.Println("Failed to retrieve user: ", err)
		return nil, err
	}

	return result, nil
}

func (r *UserRepository) FindByID(id string) (*models.UserProfile, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	var user models.UserProfile

	objectID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		log.Println("ID is invalid: ", err)
		return nil, err
	}

	err = r.collection.FindOne(ctx, bson.M{"_id": objectID}).Decode(&user)
	if err != nil {
		log.Println("Failed to retrieve user: ", err)
		return nil, err
	}

	return &user, nil
}

func (r *UserRepository) ChangePassword(user *models.UserProfile, hashedPassword []byte) (*mongo.UpdateResult, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	result, err := r.collection.UpdateOne(ctx, bson.M{"_id": user.ID}, bson.M{"$set": bson.M{"password": hashedPassword}})

	if err != nil {
		log.Println("Failed to update user: ", err)
		return nil, err
	}

	return result, nil
}

func (r *UserRepository) GetCurrentHashPassword(email string) ([]byte, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	var user models.User

	err := r.collection.FindOne(ctx, bson.M{"email": email}).Decode(&user)
	if err != nil {
		log.Println("Failed to retrieve user: ", err)
		return nil, err
	}

	return user.Password, nil
}
