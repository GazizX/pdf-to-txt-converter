package handlers

import (
	"context"
	"fmt"
	"io"
	"net/http"

	"github.com/GazizX/pdf-to-text-converter/internal/converter"
	"github.com/GazizX/pdf-to-text-converter/internal/grpcclient"
	"github.com/GazizX/pdf-to-text-converter/pkg/utils"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func HandleConvertPDF(client *grpcclient.GRPCClient, logger *zap.SugaredLogger) gin.HandlerFunc {
	return func(c *gin.Context) {
		file, err := c.FormFile("file")
		if err != nil {
			c.String(http.StatusBadRequest, fmt.Sprintf("no file provided: %v", err))
			logger.Infof("no file provided: %v", err)
			return
		}

		fileContent, err := file.Open()
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to open file: %v", err))
			logger.Infof("failed to open file: %v", err)
			return
		}
		defer fileContent.Close()

		pdfBytes, err := io.ReadAll(fileContent)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to read file: %v", err))
			logger.Infof("failed to read file: %v", err)
			return
		}

		if !utils.IsPDF(pdfBytes) {
			c.String(http.StatusBadRequest, "not a valid PDF file")
			logger.Infof("not a valid PDF file")
			return
		}
		ctx := context.Background()
		stream, err := client.NewStream(ctx)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to create gRPC stream: %v", err))
			logger.Infof("failed to create gRPC stream: %v", err)
			return
		}

		txtResult, err := converter.ConvertPDFtoTXT(pdfBytes, stream)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to convert file: %v", err))
			logger.Infof("failed to convert file: %v", err)
			return
		}

		txtFile, err := utils.TxtToFile(txtResult)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to convert string into .txt: %v", err))
			logger.Infof("failed to convert string into .txt: %v", err)
			return
		}

		c.FileAttachment(txtFile.Name(), "converted.txt")
	}
}
