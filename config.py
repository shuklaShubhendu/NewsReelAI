import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
# Load Groq API Key (REQUIRED for script generation)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found in .env file. Get one from https://console.groq.com/keys")
    # exit() # Uncomment to force exit if key is missing

# --- News Sources ---
# Using RSS feeds is generally more reliable than scraping websites directly
RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.thehindu.com/feeder/default.ece",
    "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
    # Add more feeds relevant to your target topics (Indian sources recommended)
]

# --- Video Parameters ---
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_FPS = 24
TARGET_VIDEO_DURATION_SECONDS = 45 # Aim for roughly this duration
MIN_SCENES = 4
MAX_SCENES = 8 # Controls complexity and fits duration target
MAX_OVERLAY_WORDS = 15 # Max words per text overlay
OUTPUT_FOLDER = "assets/output_videos"
TEMP_IMAGE_FOLDER = "assets/temp_images"
TEMP_AUDIO_FOLDER="assets/temp_audio"
BACKGROUND_MUSIC_FILE = "assets/background_music.mp3" # Make sure this file exists

# --- LLM Configuration ---
# Select a Groq model (check https://console.groq.com/docs/models for options)
# llama3-8b-8192 is fast and capable for summarization
LLM_MODEL_NAME = "llama3-8b-8192"
# Other options: "mixtral-8x7b-32768", "llama3-70b-8192", "gemma-7b-it"

# --- Image Generation (Placeholder - Modify if using a specific API) ---
# Set to True if you implement actual image generation in video_creator.py
USE_AI_IMAGE_GENERATION = True
PLACEHOLDER_IMAGE = "assets/placeholder.png" # Create a simple placeholder image file

# Create necessary directories if they don't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_IMAGE_FOLDER, exist_ok=True)
# Create placeholder image if needed
if not os.path.exists(PLACEHOLDER_IMAGE) and not USE_AI_IMAGE_GENERATION:
     print(f"Warning: Placeholder image '{PLACEHOLDER_IMAGE}' not found.")
     try:
         from PIL import Image, ImageDraw, ImageFont
         img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color = (120, 120, 120))
         d = ImageDraw.Draw(img)
         try:
            # Attempt to load a common font
            font = ImageFont.truetype("arial.ttf", 40)
         except IOError:
            # Use default font if Arial not found
            font = ImageFont.load_default()
         d.text((VIDEO_WIDTH//4, VIDEO_HEIGHT//2), "Placeholder Image", fill=(255,255,0), font=font, anchor="mm")
         img.save(PLACEHOLDER_IMAGE)
         print(f"Created a simple {PLACEHOLDER_IMAGE}")
     except ImportError:
         print("Pillow not installed, cannot create placeholder image automatically.")
     except Exception as e:
         print(f"Could not create placeholder image: {e}")


# --- Legal/Ethical Reminder ---
# Remember copyright laws (Indian Copyright Act, 1957) regarding scraping/using news content.
# Be mindful of potential misinformation (Indian IT Rules, 2021). Review generated content.

