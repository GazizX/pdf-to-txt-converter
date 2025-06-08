package main

import (
	"log"

	"github.com/GazizX/pdf-to-text-converter/internal/grpcclient"
	"github.com/GazizX/pdf-to-text-converter/internal/handlers"
	"github.com/gin-gonic/gin"
)

func main() {

	newClient, err := grpcclient.NewGRPCClient(":50051") // заменить на ServerPORT из .env
	if err != nil {
		log.Printf("could not connect to gRPC server(Python): %v", err)
	}

	router := gin.Default()
	router.MaxMultipartMemory = 25 << 20 // 25 Mb

	router.POST("/convert", handlers.HandleConvertPDF(newClient))

	router.Run(":8080") // заменить на ClientPORT из .env
}
