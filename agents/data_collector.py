import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import random
from urllib.parse import urljoin, urlparse

class DataCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_and_scrape(self, sub_query: str, max_sources: int = 3) -> List[Dict]:
        """
        Search and scrape 2-3 web sources for a sub-query
        """
        sources = self._search_sources(sub_query, max_sources)
        results = []
        
        for source in sources:
            try:
                content = self._scrape_content(source['url'])
                if content and len(content) > 300:  # Minimum content length
                    results.append({
                        'url': source['url'],
                        'title': source['title'],
                        'content': content[:1500]  # Limit content length
                    })
                # Rate limiting
                time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"Error scraping {source['url']}: {e}")
                continue
        
        return results
    
    def _search_sources(self, sub_query: str, max_sources: int) -> List[Dict]:
        """
        Search for sources related to the sub-query
        Using a simple approach with Google search URL (for demonstration)
        """
        # In a production environment, you might want to use a proper search API
        search_url = f"https://www.google.com/search?q={sub_query.replace(' ', '+')}&num={max_sources}"
        
        try:
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results (this is a simplified approach)
            results = []
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                if href.startswith('/url?q='):
                    # Extract actual URL from Google's redirect
                    url = href.split('/url?q=')[1].split('&')[0]
                    if self._is_valid_url(url):
                        results.append({
                            'url': url,
                            'title': link.get_text() or "No title"
                        })
                        
                        if len(results) >= max_sources:
                            break
            
            return results[:max_sources]
        except Exception as e:
            print(f"Error searching sources: {e}")
            return []
    
    def _scrape_content(self, url: str) -> str:
        """
        Scrape clean text content from a URL
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error scraping content from {url}: {e}")
            return ""
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid and scrapable
        """
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme) and 'google' not in parsed.netloc
        except:
            return False