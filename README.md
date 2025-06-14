# GenAI Research Assistant 🧠✨

**Empower your research with AI-driven insights and video generation!** 🚀

The **GenAI Research Assistant** is a powerful Python-based tool designed to streamline research by retrieving, summarizing, and answering queries on academic papers, technical documentation, and company reports. Built with **LangChain**, **ChromaDB**, **AI Agents**, **NVIDIA NIM**, and **AWS Bedrock**, it offers dynamic model selection and an extensible framework for advanced Retrieval-Augmented Generation (RAG). Additionally, it includes a video generation pipeline (inspired by News Reel AI) to create engaging video summaries using **Stable Diffusion**, **gTTS**, and **MoviePy**. Perfect for researchers, students, and professionals! 📚🎥

---

## Features 🌟

- 📖 **Document Retrieval & Summarization**: Fetches and summarizes academic papers, reports, and technical documents using **LangChain** and **AI Agents**.
- 🔍 **Vector Search**: Integrates **ChromaDB** for fast, efficient similarity searches across large document corpora.
- 🤖 **Dynamic Model Selection**: Choose between multiple LLMs like **AWS Bedrock (Lambda)** and **NVIDIA NIM** for tailored research needs.
- 🧩 **Extensible Framework**: Supports advanced RAG techniques and easy integration of additional models.
- 🎬 **Video Generation**: Creates video summaries with AI-generated visuals (**Stable Diffusion**), text-to-speech (**gTTS**), and video editing (**MoviePy**).
- 🛡️ **Robust Error Handling**: Ensures reliable operation with clear logging and fallback mechanisms.
- 📂 **Video Output**: Saves videos with sanitized filenames in the `output/` folder.

---

## How It Works ⚙️

1. **Document Processing** 📜:
   - Uses **LangChain** and **AI Agents** to retrieve and summarize documents.
   - Stores embeddings in **ChromaDB** for efficient similarity searches.
   - Supports multi-session contexts for seamless conversation switching.

2. **Model Selection** 🤝:
   - Dynamically switches between LLMs (**AWS Bedrock**, **NVIDIA NIM**) based on user preferences.
   - Configurable via environment variables or `config.py`.

3. **Video Generation Pipeline** 🎥:
   - **News Fetching**: Pulls trending articles via RSS feeds using `news_fetcher.py` (with fallback web scraping).
   - **Script Generation**: Creates structured video scripts using **Groq** (`script_generator.py`).
   - **Video Creation**: Combines AI-generated images (**Stable Diffusion**), text-to-speech (**gTTS**), and text overlays to produce videos (`video_creator.py`).

4. **Output** 💾:
   - Saves videos to the `output/` folder with timestamped filenames.
   - Logs execution details for debugging and monitoring.

---

## Sample Video 🎬

Watch a sample video generated by the integrated video pipeline! 🚀

**Title**: SC Rejects Staying Waqf Law, Seeks Centre's Reply  
**File**: [SC_rejects_staying_Waqf_law_seeks_Centre_s_reply_o_20250416_174217.mp4](assets/output_videos/SC_rejects_staying_Waqf_law_seeks_Centre_s_reply_o_20250416_174217.mp4)

### Watch the Video ▶️

If your platform supports HTML5 video (e.g., GitLab, custom Markdown renderers), play the video below. For platforms like GitHub, use the link above or local playback instructions.

<video controls width="600">
  <source src="output/SC_rejects_staying_Waqf_law_seeks_Centre_s_reply_o_20250416_174217.mp4" type="video/mp4">
  Your browser does not support the video tag. Download the video <a href="output/SC_rejects_staying_Waqf_law_seeks_Centre_s_reply_o_20250416_174217.mp4">here</a>.
</video>

#### Playback Instructions
- **Locally**: Open the video from the `output/` folder using a media player like VLC:
  ```bash
  # Example with VLC
  vlc output/SC_rejects_staying_Waqf_law_seeks_Centre_s_reply_o_20250416_174217.mp4
  ```
- **On GitHub**: Download the video via the link above, as GitHub doesn’t support embedded video playback.
- **Note**: Ensure your media player supports MP4. We recommend VLC or MPC-HC.

---

## Prerequisites 🛠️

To run the GenAI Research Assistant, you’ll need:

- 🐍 **Python**: Version 3.8 or higher
- 📦 **Dependencies**: See [Dependencies](#dependencies)
- 🔑 **API Keys**:
  - **Groq** (for script generation)
  - **Stability AI** (for image generation)
  - **AWS Bedrock** and **NVIDIA NIM** (for LLMs)
- 🖼️ **Stable Diffusion**: Configured locally or via cloud
- 🎥 **FFmpeg**: For video processing
- 📺 **Media Player**: For video playback (e.g., VLC)
- 🗄️ **ChromaDB**: For vector storage
- 🌐 **Internet Access**: For RSS feeds and API calls

---

## Installation ⚡️

1. **Clone the Repository** 📂:
   ```bash
   git clone https://github.com/your-username/genai-research-assistant.git
   cd genai-research-assistant
   ```

2. **Set Up a Virtual Environment** 🌐:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies** 📦:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Settings** ⚙️:
   - Create a `.env` file or edit `config.py` for API keys and settings:
     ```python
     # config.py
     OUTPUT_FOLDER = "output/"
     TEMP_IMAGE_FOLDER = "temp/images/"
     TEMP_AUDIO_FOLDER = "temp/audio/"
     GROQ_API_KEY = "your-groq-api-key"
     STABILITY_API_KEY = "your-stability-api-key"
     LLM_MODEL_NAME = "llama3-8b-8192"
     VIDEO_WIDTH = 1280
     VIDEO_HEIGHT = 720
     VIDEO_FPS = 24
     TARGET_VIDEO_DURATION_SECONDS = 30
     MIN_SCENES = 3
     MAX_SCENES = 5
     MAX_OVERLAY_WORDS = 10
     PLACEHOLDER_IMAGE = "placeholder.png"
     BACKGROUND_MUSIC_FILE = "background_music.mp3"
     ```
   - Set environment variables for API keys if using `.env`.

5. **Install FFmpeg** 🎬:
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via:
     ```bash
     # Ubuntu
     sudo apt-get install ffmpeg
     # macOS
     brew install ffmpeg
     ```

6. **Set Up ChromaDB** 🗄️:
   - Follow ChromaDB’s [installation guide](https://docs.trychroma.com/getting-started) for local or hosted setup.

---

## Dependencies 📋

Key Python packages (add to `requirements.txt`):

- `langchain`: For AI agents and document processing
- `chromadb`: For vector storage and similarity search
- `groq`: For script generation
- `gtts`: For text-to-speech
- `moviepy`: For video editing
- `stability-sdk`: For AI image generation
- `feedparser`: For RSS feed parsing
- `requests`: For web scraping
- `beautifulsoup4`: For HTML parsing
- Others:
  ```plaintext
  python-dotenv
  # Add AWS Bedrock and NVIDIA NIM SDKs as needed
  ```

Generate `requirements.txt`:
```bash
pip freeze > requirements.txt
```

---

## Usage 🚀

1. **Run the Research Assistant**:
   - For document retrieval and querying:
     ```bash
     python research_assistant.py  # Adjust based on your main script
     ```
   - For video generation (if integrated):
     ```bash
     python main.py
     ```

2. **What Happens**:
   - **Research Mode** 📚: Processes documents, stores embeddings in **ChromaDB**, and answers queries using selected LLMs.
   - **Video Mode** 🎥:
     - Fetches news articles 🗞️
     - Generates scripts with **Groq** 📝
     - Creates videos with AI images, TTS, and text overlays 🎬
     - Saves videos to `output/` (e.g., `Article_Title_20250531_011623.mp4`)

3. **Example Output** (Video Pipeline):
   ```
   --- Starting AI Video Generation Pipeline ---
   Step 1: Fetching trending news articles... 🗳️
   Selected article: 'Global Tech Summit 2025 Announced'
   Source Feed: Tech News RSS
   Step 2: Generating script using AI... ✍️
   Generated script with 4 scenes.
   Step 3: Creating video from script... 🎬
   Success! Video saved to: output/Global_Tech_Summit_20250531_011623.mp4
   --- Pipeline Finished ---
   Total execution time: 125.43 seconds
   ```

---

## Project Structure 📁

```
genai-research-assistant/
├── main.py              # Main video pipeline script
├── research_assistant.py # Main research assistant script (assumed)
├── config.py            # Configuration settings
├── news_fetcher.py      # News fetching module
├── script_generator.py  # AI script generation module
├── video_creator.py     # Video creation module
├── output/              # Generated videos
│   └── SC_rejects_staying_Waqf_law_seeks_Centre_s_reply_o_20250416_174217.mp4
├── temp/                # Temporary files (images, audio)
│   ├── images/
│   └── audio/
└── requirements.txt     # Python dependencies
```

---

## Contributing 🤝

We welcome contributions! To contribute:

1. Fork the repository 🍴
2. Create a branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request 📬

Ensure code follows the project’s style and includes tests.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements 🙌

- **LangChain**: For powerful AI agent workflows 📚
- **ChromaDB**: For efficient vector search 🗄️
- **Groq**: For fast script generation ⚡️
- **Stable Diffusion**: For stunning video visuals 🖼️
- **gTTS & MoviePy**: For audio and video processing 🎙️🎬
- **AWS Bedrock & NVIDIA NIM**: For versatile LLM support 🤖
- **FFmpeg**: For seamless video processing 🎥

---


Happy researching and video creating! 🎉🔍📽️
