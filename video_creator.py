# import os
# import random
# import time # For unique filenames
# import moviepy
# from moviepy import *
# import matplotlib.font_manager
# # Consider adding PIL/Pillow if doing more complex image manipulation
# # from PIL import Image
# # from moviepy.config import change_withtings # To potentially specify ImageMagick path if needed
# # Uncomment the line below and with the path if MoviePy can't find ImageMagick automatically
# # change_withtings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # Example for Windows

# import config # Use config.py for withtings

# # --- Placeholder for AI Image Generation ---
# def generate_image_for_scene(scene_description, scene_index):
#     """
#     Generates or retrieves an image for a given scene description.
#     Currently uses a placeholder. Replace with actual API calls if desired.
#     """
#     # Ensure temp folder exists
#     os.makedirs(config.TEMP_IMAGE_FOLDER, exist_ok=True)
#     # Add timestamp to filename to prevent potential clashes if run quickly
#     output_path = os.path.join(config.TEMP_IMAGE_FOLDER, f"scene_{scene_index}_{int(time.time())}.png")

#     if config.USE_AI_IMAGE_GENERATION:
#         print(f"Attempting AI image generation for: '{scene_description}'...")
#         # ===> [YOUR AI IMAGE GENERATION API CALL GOES HERE] <===
#         # Example using a hypothetical API:
#         # try:
#         #     image_data = your_image_api.generate(prompt=f"News graphic illustrating: {scene_description}", width=config.VIDEO_WIDTH, height=config.VIDEO_HEIGHT)
#         #     with open(output_path, 'wb') as f:
#         #         f.write(image_data)
#         #     print(f"AI Image saved to {output_path}")
#         #     return output_path
#         # except Exception as e:
#         #     print(f"Error generating AI image: {e}. Falling back to placeholder.")
#         #     # Fallback to placeholder if API fails
#         #     from shutil import copyfile
#         #     try:
#         #          copyfile(config.PLACEHOLDER_IMAGE, output_path)
#         #          return output_path
#         #     except FileNotFoundError:
#         #          print(f"Error: Placeholder image {config.PLACEHOLDER_IMAGE} not found!")
#         #          return None
#         # =========================================================
#         print("Warning: USE_AI_IMAGE_GENERATION is True, but no specific implementation is provided in video_creator.py. Using placeholder.")
#         # Fallback to placeholder if flag is True but code is missing
#         from shutil import copyfile
#         try:
#              copyfile(config.PLACEHOLDER_IMAGE, output_path)
#              return output_path
#         except FileNotFoundError:
#              print(f"Error: Placeholder image {config.PLACEHOLDER_IMAGE} not found!")
#              return None

#     else:
#         # Use the static placeholder image
#         print(f"Using placeholder image for scene {scene_index}.")
#         from shutil import copyfile
#         try:
#             copyfile(config.PLACEHOLDER_IMAGE, output_path)
#             return output_path
#         except FileNotFoundError:
#             print(f"Error: Placeholder image {config.PLACEHOLDER_IMAGE} not found!")
#             return None
#         except Exception as e:
#             print(f"Error copying placeholder image: {e}")
#             return None


# # --- Main Video Creation Function ---
# def create_video_from_script(script_data, output_filename_base):
#     """Creates a video from the script data using MoviePy."""
#     if not script_data:
#         print("Error: No script data provided to create video.")
#         return None

#     num_scenes = len(script_data)
#     if num_scenes == 0:
#         print("Error: Script data is empty.")
#         return None

#     output_video_path = os.path.join(config.OUTPUT_FOLDER, f"{output_filename_base}.mp4")
#     print(f"Starting video creation for '{output_video_path}' with {num_scenes} scenes...")

#     # Calculate duration per scene
#     duration_per_scene = max(2.0, config.TARGET_VIDEO_DURATION_SECONDS / num_scenes) # Ensure minimum duration
#     print(f"Calculated duration per scene: {duration_per_scene:.2f} seconds")

#     video_clips = []
#     temp_image_files = [] # Keep track of generated images for cleanup

#     for i, scene in enumerate(script_data):
#         print(f"Processing scene {i+1}/{num_scenes}: {scene.get('scene_description', 'No description')}")

#         # 1. Get Image for the scene
#         image_path = generate_image_for_scene(scene.get('scene_description', 'news background'), i)
#         if not image_path or not os.path.exists(image_path):
#             print(f"Error: Could not get image for scene {i+1}. Skipping scene.")
#             continue
#         temp_image_files.append(image_path)

#         # 2. Create Image Clip with Ken Burns effect (optional zoom/pan)
#         img_clip = ImageClip(image_path).with_duration(duration_per_scene)
#         # Resize if necessary to fit video dimensions (cropping might occur)
#         img_clip = img_clip.resized(height=config.VIDEO_HEIGHT)
#         if img_clip.w < config.VIDEO_WIDTH:
#             img_clip = img_clip.resize(width=config.VIDEO_WIDTH)

#         # Simple Ken Burns effect: zoom in slightly
#         img_clip = img_clip.resized(lambda t: 1 + 0.02 * t) # Zoom in 2% per second
#         img_clip = img_clip.with_position(('center', 'center'))

#         # Ensure the clip size matches the video dimensions after potential resize/zoom
#         # Create a background color clip matching video size and composite image onto it
#         background = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
#                                color=(0,0,0), # Black background
#                                duration=duration_per_scene)
#         final_img_clip = CompositeVideoClip([background, img_clip],
#                                             size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))


#         # 3. Create Text Clip for Overlay
#         overlay_text = scene.get('overlay_text', '')
#         if overlay_text:
#              # Configure text appearance
#              # Font choice: Check available fonts on your system or provide a path to a .ttf file
#              # On Linux: `fc-list` command
#              # On Windows: Check C:\Windows\Fonts
#              font_choice = 'Arial' # Try a common font
#              # font_choice = '/path/to/your/font.ttf' # Or specify path
#              try:
#                  text_clip = TextClip(
#                                     # text=overlay_text,
#                                     # # fontsize=24, # Adjust size as needed
#                                     # color='white',
#                                     # font=font_choice,
#                                     # stroke_color='black', # Add outline for readability
#                                     # stroke_width=1.5,
#                                     # method='caption', # Auto-wrap text
#                                     # size=(config.VIDEO_WIDTH * 0.8, None), # Limit text width
#                                     # # align='center'
#                                     text=overlay_text,
                                    
#                                     font="C:\\Windows\\Fonts\\lucon.ttf"
# ,
#                                     font_size=24,
#                                     color="white",
#                                     method="caption",
#                                     size=(int(config.VIDEO_WIDTH * 0.8), None),
#                                                                     )
#              except OSError as e:
#                   print(f"Warning: Font '{font_choice}' not found or invalid: {e}. Using default.")
#                   # Fallback to default font if specified one fails
#                   text_clip = TextClip(overlay_text, fontsize=40, color='white', stroke_color='black', stroke_width=1.5, method='caption', size=(config.VIDEO_WIDTH * 0.8, None), align='center')

#              # with text position (e.g., bottom center) and duration
#              text_clip = text_clip.with_position(('center', 'bottom')).with_duration(duration_per_scene)

#              # 4. Composite Text onto Image Clip
#              scene_clip = CompositeVideoClip([final_img_clip, text_clip], size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
#         else:
#              # If no text, just use the image clip
#              scene_clip = final_img_clip

#         video_clips.append(scene_clip)

#     if not video_clips:
#         print("Error: No valid scenes were processed. Video not created.")
#         # Clean up any temp images that might have been created
#         for img_file in temp_image_files:
#             try:
#                 os.remove(img_file)
#             except OSError:
#                 pass # Ignore errors during cleanup
#         return None

#     # 5. Concatenate all scene clips
#     final_clip = concatenate_videoclips(video_clips, method="compose")

#     # 6. Add Background Music (Optional)
#     if config.BACKGROUND_MUSIC_FILE and os.path.exists(config.BACKGROUND_MUSIC_FILE):
#         try:
#             print(f"Adding background music: {config.BACKGROUND_MUSIC_FILE}")
#             audio_clip = AudioFileClip(config.BACKGROUND_MUSIC_FILE)
#             # Trim or loop audio to match video duration
#             if audio_clip.duration > final_clip.duration:
#                 audio_clip = audio_clip.subclip(0, final_clip.duration)
#             # elif audio_clip.duration < final_clip.duration:
#                 # Consider looping if needed: audio_clip = audio_clip.fx(vfx.loop, duration=final_clip.duration)
#                 # pass # Or just let it end early

#             # with audio volume (e.g., lower it)
#             audio_clip = audio_clip.volumex(0.3) # with volume to 30%

#             final_clip = final_clip.with_audio(audio_clip)
#         except Exception as e:
#             print(f"Warning: Could not add background music: {e}")
#     else:
#         print("Info: Background music file not found or not specified. Skipping.")

#     # 7. Write the final video file
#     try:
#         print(f"Writing final video to: {output_video_path}")
#         final_clip.write_videofile(output_video_path,
#                                    fps=config.VIDEO_FPS,
#                                    codec='libx264', # Common codec
#                                    audio_codec='aac', # Common audio codec
#                                    prewith='medium', # Encoding speed vs quality
#                                    threads=4) # Use multiple threads for encoding
#         print("Video creation completed successfully.")
#     except Exception as e:
#         print(f"Error writing video file: {e}")
#         output_video_path = None # Indicate failure
#     finally:
#         # Close clips to release resources (important for MoviePy)
#         final_clip.close()
#         if 'audio_clip' in locals() and audio_clip:
#              audio_clip.close()
#         for clip in video_clips:
#             clip.close() # Close individual scene composites

#     # 8. Clean up temporary image files
#     print("Cleaning up temporary image files...")
#     for img_file in temp_image_files:
#         try:
#             os.remove(img_file)
#             # print(f"Removed temp file: {img_file}")
#         except OSError as e:
#             print(f"Warning: Could not remove temp file {img_file}: {e}")

#     return output_video_path # Return path if successful, None otherwise


# # Example Usage (Optional)
# if __name__ == "__main__":
#     # Mock script data for testing video creation directly
#     test_script = [
#         {'scene_description': 'Global financial charts showing downward trend', 'overlay_text': 'Markets react nervously to recent global events.'},
#         {'scene_description': 'Politician speaking urgently at press conference', 'overlay_text': 'Officials promise swift action and investigation.'},
#         {'scene_description': 'Busy city street view with people walking', 'overlay_text': 'Public sentiment remains mixed as situation unfolds.'},
#         {'scene_description': 'Abstract network connection graphic', 'overlay_text': 'International cooperation deemed crucial for resolution.'},
#         {'scene_description': 'Newspaper headlines graphic', 'overlay_text': 'Further developments expected in the coming days.'}
#     ]
#     output_name = f"test_video_{int(time.time())}"
#     result_path = create_video_from_script(test_script, output_name)
#     if result_path:
#         print(f"Test video saved to: {result_path}")
#     else:
#         print("Test video creation failed.")

import os
import time
import logging
from gtts import gTTS
from moviepy import *
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from shutil import copyfile

import config

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- AI Image Generation with Stability AI ---
def generate_image_for_scene(scene_description, scene_index):
    """
    Generates an image for a given scene description using Stability AI or falls back to placeholder.
    """
    os.makedirs(config.TEMP_IMAGE_FOLDER, exist_ok=True)
    output_path = os.path.join(config.TEMP_IMAGE_FOLDER, f"scene_{scene_index}_{int(time.time())}.png")

    if not config.USE_AI_IMAGE_GENERATION:
        logger.info(f"AI image generation disabled. Using placeholder for scene {scene_index}.")
        try:
            copyfile(config.PLACEHOLDER_IMAGE, output_path)
            return output_path
        except FileNotFoundError:
            logger.error(f"Placeholder image {config.PLACEHOLDER_IMAGE} not found!")
            return None

    logger.info(f"Generating AI image for scene {scene_index}: '{scene_description}'")
    try:
        stability_api = client.StabilityInference(
            key=os.getenv("STABILITY_API_KEY"),
            verbose=True
        )
        responses = stability_api.generate(
            prompt=f"A high-quality news graphic illustrating: {scene_description}",
            width=config.VIDEO_WIDTH,
            height=config.VIDEO_HEIGHT,
            steps=50,
            cfg_scale=7.5
        )
        for resp in responses:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    with open(output_path, "wb") as f:
                        f.write(artifact.binary)
                    logger.info(f"AI image saved to {output_path}")
                    return output_path
        logger.warning("No image artifact received from Stability AI. Falling back to placeholder.")
    except Exception as e:
        logger.error(f"AI image generation failed: {e}. Falling back to placeholder.")

    # Fallback to placeholder
    try:
        copyfile(config.PLACEHOLDER_IMAGE, output_path)
        logger.info(f"Fell back to placeholder image: {output_path}")
        return output_path
    except FileNotFoundError:
        logger.error(f"Placeholder image {config.PLACEHOLDER_IMAGE} not found!")
        return None

# --- Text-to-Speech Audio Generation ---
def generate_tts_audio(text, scene_index):
    """
    Generates TTS audio for the given text and saves it to a temporary file.
    """
    os.makedirs(config.TEMP_AUDIO_FOLDER, exist_ok=True)
    output_path = os.path.join(config.TEMP_AUDIO_FOLDER, f"tts_{scene_index}_{int(time.time())}.mp3")
    
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        logger.info(f"TTS audio saved to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"TTS generation failed for text '{text}': {e}")
        return None

# --- Main Video Creation Function ---
def create_video_from_script(script_data, output_filename_base):
    """Creates a video from the script data with AI images, text overlays, TTS, and background music."""
    if not script_data:
        logger.error("No script data provided to create video.")
        return None

    num_scenes = len(script_data)
    if num_scenes == 0:
        logger.error("Script data is empty.")
        return None

    output_video_path = os.path.join(config.OUTPUT_FOLDER, f"{output_filename_base}.mp4")
    logger.info(f"Starting video creation for '{output_video_path}' with {num_scenes} scenes...")

    # Calculate duration per scene (adjusted for TTS readability)
    duration_per_scene = max(3.0, config.TARGET_VIDEO_DURATION_SECONDS / num_scenes)
    logger.info(f"Calculated duration per scene: {duration_per_scene:.2f} seconds")

    video_clips = []
    temp_image_files = []
    temp_audio_files = []

    for i, scene in enumerate(script_data):
        logger.info(f"Processing scene {i+1}/{num_scenes}: {scene.get('scene_description', 'No description')}")

        # 1. Generate AI Image
        image_path = generate_image_for_scene(scene.get('scene_description', 'news background'), i)
        if not image_path or not os.path.exists(image_path):
            logger.error(f"Could not get image for scene {i+1}. Skipping scene.")
            continue
        temp_image_files.append(image_path)

        # 2. Create Image Clip with Ken Burns effect
        img_clip = ImageClip(image_path).with_duration(duration_per_scene)
        img_clip = img_clip.resized(height=config.VIDEO_HEIGHT)
        if img_clip.w < config.VIDEO_WIDTH:
            img_clip = img_clip.resize(width=config.VIDEO_WIDTH)

        img_clip = img_clip.resized(lambda t: 1 + 0.02 * t)  # Zoom in 2% per second
        img_clip = img_clip.with_position(('center', 'center'))

        background = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                              color=(0, 0, 0),
                              duration=duration_per_scene)
        final_img_clip = CompositeVideoClip([background, img_clip],
                                            size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))

        # 3. Create Text Clip for Overlay
        overlay_text = scene.get('overlay_text', '')
        audio_clip = None
        if overlay_text:
            try:
                text_clip = TextClip(
                    text=overlay_text,
                    font="C:\\Windows\\Fonts\\lucon.ttf",
                    font_size=24,
                    color="white",
                    stroke_color="black",
                    stroke_width=1,
                    method="caption",
                    size=(int(config.VIDEO_WIDTH * 0.8), None),
                    # align="center"
                )
                text_clip = text_clip.with_position(('center', 'bottom')).with_duration(duration_per_scene)
            except OSError as e:
                logger.warning(f"Font 'lucon.ttf' not found: {e}. Using default.")
                text_clip = TextClip(
                    text=overlay_text,
                    fontsize=24,
                    color="white",
                    stroke_color="black",
                    stroke_width=1.5,
                    method="caption",
                    size=(int(config.VIDEO_WIDTH * 0.8), None),
                    align="center"
                ).set_position(('center', 'bottom')).set_duration(duration_per_scene)

            # 4. Generate TTS Audio
            tts_audio_path = generate_tts_audio(overlay_text, i)
            if tts_audio_path and os.path.exists(tts_audio_path):
                audio_clip = AudioFileClip(tts_audio_path)
                temp_audio_files.append(tts_audio_path)
                # Adjust duration to match scene
                # audio_clip = audio_clip.with_duration(duration_per_scene)
                scene_duration = audio_clip.duration
                img_clip = img_clip.with_duration(scene_duration)
                if overlay_text:
                    text_clip = text_clip.with_duration(scene_duration)


            # 5. Composite Text onto Image
            scene_clip = CompositeVideoClip([final_img_clip, text_clip],
                                           size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
        else:
            scene_clip = final_img_clip

        # 6. Set Audio for Scene
        if audio_clip:
            scene_clip = scene_clip.with_audio(audio_clip)

        video_clips.append(scene_clip)

    if not video_clips:
        logger.error("No valid scenes were processed. Video not created.")
        for img_file in temp_image_files:
            try:
                os.remove(img_file)
            except OSError:
                pass
        for audio_file in temp_audio_files:
            try:
                os.remove(audio_file)
            except OSError:
                pass
        return None

    # 7. Concatenate all scene clips
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # 8. Add Background Music
    if config.BACKGROUND_MUSIC_FILE and os.path.exists(config.BACKGROUND_MUSIC_FILE):
        try:
            logger.info(f"Adding background music: {config.BACKGROUND_MUSIC_FILE}")
            bg_music = AudioFileClip(config.BACKGROUND_MUSIC_FILE)
            # Loop or trim to match video duration
            bg_music = bg_music.with_duration(final_clip.duration)
            # Lower volume to avoid overpowering TTS
            # bg_music = bg_music.volumex(0.2)  # 20% volume

            # Composite with existing audio (TTS)
            if final_clip.audio:
                final_audio = CompositeAudioClip([final_clip.audio, bg_music])
                final_clip = final_clip.with_audio(final_audio)
            else:
                final_clip = final_clip.with_audio(bg_music)
        except Exception as e:
            logger.warning(f"Could not add background music: {e}")
    else:
        logger.info("Background music file not found or not specified. Skipping.")

    # 9. Write the final video file
    try:
        logger.info(f"Writing final video to: {output_video_path}")
        final_clip.write_videofile(
            output_video_path,
            fps=config.VIDEO_FPS,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            threads=4
        )
        logger.info("Video creation completed successfully.")
    except Exception as e:
        logger.error(f"Error writing video file: {e}")
        output_video_path = None
    finally:
        final_clip.close()
        for clip in video_clips:
            clip.close()

    # 10. Clean up temporary files
    logger.info("Cleaning up temporary files...")
    for img_file in temp_image_files:
        try:
            os.remove(img_file)
        except OSError as e:
            logger.warning(f"Could not remove temp file {img_file}: {e}")
    for audio_file in temp_audio_files:
        try:
            os.remove(audio_file)
        except OSError as e:
            logger.warning(f"Could not remove temp file {audio_file}: {e}")

    return output_video_path

# Example Usage
if __name__ == "__main__":
    test_script = [
        {'scene_description': 'Global financial charts showing downward trend', 'overlay_text': 'Markets react nervously to recent global events.'},
        {'scene_description': 'Politician speaking urgently at press conference', 'overlay_text': 'Officials promise swift action and investigation.'},
        {'scene_description': 'Busy city street view with people walking', 'overlay_text': 'Public sentiment remains mixed as situation unfolds.'},
        {'scene_description': 'Abstract network connection graphic', 'overlay_text': 'International cooperation deemed crucial for resolution.'},
        {'scene_description': 'Newspaper headlines graphic', 'overlay_text': 'Further developments expected in the coming days.'}
    ]
    output_name = f"test_video_{int(time.time())}"
    result_path = create_video_from_script(test_script, output_name)
    if result_path:
        logger.info(f"Test video saved to: {result_path}")
    else:
        logger.error("Test video creation failed.")