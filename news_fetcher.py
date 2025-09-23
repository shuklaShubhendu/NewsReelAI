import feedparser
import requests
from bs4 import BeautifulSoup
import config # Use config.py for settings
#using confid is a good option always
def fetch_trending_rss(limit=5):
    """Fetches latest news entries from configured RSS feeds."""
    print(f"Fetching news from {len(config.RSS_FEEDS)} RSS feed(s)...")
    articles = []
    for url in config.RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            # Add entries, prioritizing those with summaries
            for entry in feed.entries[:limit]:
                 # Basic check for content
                content = entry.get('summary', entry.get('title', 'No content'))
                # Simple filter to avoid empty entries
                if entry.get('title') and entry.get('link') and len(content) > 50:
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', 'Summary not available'), # Use summary if available
                        'published': entry.get('published', 'Date not available'),
                        'source_feed': url
                    })
        except Exception as e:
            print(f"Warning: Could not fetch or parse feed {url}: {e}")

    # Simple sort by published date if available (best effort)  nice and understandbke
    try:
        articles.sort(key=lambda x: feedparser._parse_date(x['published']), reverse=True)
    except Exception:
        print("Warning: Could not sort articles by date.")
        # Proceed without date sorting if parsing fails

    print(f"Found {len(articles)} potential articles.")
    return articles[:limit] # Return the top 'limit' articles overall

def fetch_article_content_from_link(url):
    """
    Attempts to fetch full article text from a URL.
    NOTE: This is fragile and likely to break as website layouts change.
          Requires specific parsing logic for each site.
          Using RSS summaries is often more reliable for quick prototypes.
    """
    print(f"Attempting to fetch full content from: {url} (This is often unreliable)")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'} # Be a polite scraper
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an error for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- !!! THIS IS THE FRAGILE PART !!! ---
        # You MUST inspect the HTML structure of target sites and adapt this logic.
        # Common patterns: look for <article>, <main>, divs with class="content", "article-body", etc.
        # Example (very generic, likely needs adjustment):
        article_body = soup.find('article') or soup.find('main') or soup.find('div', class_='article-body') # Add more specific selectors
        if article_body:
            paragraphs = article_body.find_all('p')
            full_text = "\n".join([p.get_text() for p in paragraphs])
            if len(full_text) > 200: # Basic check if we got substantial text
                 print("Successfully fetched some article text.")
                 return full_text
            else:
                 print("Warning: Found article container, but text seems short.")
                 return None # Indicate failure to get substantial text
        else:
            print("Warning: Could not find a main article container using common tags.")
            return None # Indicate failure

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing content from {url}: {e}")
        return None

# Example usage (optional, can be run directly for testing)
if __name__ == "__main__":
    top_articles = fetch_trending_rss(limit=3)
    if top_articles:
        print("\nLatest Articles from RSS:")
        for i, article in enumerate(top_articles):
            print(f"{i+1}. {article['title']} ({article['published']})")
            print(f"   Link: {article['link']}")
            print(f"   Summary: {article['summary'][:150]}...") # Print start of summary

        # Example trying to fetch full text (use with caution)
        # selected_article_url = top_articles[0]['link']
        # full_text = fetch_article_content_from_link(selected_article_url)
        # if full_text:
        #     print("\nFetched Full Text (first 500 chars):")
        #     print(full_text[:500] + "...")
        # else:
        #      print(f"\nUsing RSS summary for {top_articles[0]['title']} as full text fetch failed.")
        #      print(top_articles[0]['summary'])
    else:
        print("No articles fetched.")
