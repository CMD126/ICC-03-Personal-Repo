"""
MIT License

Copyright (c) 2025 LexLucas CMD126

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import necessary libraries
# os: For handling file paths and directories
# re: For regular expressions
# urllib.parse: For parsing URLs
# requests: For making HTTP requests
# BeautifulSoup from bs4: For parsing HTML and extracting text
# weasyprint: For creating PDFs from HTML
# pypdf: For extracting text from PDFs
import os
import re
import tempfile
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from pypdf import PdfReader

# Note: Install: pip install requests beautifulsoup4 weasyprint pypdf

# Headers to mimic browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Function to get a default directory name from the URL
# Default: Last path segment or domain without 'www.'
def get_dir_name(url):
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if path:
        name = path.split('/')[-1]
        if name:
            return name
    return parsed.netloc.replace('www.', '')

# Function to check if URL is Google Doc and extract ID
def get_google_doc_id(url):
    match = re.search(r'docs\.google\.com/document/d/([^/]+)', url)
    if match:
        return match.group(1)
    return None

# Ask for URLs
links_input = input("Enter URLs (comma-separated): ")
links = [link.strip() for link in links_input.split(',') if link.strip()]

contents = {}

docs = os.path.expanduser("~/Documents")
# Default base directory: ~/Documents/web_contents if multiple links, else ~/Documents
base_dir = os.path.join(docs, "web_contents") if len(links) > 1 else docs
if len(links) > 1:
    os.makedirs(base_dir, exist_ok=True)

for link in links:
    default_dir = get_dir_name(link)
    # Allow rename: Ask for custom directory name, default to URL-based
    custom_dir = input(f"Enter custom dir name for {link} (default: {default_dir}): ").strip() or default_dir
    doc_id = get_google_doc_id(link)
    if doc_id:
        # Handle Google Doc
        try:
            # For PDF
            pdf_url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"
            resp_pdf = requests.get(pdf_url, headers=headers)
            is_pdf = resp_pdf.ok and 'application/pdf' in resp_pdf.headers.get('Content-Type', '').lower()
            resp = resp_pdf if is_pdf else None

            # For text: try export txt
            text = "Error extracting text."
            txt_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
            resp_txt = requests.get(txt_url, headers=headers)
            if resp_txt.ok:
                text = resp_txt.text
            elif is_pdf:
                # Fallback: extract from PDF
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_f:
                    temp_f.write(resp_pdf.content)
                    temp_f.seek(0)
                    reader = PdfReader(temp_f)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text() + '\n'
        except Exception as e:
            text = f"Error: {e}"
            is_pdf = False
            resp = None
        is_html = False
        content_type = 'google/doc'
    else:
        # Handle general case
        try:
            resp = requests.get(link, headers=headers)
            content_type = resp.headers.get('Content-Type', '').lower()
            
            if 'text/html' in content_type:
                soup = BeautifulSoup(resp.text, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                is_html = True
                is_pdf = False
            elif 'application/pdf' in content_type:
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_f:
                    temp_f.write(resp.content)
                    temp_f.seek(0)
                    reader = PdfReader(temp_f)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text() + '\n'
                is_html = False
                is_pdf = True
            else:
                text = f"Unsupported content type: {content_type}"
                is_html = False
                is_pdf = False
        except Exception as e:
            text = f"Error: {e}"
            resp = None
            is_html = False
            is_pdf = False
            content_type = ''

    dir_name = custom_dir
    full_dir = os.path.join(base_dir, dir_name) if len(links) > 1 else os.path.join(base_dir, dir_name)
    os.makedirs(full_dir, exist_ok=True)
    
    # Default file names: content.txt and content.pdf
    txt_name = 'content.txt'
    txt_path = os.path.join(full_dir, txt_name)
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    contents[link] = (txt_path, text, resp, is_html, is_pdf, content_type)
    
    print(f"Saved {txt_path}")

# Default: Ask to save PDF
save_pdf = input("Save as PDF also? (y/n): ").lower() == 'y'

if save_pdf:
    for link, (txt_path, text, resp, is_html, is_pdf, content_type) in contents.items():
        if resp is None and not is_pdf:
            continue
        
        dir_name = os.path.basename(os.path.dirname(txt_path))
        pdf_dir = os.path.join(base_dir, dir_name) if len(links) > 1 else os.path.join(base_dir, dir_name)
        
        pdf_name = os.path.join(pdf_dir, 'content.pdf')
        
        if is_html:
            HTML(string=resp.text, base_url=link).write_pdf(pdf_name)
        elif is_pdf or 'google/doc' in content_type:
            with open(pdf_name, 'wb') as f:
                f.write(resp.content)
        
        if os.path.exists(pdf_name):
            print(f"Saved {pdf_name}")

# This script's purpose is to be merely a docs converter to streamline the data collection process by minimizing distractions.