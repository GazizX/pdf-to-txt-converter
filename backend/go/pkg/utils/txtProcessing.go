package utils

import "os"

func TxtToFile(text string) (*os.File, error) {
	tmpFile, err := os.CreateTemp("", "*.txt")
	if err != nil {
		return nil, err
	}
	tmpFile.Write([]byte(text))
	return tmpFile, nil
}
