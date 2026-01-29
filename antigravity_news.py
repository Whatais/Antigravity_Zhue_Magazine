import feedparser
import google.generativeai as genai
import os
from datetime import datetime

# --- CONFIGURATION ---
# Replace with your actual Google Gemini API Key
GEMINI_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"

# Output file name
OUTPUT_FILE = "Headlines_and_Titles.txt"

# Feed list extracted from your provided RSS.txt file 
RSS_FEEDS = [
    # US News
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://rss.cnn.com/rss/edition_world.rss",
    "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.nbcnews.com/nbcnews/public/news",
    "http://abcnews.go.com/abcnews/topstories",
    "https://www.cbsnews.com/latest/rss/main",
    "http://www.washingtonpost.com/rss/",
    "http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
    "http://www.npr.org/rss/rss.php?id=1001",
    "http://online.wsj.com/xml/rss/3_7085.xml",
    "http://www.politico.com/rss/politicopicks.xml",
    "https://news.yahoo.com/rss/mostviewed",
    
    # Europe/UK
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://feeds.reuters.com/reuters/EuropeNews",
    "https://www.theguardian.com/world/rss",
    "https://www.dailymail.co.uk/home/index.rss",
    "http://www.independent.co.uk/news/uk/rss",
    "https://feeds.thelocal.com/rss/es",
    "https://eureporter.co/feed",
    
    # Technology
    "http://feeds.wired.com/wired/index",
    "https://www.theverge.com/rss/index.xml",
    "https://techcrunch.com/region/europe/feed",
    "https://news.ycombinator.com/rss",
    "http://feeds.arstechnica.com/arstechnica/index",
    "https://gizmodo.com/rss",
    "https://9to5mac.com/feed",
    "https://www.engadget.com/rss.xml"
]

def fetch_rss_data(feeds):
    """
    Reads all RSS feeds and collects the latest headlines.
    Limiting to top 2 items per feed to avoid overloading the context window.
    """
    print(f"📡 Scanning {len(feeds)} global feeds...")
    aggregated_news = []
    
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            # Grab the first 2 entries from each feed to ensure freshness
            for entry in feed.entries[:2]:
                title = entry.get('title', 'No Title')
                # minimal cleaning to remove potential CDATA tags mentioned in source [cite: 15]
                clean_title = title.replace("<![CDATA[", "").replace("]]>", "")
                source = feed.feed.get('title', 'Unknown Source')
                aggregated_news.append(f"- [{source}] {clean_title}")
        except Exception as e:
            print(f"⚠️ Could not read {url}: {e}")
            continue
            
    return "\n".join(aggregated_news)

def generate_curated_headlines(news_data):
    """
    Sends the raw news to Gemini to select the top 5 and rewrite them.
    """
    print("🧠 Processing with Gemini AI...")
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Using the latest efficient model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an elite news editor.
    
    INPUT DATA:
    {news_data}
    
    INSTRUCTIONS:
    1. Analyze the news list above and select the **5 most important** global stories.
    2. Ensure there is **NO repetition** of topics (e.g., if two sources cover the same election, pick only one).
    3. For each selected story, you must rewrite the metadata strictly as follows:
       - **Headline:** Must be strictly ALL UPPERCASE. It must be a new, punchy summary (different from the original).
       - **Sub-headline:** Must be in Title Case (Capitalize Major Words). It must be a new context sentence.
    
    OUTPUT FORMAT (Strictly text, no markdown code blocks):
    [STORY 1]
    HEADLINE: [YOUR ALL CAPS HEADLINE]
    Sub-headline: [Your Title Case Sub-headline]

    [STORY 2]
    HEADLINE: [YOUR ALL CAPS HEADLINE]
    Sub-headline: [Your Title Case Sub-headline]
    
    ...and so on for 5 stories.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

def save_to_file(content):
    """
    Overwrites the content to the specified file.
    """
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Success! Content written to '{OUTPUT_FILE}'")
        print("-" * 30)
        print(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Read RSS
    raw_news = fetch_rss_data(RSS_FEEDS)
    
    if not raw_news:
        print("❌ No news data found. Check internet connection.")
    else:
        # 2, 3, 4. Select & Create Headlines/Subheadlines (via AI)
        ai_output = generate_curated_headlines(raw_news)
        
        # 5. Add to file (Overwrite)
        save_to_file(ai_output)
