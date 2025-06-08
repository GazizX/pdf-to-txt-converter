package utils

func IsPDF(pdfBytes []byte) bool {
	return len(pdfBytes) > 4 && string(pdfBytes[:4]) == "%PDF"
}

func SplitIntoChunks(pdfBytes []byte, size int) [][]byte {
	chunks := make([][]byte, 0, int(len(pdfBytes)/size))
	for start := 0; start < len(pdfBytes); start += size {
		end := start + size
		if end > len(pdfBytes) {
			end = len(pdfBytes)
		}
		chunks = append(chunks, pdfBytes[start:end])
	}
	return chunks
}
