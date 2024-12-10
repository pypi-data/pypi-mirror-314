# Define variables
CARGO = cargo
PACKAGE_NAME = genius-agent-factor-graph

# Phony targets to prevent confusion with files of the same name
.PHONY: all build test lint fmt check bench clean doc

# Default target: build the project
all: build

# Build the library in release mode
build:
	@echo "Building the library..."
	$(CARGO) build --release

# Run all tests, including unit and integration tests
test:
	@echo "Running tests..."
	$(CARGO) test-all-features --features json

# Run clippy for linting
lint:
	@echo "Running clippy linter..."
	$(CARGO) clippy --all-targets --all-features -- -D warnings

# Run rustfmt to ensure consistent formatting
fmt:
	@echo "Formatting code..."
	$(CARGO) fmt --all

# Check for code issues without actually building or testing
check:
	@echo "Running cargo check..."
	$(CARGO) check

# Run benchmarks if the project has them
bench:
	@echo "Running benchmarks..."
	$(CARGO) bench

# Clean the project (remove build artifacts)
clean:
	@echo "Cleaning up..."
	$(CARGO) clean

# Generate documentation for the project
doc:
	@echo "Generating documentation..."
	$(CARGO) doc --open

# Catch-all target to perform all quality checks
ci: fmt check test
	@echo "Running all CI checks (format, check, and test)..."

# Run examples/usage.rs
example:
	@echo "Running example..."
	$(CARGO) run --example usage --features json