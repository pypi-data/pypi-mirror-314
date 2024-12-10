#!/bin/bash

#  Usage Example:
#  ./run_k6_tests.sh
 
# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo "k6 could not be found. Please install k6 and try again."
    exit 1
fi

# Define the k6 script to run
K6_SCRIPT="k6_loadtest.js"

# Check if the script exists
if [ ! -f "$K6_SCRIPT" ]; then
    echo "k6 script '$K6_SCRIPT' does not exist in the current directory."
    exit 1
fi

# Define the test configurations as an array of strings
TEST_CONFIGS=(
    # ""                      # Default run
    "K6_VUS=1 K6_DURATION=1m"
    "K6_VUS=1 K6_DURATION=5m"
    "K6_VUS=1 K6_DURATION=10m"
    "K6_VUS=5 K6_DURATION=1m"
    "K6_VUS=5 K6_DURATION=5m"        
    "K6_VUS=5 K6_DURATION=10m"
    "K6_VUS=10 K6_DURATION=1m"
    "K6_VUS=10 K6_DURATION=5m"
    "K6_VUS=10 K6_DURATION=10m"
)

# TEST_CONFIGS=(
#     # ""                      # Default run
#     "K6_VUS=1 K6_DURATION=15s"
#     "K6_VUS=10 K6_DURATION=15s"
#     "K6_VUS=100 K6_DURATION=15s"
#     "K6_VUS=1 K6_DURATION=1m"
#     "K6_VUS=10 K6_DURATION=1m"
#     "K6_VUS=100 K6_DURATION=1m"    
# )

# Run the tests
STEP=1
for CONFIG in "${TEST_CONFIGS[@]}"; do
    echo "Pausing for 120 seconds before running Step $STEP..."
    sleep 120

    echo "Running Step $STEP with configuration: ${CONFIG:-default}"
    if [ -n "$CONFIG" ]; then
        eval "$CONFIG k6 run \"$K6_SCRIPT\""
    else
        k6 run "$K6_SCRIPT"
    fi

    if [ $? -ne 0 ]; then
        echo "Step $STEP failed. Exiting."
        exit 1
    fi
    echo "Step $STEP completed successfully."
    STEP=$((STEP + 1))
done

echo "All steps completed successfully."

afplay /System/Library/Sounds/Glass.aiff

echo "Script finished running. 🎉"
