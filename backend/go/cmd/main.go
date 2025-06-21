package main

import (
	"log"
	"time"

	"github.com/GazizX/pdf-to-text-converter/internal/grpcclient"
	"github.com/GazizX/pdf-to-text-converter/internal/handlers"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func main() {
	logger, _ := zap.NewProduction()
	sugar := logger.Sugar()
	defer logger.Sync()

	newClient, err := grpcclient.NewGRPCClient(":50051", logger) // заменить на ServerPORT из .env
	if err != nil {
		log.Fatalf("could not connect to gRPC server(Python): %v", err)
	}

	router := gin.Default()
	router.MaxMultipartMemory = 25 << 20 // 25 Mb

	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173"},
		AllowMethods:     []string{"POST", "GET", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	router.POST("/convert", handlers.HandleConvertPDF(newClient, sugar))

	router.Run(":8080") // заменить на ClientPORT из .env
}
