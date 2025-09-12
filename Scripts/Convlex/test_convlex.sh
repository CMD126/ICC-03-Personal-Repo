#!/bin/bash

# Get the absolute path of the project root directory
PROJECT_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )

# The python script to test
PYTHON_SCRIPT="$PROJECT_ROOT/Scripts/Convlex/convlex.py"

# The URL of a sample PDF file for testing
PDF_URL="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# The expected output directory and file. Use a unique name to avoid clashes.
OUTPUT_DIR_NAME="test_pdf_output"
OUTPUT_DIR="$HOME/Documents/$OUTPUT_DIR_NAME"
OUTPUT_TXT_FILE="$OUTPUT_DIR/content.txt"
OUTPUT_PDF_FILE="$OUTPUT_DIR/content.pdf"

# Clean up any previous runs
rm -rf "$OUTPUT_DIR"

echo "Running convlex.py and expecting it to succeed..."
# Run the python script, piping the necessary inputs
printf "%s\n%s\n%s\n" "$PDF_URL" "$OUTPUT_DIR_NAME" "y" | python3 "$PYTHON_SCRIPT"

# Check if the output files were created and have the correct content
if [ -f "$OUTPUT_TXT_FILE" ] && [ -s "$OUTPUT_TXT_FILE" ] && \
   [ -f "$OUTPUT_PDF_FILE" ] && [ -s "$OUTPUT_PDF_FILE" ] && \
   grep -q "Dummy PDF file" "$OUTPUT_TXT_FILE"; then
    echo "TEST PASSED: The script ran successfully and created the expected output."
    EXIT_CODE=0
else
    echo "TEST FAILED: The script did not produce the expected output."
    if [ -f "$OUTPUT_TXT_FILE" ]; then
        echo "--- content.txt content ---"
        cat "$OUTPUT_TXT_FILE"
        echo "---------------------------"
    else
        echo "Output text file was not created."
    fi
    if [ ! -f "$OUTPUT_PDF_FILE" ]; then
        echo "Output pdf file was not created."
    fi
    EXIT_CODE=1
fi

# Clean up the output directory
rm -rf "$OUTPUT_DIR"

exit $EXIT_CODE
