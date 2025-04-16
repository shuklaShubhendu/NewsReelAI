from groq import Groq # Import Groq client
import config
import json
import os

def configure_llm():
    """Configures the Groq client."""
    if not config.GROQ_API_KEY:
        print("Error: Groq API Key not configured in config.py or .env file.")
        return None
    try:
        # Initialize Groq client
        client = Groq(api_key=config.GROQ_API_KEY)
        print(f"Groq client configured successfully for model: {config.LLM_MODEL_NAME}")
        return client
    except Exception as e:
        print(f"Error configuring Groq client: {e}")
        return None

def generate_script(article_title, article_content):
    """Generates a video script from article text using Groq."""
    client = configure_llm()
    if not client:
        return None

    print(f"Generating script with Groq model: {config.LLM_MODEL_NAME}...")

    # Combine title and content for context
    full_context = f"Title: {article_title}\n\nContent: {article_content}"

    # Construct the messages list for the chat API
    messages = [
        {
            "role": "system",
            "content": f"""
Analyze the following news article content (including the title).
Summarize the absolute key points into a script for a short video (around {config.TARGET_VIDEO_DURATION_SECONDS} seconds).
Structure the output STRICTLY as a JSON list of 'scenes'. Aim for {config.MIN_SCENES} to {config.MAX_SCENES} scenes.
Each scene object in the JSON list MUST have ONLY these two keys:
1.  "scene_description": A very brief visual concept (3-5 words max, e.g., "Global stock market chart", "Politician speaking at podium", "Flooded street view"). This will guide image generation.
2.  "overlay_text": The exact text (max {config.MAX_OVERLAY_WORDS} words) to display on screen for this scene. This text must be factual based *only* on the provided article content.

Keep the tone neutral and strictly factual, based ONLY on the text provided below.
Do not add any information not present in the text.
Do not include introductory or concluding remarks outside the JSON structure.
Output ONLY the raw JSON list, starting with '[' and ending with ']'. Do not use markdown formatting like ```json.
"""
        },
        {
            "role": "user",
            "content": f"Article Content:\n---\n{full_context[:15000]}\n---\n\nJSON Output:" # Limit context to fit model window if necessary
        }
    ]

    try:
        # Use client.chat.completions.create for Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=config.LLM_MODEL_NAME,
            temperature=0.6, # Adjust temperature for creativity vs factualness
            max_tokens=1024, # Max tokens for the response
            # response_format={"type": "json_object"}, # Enforce JSON output if model supports it well (Llama3 often does) - Check Groq docs
        )

        # Extract the response content
        response_text = chat_completion.choices[0].message.content
        # print("--- Groq Raw Response ---")
        # print(response_text)
        # print("--- End Groq Raw Response ---")


        # Attempt to parse the JSON response
        # Groq models (like Llama 3) are usually good at following JSON instructions
        cleaned_response_text = response_text.strip()
        # Sometimes models might still add markdown even if asked not to
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:]
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-3]
        cleaned_response_text = cleaned_response_text.strip()

        script_data = json.loads(cleaned_response_text)

        # Basic validation
        if not isinstance(script_data, list):
            raise ValueError("Groq LLM did not return a JSON list.")
        valid_scenes = []
        for i, scene in enumerate(script_data):
            if isinstance(scene, dict) and 'scene_description' in scene and 'overlay_text' in scene:
                 # Optional: Truncate long text if model ignored instruction
                 overlay = scene['overlay_text']
                 if len(overlay.split()) > config.MAX_OVERLAY_WORDS:
                      print(f"Warning: Scene {i} overlay text truncated: '{overlay[:50]}...'")
                      overlay = " ".join(overlay.split()[:config.MAX_OVERLAY_WORDS]) + "..."
                 valid_scenes.append({
                      'scene_description': scene['scene_description'],
                      'overlay_text': overlay
                 })
            else:
                print(f"Warning: Skipping invalid scene structure at index {i}: {scene}")

        if not valid_scenes:
             raise ValueError("No valid scenes found in the response.")

        print(f"Script generated successfully with {len(valid_scenes)} valid scenes.")
        return valid_scenes

    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON response from Groq LLM: {e}")
        print("LLM Response Text was:")
        print(response_text)
        return None
    except Exception as e:
        print(f"Error during Groq script generation: {e}")
        # You might want to print specific Groq API errors if available
        # print(f"Groq API Error details: {e.body}" if hasattr(e, 'body') else "")
        return None

# Example usage (optional)
if __name__ == "__main__":
    # Mock data for testing
    test_title = "Example Groq Test Article Title"
    test_content = """
    This is the first paragraph about using Groq. It discusses its speed and API compatibility.
    Groq runs models like Llama 3 very quickly.

    The second paragraph mentions API keys and setup. You need an API key from the Groq console.
    The Python client makes integration straightforward. Users appreciate the low latency for
    interactive applications.
    """
    script = generate_script(test_title, test_content)
    if script:
        print("\nGenerated Script (Groq):")
        print(json.dumps(script, indent=2))
    else:
        print("\nFailed to generate script using Groq.")