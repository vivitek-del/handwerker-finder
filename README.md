# Handwerker-Finder USA 🔧

## Setup & Deployment

1. Dieses Projekt als ZIP entpacken und in ein neues GitHub-Repository hochladen
2. Gehe zu [Streamlit Cloud](https://share.streamlit.io) und logge dich ein
3. Klicke auf "New App" → wähle dein Repository → Hauptdatei: `handwerker_finder_app.py`
4. Unter **Settings → Secrets** folgendes einfügen:
   ```
   YELP_API_KEY = "dein_yelp_key"
   GOOGLE_API_KEY = "dein_google_key"
   APIFY_API_TOKEN = "dein_apify_key"
   ```
5. Klicke auf **Deploy** – fertig ✅
