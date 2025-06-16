package converter

import (
	"github.com/GazizX/pdf-to-text-converter/internal/proto"
	"github.com/GazizX/pdf-to-text-converter/pkg/utils"
)

const chunkSize = 32 * 1024 // 32 Kb

func ConvertPDFtoTXT(pdfBytes []byte, stream proto.PDFConverter_ConvertClient) (string, error) {
	for _, chunk := range utils.SplitIntoChunks(pdfBytes, chunkSize) {
		err := stream.Send(&proto.PDFChunk{Data: chunk})
		if err != nil {
			return "", err
		}
	}

	response, err := stream.CloseAndRecv()
	if err != nil {
		return "", err
	}

	return response.GetText(), nil
}
