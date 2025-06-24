FROM golang:1.23.5 as builder
WORKDIR /app
COPY backend/go/go.mod backend/go/go.sum ./
RUN go mod download
COPY backend/go/ ./
RUN CGO_ENABLED=0 GOOS=linux go build -o /backend ./cmd/main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /backend /app/backend
EXPOSE 8080
CMD ["/app/backend"]