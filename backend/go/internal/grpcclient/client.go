package grpcclient

import (
	"context"

	"github.com/GazizX/pdf-to-text-converter/internal/interceptors"
	"github.com/GazizX/pdf-to-text-converter/internal/proto"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type GRPCClient struct {
	Conn *grpc.ClientConn
}

func NewGRPCClient(addr string, logger *zap.Logger) (*GRPCClient, error) {
	conn, err := grpc.NewClient(
		addr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithStreamInterceptor(interceptors.ClientStreamInterceptor(logger)),
	)
	if err != nil {
		return nil, err
	}
	return &GRPCClient{Conn: conn}, nil
}

func (grpcClient *GRPCClient) NewStream(ctx context.Context) (proto.PDFConverter_ConvertClient, error) {
	client := proto.NewPDFConverterClient(grpcClient.Conn)
	return client.Convert(ctx)
}
