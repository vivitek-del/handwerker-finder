import streamlit as st
import requests

# 🔑 Nur Yelp API Key aus Streamlit Secrets laden
YELP_API_KEY = st.secrets["YELP_API_KEY"]

def search_yelp(location, term):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"term": term, "location": location, "limit": 10, "sort_by": "rating"}
    r = requests.get(url, headers=headers, params=params)
    return r.json().get("businesses", [])

# 📌 Streamlit UI
st.set_page_config(page_title="Handwerker-Finder USA", page_icon="🔧", layout="centered")

st.title("🔧 Handwerker-Finder (nur Yelp)")
st.write("Finde schnell Handwerker in deiner Nähe – basierend auf Yelp-Daten.")

location = st.text_input("📍 Ort (z.B. Miami, FL)")
term = st.text_input("🛠 Handwerker-Typ (z.B. plumber, electrician)")

if st.button("🔍 Suchen"):
    if location and term:
        st.info(f"Suche nach '{term}' in {location}...")
        yelp_results = search_yelp(location, term)
        
        if yelp_results:
            for b in yelp_results:
                st.markdown(f"""
                **{b['name']}**  
                📍 {b['location']['address1']}  
                📞 {b.get('phone', 'Keine Nummer')}  
                ⭐ {b.get('rating', 'N/A')}
                """)
                st.markdown("---")
        else:
            st.warning("Keine Ergebnisse gefunden.")
    else:
        st.error("Bitte Ort und Handwerker-Typ eingeben.")
