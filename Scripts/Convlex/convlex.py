# MIT License
#
# Copyright (c) 2025 LexLucas CMD126
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Import necessary libraries for file handling, web requests, and data parsing.
import os  # For interacting with the operating system, like creating directories.
import re  # For regular expression matching to find Google Doc IDs.
import tempfile  # To create temporary files for processing PDFs.
from urllib.parse import urlparse  # To break down URLs into their components.
import requests  # To send HTTP requests to fetch web content.
from bs4 import BeautifulSoup  # To parse HTML and extract text content.
from weasyprint import HTML  # To convert HTML content into PDF files.
from pypdf import PdfReader  # To read and extract text from PDF files.

# Installation command for required packages:
# pip install requests beautifulsoup4 weasyprint pypdf

# Define headers to mimic a web browser, which can help avoid being blocked by websites.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_dir_name(url):
    """
    Generate a default directory name from a URL.
    It uses the last part of the URL's path or the domain name as a fallback.
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if path:
            # Take the last segment of the path.
            name = path.split('/')[-1]
            if name:
                return name
        # If no path, use the domain name, removing 'www.'
        return parsed.netloc.replace('www.', '')
    except Exception:
        # Fallback for invalid URLs.
        return "default_document"

def get_google_doc_id(url):
    """
    Extract the document ID from a Google Docs URL using regular expressions.
    """
    match = re.search(r'docs\.google\.com/document/d/([^/]+)', url)
    return match.group(1) if match else None

# --- Main Script Logic ---

# 1. Get URLs from the user.
links_input = input("Enter one or more URLs, separated by commas: ")
# Split the input string into a list of cleaned-up URLs.
links = [link.strip() for link in links_input.split(',') if link.strip()]

# A dictionary to store the processing results for each link.
contents = {}

# Determine the base directory for saving files.
# Default to '~/Documents'. If multiple links, use a subdirectory 'web_contents'.
docs_path = os.path.expanduser("~/Documents")
if len(links) > 1:
    base_dir = os.path.join(docs_path, "web_contents")
    os.makedirs(base_dir, exist_ok=True)  # Create the directory if it doesn't exist.
else:
    base_dir = docs_path

# 2. Process each URL.
for link in links:
    # Generate a default directory name and ask the user for a custom one.
    default_dir = get_dir_name(link)
    custom_dir_prompt = f"Enter a directory name for '{link}' (or press Enter to use '{default_dir}'): "
    custom_dir = input(custom_dir_prompt).strip() or default_dir

    # Check if the link is a Google Doc.
    doc_id = get_google_doc_id(link)
    if doc_id:
        # --- Handle Google Docs ---
        try:
            # Attempt to download the document as a PDF.
            pdf_url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"
            resp_pdf = requests.get(pdf_url, headers=headers)
            is_pdf = resp_pdf.ok and 'application/pdf' in resp_pdf.headers.get('Content-Type', '').lower()
            resp = resp_pdf if is_pdf else None

            # Attempt to download the document as plain text.
            text = "Error: Could not extract text."
            txt_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
            resp_txt = requests.get(txt_url, headers=headers)
            if resp_txt.ok:
                text = resp_txt.text
            elif is_pdf:
                # If text export fails but PDF download worked, extract text from the PDF.
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_f:
                    temp_f.write(resp_pdf.content)
                    temp_f_path = temp_f.name

                reader = PdfReader(temp_f_path)
                text = "".join(page.extract_text() + "\n" for page in reader.pages)
                os.remove(temp_f_path)  # Clean up the temporary file.
        except Exception as e:
            text = f"An error occurred: {e}"
            is_pdf = False
            resp = None

        is_html = False
        content_type = 'google/doc'
    else:
        # --- Handle other URLs (HTML, PDF) ---
        try:
            resp = requests.get(link, headers=headers, timeout=10)
            content_type = resp.headers.get('Content-Type', '').lower()

            if 'text/html' in content_type:
                # For HTML, parse the content and extract clean text.
                soup = BeautifulSoup(resp.text, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                is_html = True
                is_pdf = False
            elif 'application/pdf' in content_type:
                # For PDF, extract text using a temporary file.
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_f:
                    temp_f.write(resp.content)
                    temp_f_path = temp_f.name

                reader = PdfReader(temp_f_path)
                text = "".join(page.extract_text() + "\n" for page in reader.pages)
                os.remove(temp_f_path)
                is_html = False
                is_pdf = True
            else:
                text = f"Unsupported content type: {content_type}"
                is_html = is_pdf = False
        except requests.exceptions.RequestException as e:
            text = f"Failed to retrieve URL: {e}"
            resp = None
            is_html = is_pdf = False
            content_type = ''

    # 3. Save the extracted text to a file.
    # Create the final directory for the output.
    full_dir = os.path.join(base_dir, custom_dir)
    os.makedirs(full_dir, exist_ok=True)
    
    # Define the output file path.
    txt_path = os.path.join(full_dir, 'content.txt')
    
    # Write the extracted text to the file.
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # Store the results for this link.
    contents[link] = (txt_path, text, resp, is_html, is_pdf, content_type)
    print(f"Text content saved to: {txt_path}")

# 4. Ask the user if they want to save PDFs.
save_pdf_choice = input("Would you like to save PDF versions as well? (y/n): ").lower()

if save_pdf_choice == 'y':
    for link, (txt_path, text, resp, is_html, is_pdf, content_type) in contents.items():
        # Skip if there's no response object to get PDF content from.
        if resp is None:
            continue
        
        # Determine the directory for the PDF file.
        pdf_dir = os.path.dirname(txt_path)
        pdf_path = os.path.join(pdf_dir, 'content.pdf')
        
        try:
            if is_html:
                # Convert HTML to PDF.
                HTML(string=resp.text, base_url=link).write_pdf(pdf_path)
            elif is_pdf or 'google/doc' in content_type:
                # Save the downloaded PDF content directly.
                with open(pdf_path, 'wb') as f:
                    f.write(resp.content)

            if os.path.exists(pdf_path):
                print(f"PDF saved to: {pdf_path}")
        except Exception as e:
            print(f"Could not save PDF for {link}. Reason: {e}")

print("\nScript finished. All requested documents have been processed.")
# This script is designed to simplify data collection by converting web documents into standard formats.