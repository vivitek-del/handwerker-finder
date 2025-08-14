import streamlit as st
import requests

# 🔑 API Keys aus Streamlit Secrets laden
YELP_API_KEY = st.secrets["YELP_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
APIFY_API_TOKEN = st.secrets["APIFY_API_TOKEN"]

def search_yelp(location, term):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"term": term, "location": location, "limit": 10, "sort_by": "rating"}
    r = requests.get(url, headers=headers, params=params)
    return r.json().get("businesses", [])

def search_google_places(location, term):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": f"{term} in {location}", "key": GOOGLE_API_KEY}
    r = requests.get(url, params=params)
    return r.json().get("results", [])

def search_craigslist(location, term):
    url = f"https://api.apify.com/v2/acts/epctex~craigslist-scraper/run-sync-get-dataset-items"
    payload = {"searchQuery": term, "maxItems": 10, "location": location}
    r = requests.post(f"{url}?token={APIFY_API_TOKEN}", json=payload)
    try:
        return r.json()
    except:
        return []

def merge_results(yelp_data, google_data, craigslist_data):
    seen = set()
    merged = []
    
    def add_result(name, address, phone="", rating=None, source=""):
        key = (name.lower() + address.lower()).strip()
        if key not in seen:
            seen.add(key)
            merged.append({
                "name": name,
                "address": address,
                "phone": phone,
                "rating": rating,
                "source": source
            })
    
    for b in yelp_data:
        add_result(b["name"], b["location"]["address1"], b.get("phone", ""), b.get("rating"), "Yelp")
    
    for g in google_data:
        add_result(g["name"], g.get("formatted_address", ""), "", None, "Google Places")
    
    for c in craigslist_data:
        add_result(c.get("title", ""), c.get("location", ""), "", None, "Craigslist")
    
    merged.sort(key=lambda x: (x["rating"] is None, -(x["rating"] or 0)))
    return merged

# 📌 Streamlit UI
st.set_page_config(page_title="Handwerker-Finder USA", page_icon="🔧", layout="centered")

st.title("🔧 Handwerker-Finder (USA)")
st.write("Finde schnell Handwerker in deiner Nähe – durchsucht Yelp, Google Places & Craigslist.")

location = st.text_input("📍 Ort (z.B. Miami, FL)")
term = st.text_input("🛠 Handwerker-Typ (z.B. plumber, electrician)")

if st.button("🔍 Suchen"):
    if location and term:
        st.info(f"Suche nach '{term}' in {location}...")
        yelp_results = search_yelp(location, term)
        google_results = search_google_places(location, term)
        craigslist_results = search_craigslist(location, term)
        
        results = merge_results(yelp_results, google_results, craigslist_results)
        
        if results:
            for r in results:
                st.markdown(f"""
                **{r['name']}**  
                📍 {r['address']}  
                📞 {r['phone'] or 'Keine Nummer'}  
                ⭐ {r['rating'] or 'N/A'} ({r['source']})
                """)
                st.markdown("---")
        else:
            st.warning("Keine Ergebnisse gefunden.")
    else:
        st.error("Bitte Ort und Handwerker-Typ eingeben.")
