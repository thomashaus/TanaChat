.PHONY: setup dev test lint build docker-build docker-run docker-stop mcp-test mcp-debug deploy-www deploy-api deploy-mcp clean help samples validate-samples seed-samples generate-samples

help:
	@echo "TanaChat.ai Development Commands"
	@echo ""
	@echo "Development:"
	@echo "  make setup      - Initial setup"
	@echo "  make build      - Build all components"
	@echo "  make dev        - Start all services"
	@echo "  make test       - Run all tests"
	@echo "  make lint       - Run all linters"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-run   - Run services in Docker"
	@echo "  make docker-stop  - Stop Docker services"
	@echo ""
	@echo "MCP:"
	@echo "  make mcp-test   - Test with inspector"
	@echo "  make mcp-debug  - Debug via stdio"
	@echo ""
	@echo "Deploy:"
	@echo "  make deploy-www - Deploy www"
	@echo "  make deploy-api - Deploy api"
	@echo "  make deploy-mcp - Deploy mcp"
	@echo ""
	@echo "Samples:"
	@echo "  make samples    - Show sample file info"
	@echo "  make validate-samples - Validate all sample files"
	@echo "  make seed-samples     - Load samples into LocalStack"
	@echo "  make generate-samples - Generate new sample files"
	@echo ""
	@echo "Utility:"
	@echo "  make clean      - Remove build artifacts"

setup:
	./scripts/setup.sh

build:
	@echo "🏗️  Building TanaChat.ai components..."
	@echo "Building app (React app)..."
	cd app && npm run build
	@echo "Building api (Python package)..."
	cd api && uv build --wheel
	@echo "Building mcp (Python package)..."
	cd mcp && uv build --wheel
	@echo "✅ Build complete!"
	@echo ""
	@echo "Build artifacts:"
	@echo "  - app/dist/"
	@echo "  - api/dist/"
	@echo "  - mcp/dist/"

docker-build:
	@echo "🐳 Building TanaChat.ai Docker images..."
	docker-compose build

docker-run:
	@echo "🚀 Starting TanaChat.ai Docker services..."
	docker-compose up -d

docker-stop:
	@echo "🛑 Stopping Docker services..."
	docker-compose down

dev:
	./scripts/dev.sh

test:
	./scripts/test.sh

lint:
	./scripts/lint.sh

mcp-test:
	./scripts/mcp-test.sh

mcp-debug:
	./scripts/mcp-debug.sh

deploy-www:
	./scripts/deploy-www.sh

deploy-api:
	./scripts/deploy-api.sh

deploy-mcp:
	./scripts/deploy-mcp.sh

samples:
	@echo "📁 Sample Files Information:"
	@echo ""
	@echo "Valid TIF files:"
	@find samples/tana/imports/valid -name "*.json" -exec basename {} \;
	@echo ""
	@echo "Invalid TIF files (for error testing):"
	@find samples/tana/imports/invalid -name "*.json" -exec basename {} \;
	@echo ""
	@echo "API examples:"
	@find samples/api -name "*.json" -exec echo "  {}" \;
	@echo ""
	@echo "Total samples: $(find samples -name "*.json" -type f | wc -l | tr -d ' ')"

validate-samples:
	./scripts/validate-samples.sh

seed-samples:
	./scripts/seed-samples.sh

generate-samples:
	@echo "🏭 Generating sample Tana files..."
	python scripts/generate-samples.py --type small --count 20
	@echo ""
	@echo "Generated: samples/tana/imports/valid/generated-small.json"
	@echo ""
	@echo "To generate larger samples:"
	@echo "  python scripts/generate-samples.py --type medium"
	@echo "  python scripts/generate-samples.py --type large"

clean:
	rm -rf app/node_modules app/dist
	rm -rf api/.venv
	rm -rf mcp/.venv
	rm -rf temp/debug/* temp/reports/* temp/scratch/*
	rm -rf samples/tana/imports/valid/generated-*.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
