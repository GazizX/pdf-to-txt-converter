package converter_test

import (
	"context"
	"errors"
	"github.com/GazizX/pdf-to-text-converter/internal/converter"
	"github.com/GazizX/pdf-to-text-converter/internal/proto"
	"google.golang.org/grpc/metadata"
	"testing"
)

// mockConvertClient structure mocks python logic
type mockConvertClient struct {
	SentChunks   []*proto.PDFChunk // imitates PDF data bytes
	SendError    error             // case of error on stream.Send()
	ReceiveError error             // case of error on stream.CloseAndRecv()
	Response     string            // case of successful conversion
}

// empty methods to fully implement the proto.PDFConverter_ConvertClient interface
func (m *mockConvertClient) Header() (metadata.MD, error) {
	return metadata.MD{}, nil
}

func (m *mockConvertClient) Trailer() metadata.MD {
	return metadata.MD{}
}

func (m *mockConvertClient) CloseSend() error {
	return nil
}

func (m *mockConvertClient) Context() context.Context {
	return nil
}

func (m *mockConvertClient) SendMsg(a any) error {
	return nil
}

func (m *mockConvertClient) RecvMsg(a any) error {
	return nil
}

// required for testing methods
func (m *mockConvertClient) Send(chunk *proto.PDFChunk) error {

	if m.SendError != nil {
		return m.SendError
	}
	m.SentChunks = append(m.SentChunks, chunk)
	return nil
}

func (m *mockConvertClient) CloseAndRecv() (*proto.ConvertResponse, error) {

	if m.ReceiveError != nil {
		return nil, m.ReceiveError
	}
	return &proto.ConvertResponse{Text: m.Response}, nil
}

func TestConvertPDFtoTXT(t *testing.T) {

	tests := []struct {
		name             string
		inputBytes       []byte
		mockResponse     string
		mockSendError    error
		mockReceiveError error
		want             string
		wantErr          bool
	}{
		{
			name:         "successful conversion",
			inputBytes:   []byte("data"),
			mockResponse: "converted text",
			want:         "converted text",
			wantErr:      false,
		},
		{
			name:          "send error",
			inputBytes:    []byte("data"),
			mockSendError: errors.New("send failed"),
			wantErr:       true,
		},
		{
			name:             "receive error",
			inputBytes:       []byte("data"),
			mockReceiveError: errors.New("receive failed"),
			wantErr:          true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {

			mockStream := mockConvertClient{
				SendError:    tt.mockSendError,
				ReceiveError: tt.mockReceiveError,
				Response:     tt.mockResponse,
			}

			got, err := converter.ConvertPDFtoTXT(tt.inputBytes, &mockStream)
			if (err != nil) != tt.wantErr {
				t.Fatalf("unexpected error state: got err=%v, wantErr=%v", err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("unexpected result: got=%v, want=%v", got, tt.want)
			}
		})
	}
}
