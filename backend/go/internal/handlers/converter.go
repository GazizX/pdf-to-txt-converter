package handlers

import (
	"fmt"
	"io"
	"net/http"

	"github.com/GazizX/pdf-to-text-converter/internal/converter"
	"github.com/GazizX/pdf-to-text-converter/internal/grpcclient"
	"github.com/GazizX/pdf-to-text-converter/pkg/utils"
	"github.com/gin-gonic/gin"
)

func HandleConvertPDF(client *grpcclient.GRPCClient) gin.HandlerFunc {
	return func(c *gin.Context) {
		file, err := c.FormFile("file")
		if err != nil {
			c.String(http.StatusBadRequest, fmt.Sprintf("no file provided: %v", err))
			return
		}

		fileContent, err := file.Open()
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to open file: %v", err))
			return
		}
		defer fileContent.Close()

		pdfBytes, err := io.ReadAll(fileContent)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to read file: %v", err))
			return
		}

		if !utils.IsPDF(pdfBytes) {
			c.String(http.StatusBadRequest, "not a valid PDF file")
			return
		}

		stream, err := client.NewStream(c)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to create gRPC stream: %v", err))
		}

		txtResult, err := converter.ConvertPDFtoTXT(pdfBytes, stream)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to convert file: %v", err))
			return
		}

		c.Data(http.StatusOK, "text/plain", []byte(txtResult))
	}
}
