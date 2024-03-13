package config

import (
	"log"
	"os"
	"time"

	"github.com/ilyakaznacheev/cleanenv"
	"github.com/joho/godotenv"
)

type Config struct {
    Env         string `yaml:"env" env-default:"development"`
    HTTPServer `yaml:"http_server"`
    PostgresDB `yaml:"postgres"`
}

type HTTPServer struct {
    Address     string        `yaml:"address" env-default:"0.0.0.0:8000"`
    Timeout     time.Duration `yaml:"timeout" env-default:"5s"`
    IdleTimeout time.Duration `yaml:"idle_timeout" env-default:"60s"`
}

type PostgresDB struct {
    Host string `yaml:"host"`
    Port string `yaml:"port"`
    User string `yaml:"user"`
    Password string `yaml:"password"`
    DatabaseName string `yaml:"db_name"`
}

func NewConfig() *Config {
    if err := godotenv.Load(); err != nil {
        log.Fatal("No .env file found")
    }
    
    configPath := os.Getenv("CONFIG_PATH")
    if configPath == "" {
        log.Fatal("CONFIG_PATH environment variable is not set")
    }

    if _, err := os.Stat(configPath); err != nil {
        log.Fatalf("error opening config file: %s", err)
    }

    var cfg Config

    err := cleanenv.ReadConfig(configPath, &cfg)
    if err != nil {
        log.Fatalf("error reading config file: %s", err)
    }

    return &cfg
}