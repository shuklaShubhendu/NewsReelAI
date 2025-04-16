import time
import os
import re # For cleaning filenames
import config # Project settings
import news_fetcher
import script_generator
import video_creator

def sanitize_filename(filename):
    """Removes invalid characters for filenames."""
    # Remove non-alphanumeric characters (except hyphen and underscore)
    sanitized = re.sub(r'[^\w\-]+', '_', filename)
    # Replace multiple underscores with single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Limit length
    return sanitized[:50] # Limit filename length

def main():
    print("--- Starting AI Video Generation Pipeline ---")
    start_time = time.time()

    # 1. Fetch Trending News
    print("\nStep 1: Fetching trending news articles...")
    try:
        articles = news_fetcher.fetch_trending_rss(limit=5) # Fetch top 5 potential articles
        if not articles:
            print("Error: No articles fetched. Exiting.")
            return
        # Select the first article for this run
        selected_article = articles[0]
        print(f"Selected article: '{selected_article['title']}'")
        print(f"Source Feed: {selected_article['source_feed']}")
        # Prioritize using the RSS summary as it's more reliable than full scraping
        content_to_summarize = selected_article.get('summary', selected_article.get('title'))
        if len(content_to_summarize) < 100: # If summary is too short, try scraping (less reliable)
             print("Warning: RSS summary is short. Attempting to fetch full content (may fail)...")
             full_text = news_fetcher.fetch_article_content_from_link(selected_article['link'])
             if full_text:
                  content_to_summarize = full_text
                  print("Using fetched full article content.")
             else:
                  print("Warning: Failed to fetch full content. Using short RSS summary.")

    except Exception as e:
        print(f"Error during news fetching: {e}")
        return

    # 2. Generate Script
    print("\nStep 2: Generating script using AI...")
    try:
        script_data = script_generator.generate_script(selected_article['title'], content_to_summarize)
        if not script_data:
            print("Error: Failed to generate script. Exiting.")
            return
        print(f"Generated script with {len(script_data)} scenes.")
        # Optional: Print generated script for debugging
        # import json
        # print("--- Generated Script ---")
        # print(json.dumps(script_data, indent=2))
        # print("------------------------")

    except Exception as e:
        print(f"Error during script generation: {e}")
        return

    # 3. Create Video
    print("\nStep 3: Creating video from script...")
    try:
        # Create a somewhat unique and valid filename from the title
        base_filename = sanitize_filename(selected_article['title'])
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename_base = f"{base_filename}_{timestamp}"

        video_path = video_creator.create_video_from_script(script_data, output_filename_base)
        if not video_path:
            print("Error: Video creation failed.")
            return
        print(f"\nSuccess! Video saved to: {video_path}")

    except Exception as e:
        print(f"Error during video creation: {e}")
        return

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\n--- Pipeline Finished ---")
    print(f"Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    main()