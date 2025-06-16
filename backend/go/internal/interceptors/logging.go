package interceptors

import (
	"context"
	"time"

	"go.uber.org/zap"
	"google.golang.org/grpc"
)

func ClientStreamInterceptor(logger *zap.Logger) grpc.StreamClientInterceptor {
	return func(
		ctx context.Context,
		desc *grpc.StreamDesc,
		cc *grpc.ClientConn,
		method string,
		streamer grpc.Streamer,
		opts ...grpc.CallOption,
	) (grpc.ClientStream, error) {
		start := time.Now()

		stream, err := streamer(ctx, desc, cc, method, opts...)

		logger.Info("Client stream",
			zap.String("method", method),
			zap.Duration("duration", time.Since(start)),
			zap.Bool("error", err != nil),
		)

		return stream, err
	}
}
