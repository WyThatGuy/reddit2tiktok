# reddit2tiktok  

> **⚠️ Deprecated** — This project is no longer actively maintained and may break due to API or website changes.

**Automatically turn Reddit posts into short-form TikTok-style videos.**  

This Python project pulls **text and images from Reddit via screenshot** and combines them with a background video and text-to-speech narration to create TikTok-ready clips.  

---

## Features  
- **Fetch Reddit content** — grabs post titles, bodies, and images.  
- **Text-to-Speech** — turns post text into narration.  
- **Automatic video composition** — overlays Reddit text/images on a background video.  
- **Customizable background video** — swap out `loop.mp4` with your own.  

---

## Project Structure  

| File | Description |
|------|-------------|
| `video+audio.py` | **Main script** — orchestrates the full video creation process. |
| `tts.py` | Standalone **text-to-speech** utility, code added to `video+audio.py`. |
| `loop.mp4` | Default looping background video. Change this filename in the code to use your own. |
| `chromedriver.exe` | Used by **Selenium** to render and screenshot Reddit posts. |

---

## Requirements  

### 1. ImageMagick Software  
- [**ImageMagick**](https://imagemagick.org/) — required for rendering text as images.

### 2. ChromeDriver  
- Download **ChromeDriver** matching your Chrome version: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)  
- Place it in the project folder (or update the path in the code).

---

## Usage  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/reddit2tiktok.git
   cd reddit2tiktok
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main script**  
   ```bash
   python video+audio.py
   ```

4. **Output** will be saved as a `.mp4` file in the project directory.

---

## Notes  
- Ensure `ImageMagick` is added to your system PATH.  
- To change the background video, replace `loop.mp4` or update its filename in the script.  
- The quality of text-to-speech may vary.  

---

## License  
MIT License — feel free to use and modify.
