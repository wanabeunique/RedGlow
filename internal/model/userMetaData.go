package model

import (
	"time"
)

type UserMetaData struct{
	ID int
	timezone time.Location
	IPAdress string
	country string
	userId int
}