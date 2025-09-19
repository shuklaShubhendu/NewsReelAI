# advanced_script_generator.py
import logging
import json
from typing import List, Dict, Optional

from groq import Groq, APIError, RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import config

# --- Setup Advanced Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class VideoScriptGenerator:
    """
    A robust class to generate video scripts from articles using the Groq API.

    Features:
    - Manages a single Groq client instance.
    - Uses tenacity for automatic, exponential backoff retries on failures.
    - Implements structured logging for better diagnostics.
    - Centralizes configuration for easy management.
    - Provides detailed error handling and response validation.
    """
    def __init__(self):
        """Initializes the generator and the Groq client."""
        if not config.GROQ_API_KEY:
            logging.error("GROQ_API_KEY not found in environment variables or .env file.")
            raise ValueError("Groq API Key is not configured.")
        
        try:
            self.client = Groq(api_key=config.GROQ_API_KEY)
            logging.info(f"Groq client initialized for model: {config.LLM_MODEL_NAME}")
        except Exception as e:
            logging.error(f"Failed to initialize Groq client: {e}")
            raise

    def _parse_and_validate_response(self, response_text: str) -> Optional[List[Dict[str, str]]]:
        """Cleans, parses, and validates the JSON response from the LLM."""
        try:
            # Clean the response text (remove markdown fences if they exist)
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            script_data = json.loads(cleaned_text)

            # Validate the structure
            if not isinstance(script_data, list):
                logging.warning("LLM response was not a JSON list.")
                return None

            valid_scenes = []
            for i, scene in enumerate(script_data):
                if isinstance(scene, dict) and 'scene_description' in scene and 'overlay_text' in scene:
                    valid_scenes.append(scene)
                else:
                    logging.warning(f"Skipping invalid scene structure at index {i}: {scene}")
            
            if not valid_scenes:
                logging.warning("No valid scenes found after validation.")
                return None
                
            return valid_scenes

        except json.JSONDecodeError:
            logging.error("Failed to decode JSON from LLM response.", exc_info=True)
            logging.debug(f"Raw LLM response was:\n---\n{response_text}\n---")
            return None
        except Exception:
            logging.error("An unexpected error occurred during response validation.", exc_info=True)
            return None

    @retry(
        wait=wait_exponential(min=config.RETRY_MIN_WAIT_SECONDS, max=config.RETRY_MAX_WAIT_SECONDS),
        stop=stop_after_attempt(config.RETRY_MAX_ATTEMPTS),
        retry=retry_if_exception_type((APIError, RateLimitError)),
        before_sleep=lambda retry_state: logging.warning(
            f"Retrying API call... (Attempt #{retry_state.attempt_number})"
        )
    )
    def generate_script(self, article_title: str, article_content: str) -> Optional[List[Dict[str, str]]]:
        """
        Generates and validates a video script from article text.

        This method automatically retries on transient API errors.
        """
        if not article_content or not article_title:
            logging.warning("Attempted to generate a script with empty title or content.")
            return None

        logging.info(f"Generating script for article: '{article_title}'")
        
        full_context = f"Title: {article_title}\n\nContent: {article_content}"

        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT_TEMPLATE},
            {"role": "user", "content": f"Article Content:\n---\n{full_context[:15000]}\n---"}
        ]

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=config.LLM_MODEL_NAME,
                temperature=0.5,
                max_tokens=2048,
                response_format={"type": "json_object"}, # More reliable JSON output
            )
            response_text = chat_completion.choices[0].message.content
            
            validated_script = self._parse_and_validate_response(response_text)
            
            if validated_script:
                logging.info(f"Successfully generated script with {len(validated_script)} scenes.")
            else:
                logging.error("Failed to generate a valid script after processing the response.")

            return validated_script

        except RateLimitError as e:
            logging.error(f"Rate limit exceeded. Details: {e.body}")
            raise  # Re-raise to trigger tenacity retry
        except APIError as e:
            logging.error(f"An API error occurred. Status code: {e.status_code}. Details: {e.body}")
            raise  # Re-raise to trigger tenacity retry
        except Exception as e:
            logging.critical(f"An unhandled exception occurred during script generation: {e}", exc_info=True)
            return None


if __name__ == "__main__":
    test_title = "Global Tech Stocks Surge After Landmark AI Announcement"
    test_content = """
    Major technology stocks experienced a significant rally today following the announcement of a groundbreaking
    AI platform by industry leader, InnovateCorp. The Dow Jones Industrial Average climbed 2%, while the
    tech-heavy NASDAQ composite jumped over 4.5%.

    InnovateCorp's new platform, named 'Prometheus', promises to accelerate machine learning model
    development by an order of magnitude. CEO Jane Doe stated in a press conference that "Prometheus will
    democratize access to state-of-the-art AI, empowering developers worldwide."

    Analysts are optimistic, but some express caution about potential regulatory hurdles and the
    long-term profitability of such a complex system. The platform is scheduled for a limited beta
    release in the fourth quarter.
    """
    
    try:
        generator = VideoScriptGenerator()
        script = generator.generate_script(test_title, test_content)

        if script:
            print("\n--- Generated Video Script ---")
            print(json.dumps(script, indent=2))
            print("----------------------------\n")
        else:
            print("\n--- Failed to generate a valid video script. Check logs for details. ---\n")

    except ValueError as e:
        print(f"\nConfiguration Error: {e}\n")
    except Exception as e:
        print(f"\nA critical error occurred: {e}\n")
