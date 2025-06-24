package utils_test

import (
	"bytes"
	"github.com/GazizX/pdf-to-text-converter/pkg/utils"
	"testing"
)

func TestSplitIntoChunks(t *testing.T) {
	tests := []struct {
		name      string
		input     []byte
		chunkSize int
		want      [][]byte
	}{
		{
			name:      "exact split",
			input:     []byte("123456"),
			chunkSize: 2,
			want: [][]byte{
				[]byte("12"),
				[]byte("34"),
				[]byte("56"),
			},
		},
		{
			name:      "not exact split",
			input:     []byte("123456"),
			chunkSize: 4,
			want: [][]byte{
				[]byte("1234"),
				[]byte("56"),
			},
		},
		{
			name:      "chunk size is larger than input",
			input:     []byte("123456"),
			chunkSize: 7,
			want: [][]byte{
				[]byte("123456"),
			},
		},
		{
			name:      "empty input",
			input:     []byte{},
			chunkSize: 2,
			want:      [][]byte{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := utils.SplitIntoChunks(tt.input, tt.chunkSize)

			if len(got) != len(tt.want) {
				t.Fatalf("expected %v chunks, got %v", got, tt.want)
			}

			for i := range got {
				if !bytes.Equal(got[i], tt.want[i]) {
					t.Errorf("chunk %v: expected %v, got %v", i, tt.want[i], got[i])
				}
			}
		})
	}
}
