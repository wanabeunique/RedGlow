package model

type User struct{
	ID int
	username string
	email string
	phoneNumber *string
	isActive *string
	steamId *string
	photoPath *string
	backgroundPath *string
}