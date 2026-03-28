# Music Platform Metadata Scraper API

This is a Flask-based REST API designed to perform headless web scraping on major music streaming platforms. It extracts rich musical metadata, artist biographies, listening statistics, and search URLs using Playwright. 

This tool is particularly useful for generating robust context data for automated workflows, prompt generators, or AI pipelines where real-world music metric extraction is required safely and efficiently via multithreading.

## 🚀 Features

- **Concurrent Execution**: Executes multiple browser sessions simultaneously via `ThreadPoolExecutor` to halve the overall querying time.
- **Headless Scraping**: Powered by Playwright to bypass common bot-protections and fully render dynamic Single Page Applications before data extraction.
- **Rich Metadata Extraction**: Parses nested components (like "About" sections or hover-cards) to extract bios, listener numbers, and image references.
- **Environment configuration**: Clean setup using Python's `dotenv` to maintain environments completely decoupled from the codebase.

## 🛠️ Requirements

- Python 3.10+
- Chromium via Playwright

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ariff-dev/huf_scraping_tool.git
   cd huf_scraping_tool
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   
   # For Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Playwright browser executables:**
   ```bash
   playwright install chromium
   ```

5. **Configure environment variables:**
   Duplicate the `.env.example` file and rename it to `.env`. Adjust your target settings:
   ```env
   # .env
   FLASK_PORT=5000
   FLASK_HOST=0.0.0.0
   FLASK_ENV=development
   SCRAPER_HEADLESS=True
   ```

## ⚙️ Usage

Start the Flask server:
```bash
python main.py
```

### Endpoint: `/api/inf/`
**Method:** `POST`

Extracts both the artist details and the specific track discovery flow simultaneously, returning a single assembled structure.

**Request Payload:**
```json
{
  "artist": "Artist Name",
  "song": "Song Title"
}
```

**cURL / PowerShell Example:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/inf/" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"artist": "Borja Picó", "song": "Sonrisas"}'
```

**Success Response Example:**
```json
{
  "artist": "Borja Picó",
  "song": "Sonrisas",
  "artist_data": {
    "extracted": {
      "artist_name": "...",
      "bio": "...",
      "image_url": "...",
      "monthly_listeners": "..."
    },
    ...
  },
  "song_data": {
      "song_url": "...",
      ...
  },
  "success": true
}
```

## ⚖️ Disclaimer

This repository is for educational and research purposes. Ensure to always abide by the terms of service of the web applications you interact with. 
