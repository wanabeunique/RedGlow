package config

import (
	"os"
	"time"

	"github.com/joho/godotenv"
	"go.uber.org/zap"
	"gopkg.in/yaml.v3"
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

func NewConfig(logger *zap.Logger) *Config {
    if err := godotenv.Load(); err != nil {
        logger.Fatal("No .env file found")
    }
    
    path := os.Getenv("CONFIG_PATH")
    if path == "" {
        logger.Fatal("CONFIG_PATH environment variable is not set")
    }
    
    data, err := os.ReadFile(path)
    if err != nil {
        return nil
    }
    replaced := os.ExpandEnv(string(data))
    cfg := &Config{}
    err = yaml.Unmarshal([]byte(replaced), cfg)
    return cfg
}