#!/bin/bash

# This script performs an automated test for the `convlex.py` script.
# It verifies that the script can correctly download a PDF, convert it to text,
# and save both the text and PDF files.

# --- Test Configuration ---

# Determine the absolute path of the project's root directory.
# This makes the script runnable from any location.
PROJECT_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." &> /dev/null && pwd)

# Define the path to the Python script that will be tested.
PYTHON_SCRIPT="$PROJECT_ROOT/Scripts/Convlex/convlex.py"

# URL of a sample PDF file used for the test.
PDF_URL="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# Define the name and path for the output directory and files.
# A unique name is used to prevent conflicts with existing directories.
OUTPUT_DIR_NAME="test_pdf_output_$$" # Using $$ adds the process ID for uniqueness.
OUTPUT_DIR="$HOME/Documents/$OUTPUT_DIR_NAME"
OUTPUT_TXT_FILE="$OUTPUT_DIR/content.txt"
OUTPUT_PDF_FILE="$OUTPUT_DIR/content.pdf"

# --- Test Execution ---

# Ensure a clean slate by removing any output from previous test runs.
echo "Cleaning up previous test runs (if any)..."
rm -rf "$OUTPUT_DIR"

echo "Running test: convlex.py with a sample PDF..."
# Execute the python script and provide automated input via a pipe.
# 1. The PDF URL.
# 2. The custom directory name for the output.
# 3. 'y' to confirm saving the PDF version.
printf "%s\n%s\n%s\n" "$PDF_URL" "$OUTPUT_DIR_NAME" "y" | python3 "$PYTHON_SCRIPT"

# --- Verification ---

# Check if the test was successful by verifying the output.
# - The text file exists and is not empty.
# - The PDF file exists and is not empty.
# - The text file contains the expected content ("Dummy PDF file").
if [ -f "$OUTPUT_TXT_FILE" ] && [ -s "$OUTPUT_TXT_FILE" ] && \
   [ -f "$OUTPUT_PDF_FILE" ] && [ -s "$OUTPUT_PDF_FILE" ] && \
   grep -q "Dummy PDF file" "$OUTPUT_TXT_FILE"; then
    echo "✅ TEST PASSED: The script successfully created and populated the output files."
    EXIT_CODE=0
else
    # If the test fails, print detailed error messages.
    echo "❌ TEST FAILED: The script did not produce the expected output."
    [ ! -f "$OUTPUT_TXT_FILE" ] && echo "  - Reason: Output text file was not created."
    [ -f "$OUTPUT_TXT_FILE" ] && [ ! -s "$OUTPUT_TXT_FILE" ] && echo "  - Reason: Output text file is empty."
    [ ! -f "$OUTPUT_PDF_FILE" ] && echo "  - Reason: Output PDF file was not created."
    [ -f "$OUTPUT_PDF_FILE" ] && [ ! -s "$OUTPUT_PDF_FILE" ] && echo "  - Reason: Output PDF file is empty."
    grep -q "Dummy PDF file" "$OUTPUT_TXT_FILE" || echo "  - Reason: Text content does not match expected."

    # Display the content of the text file for debugging.
    if [ -f "$OUTPUT_TXT_FILE" ]; then
        echo "--- content.txt ---"
        cat "$OUTPUT_TXT_FILE"
        echo "-------------------"
    fi
    EXIT_CODE=1
fi

# --- Cleanup ---

# Remove the created output directory and its contents.
echo "Cleaning up test artifacts..."
rm -rf "$OUTPUT_DIR"

# Exit with a status code indicating success or failure.
exit $EXIT_CODE
