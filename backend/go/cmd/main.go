package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/GazizX/pdf-to-text-converter/internal/grpcclient"
	"github.com/GazizX/pdf-to-text-converter/internal/handlers"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"go.uber.org/zap"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	PORT := os.Getenv("PORT")
	PY_PORT := os.Getenv("PY_PORT")
	FRONTEND_PORT := os.Getenv("FRONTEND_PORT")

	logger, _ := zap.NewProduction()
	sugar := logger.Sugar()
	defer logger.Sync()

	newClient, err := grpcclient.NewGRPCClient(fmt.Sprintf("python-grpc:%s", PY_PORT), logger)
	if err != nil {
		log.Fatalf("could not connect to gRPC server(Python): %v", err)
	}

	router := gin.Default()
	router.MaxMultipartMemory = 25 << 20 // 25 Mb

	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{fmt.Sprintf("http://localhost:%s", FRONTEND_PORT)},
		AllowMethods:     []string{"POST", "GET", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Disposition"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	router.POST("/convert", handlers.HandleConvertPDF(newClient, sugar))

	router.Run(fmt.Sprintf(":%s", PORT))
}
