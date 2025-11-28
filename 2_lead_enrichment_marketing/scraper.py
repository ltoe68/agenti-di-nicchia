import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

def find_website(company_name):
    """Searches Google for the company website."""
    try:
        query = f"{company_name} official website"
        # Get the first result
        for url in search(query, num_results=1):
            return url
    except Exception as e:
        print(f"Error searching for {company_name}: {e}")
        return None

def scrape_website(url):
    """Scrapes text content from the given URL."""
    if not url:
        return ""
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate to avoid token limits (approx 4000 chars)
        return text[:4000]
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""
