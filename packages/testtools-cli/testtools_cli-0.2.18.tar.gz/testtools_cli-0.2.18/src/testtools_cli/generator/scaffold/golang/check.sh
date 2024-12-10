#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

info() {
    echo -e "${GREEN}$1${NC}"
}

error() {
    echo -e "${RED}$1${NC}"
}

# go fmt
info "Running go fmt..."
if ! go fmt ./...; then
    error "go fmt failed"
    exit 1
fi

# go vet
info "Running go vet..."
if ! go vet ./...; then
    error "go vet failed"
    exit 1
fi

# go lint
info "Running golangci-lint..."
if ! golangci-lint run; then
    error "golangci-lint failed"
    exit 1
fi

# go test
trap "rm coverage.out" EXIT
COVERAGE_THRESHOLD=70

go test -p 1 -coverprofile=coverage.out ./...

COVERAGE=$(go tool cover -func=coverage.out | awk '/total:/ {print substr($3, 1, length($3)-1)}')

info "Total test coverage: ${COVERAGE}%"

if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
  error "Coverage below threshold: ${COVERAGE_THRESHOLD}%"
  exit 1
else
  info "Coverage meets the threshold: ${COVERAGE_THRESHOLD}%"
fi