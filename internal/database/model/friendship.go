package model

import (
	"time"
)

type StatusName string

const (
	Ivited StatusName = "Заявка отправлена"
	Friends StatusName = "Друзья"
)

type Friendship struct{
	ID int
	inviterID int
	accepterID int
	status StatusName
	createdAt time.Time
}