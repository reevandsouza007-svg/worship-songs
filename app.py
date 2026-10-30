import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote_plus

st.set_page_config(page_title="WorshipWave", page_icon="🎵", layout="wide")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0b1020,#15102a,#090d18);color:#fff}
section[data-testid="stSidebar"]{background:#101526}
.hero{padding:28px;border-radius:22px;background:linear-gradient(120deg,#5936b4,#bd5cf0,#ee83bd);margin-bottom:20px}
.hero h1,.hero p{color:white}
.card{background:#171d30;border:1px solid #292f49;border-radius:16px;padding:16px;margin-bottom:8px}
div.stButton>button{width:100%;border-radius:10px;background:#6e49cf;color:white;border:1px solid #5c4a9b}
</style>
""", unsafe_allow_html=True)

LANGUAGES = {"English":"🇬🇧","Hindi":"🇮🇳","Kannada":"🇮🇳","Spanish":"🇪🇸","Konkani":"🎶"}

# The first song has a verified video ID from Hillsong Worship's official YouTube channel.
# For other songs, add the official video's 11-character ID in the youtube_id field.
SONGS = [
    {"title":"What a Beautiful Name","artist":"Hillsong Worship","language":"English","category":"Worship","youtube_id":"nQWFzMvCfLE"},
    {"title":"Goodness of God","artist":"Bethel Music","language":"English","category":"Praise","youtube_id":""},
    {"title":"Way Maker","artist":"Sinach","language":"English","category":"Praise","youtube_id":""},
    {"title":"Yeshu Teri Mahima Ho","artist":"Hindi Christian Worship","language":"Hindi","category":"Praise","youtube_id":""},
    {"title":"Hindi Christian Worship","artist":"Hindi Worship","language":"Hindi","category":"Worship","youtube_id":""},
    {"title":"Nanna Hathira Veru O Yesuve","artist":"Kannada Christian Worship","language":"Kannada","category":"Worship","youtube_id":""},
    {"title":"Kannada Christian Worship","artist":"Kannada Worship","language":"Kannada","category":"Praise","youtube_id":""},
    {"title":"Alabanzas Cristianas","artist":"Spanish Christian Worship","language":"Spanish","category":"Praise","youtube_id":""},
    {"title":"Adoración Cristiana","artist":"Spanish Worship","language":"Spanish","category":"Worship","youtube_id":""},
    {"title":"Konkani Christian Hymns","artist":"Konkani Worship","language":"Konkani","category":"Hymns","youtube_id":""},
    {"title":"Zoyo Zoyo Jezu Bala","artist":"Konkani Christian Carol","language":"Konkani","category":"Hymns","youtube_id":""},
]

if "favorites" not in st.session_state: st.session_state.favorites = []
if "playlist" not in st.session_state: st.session_state.playlist = []
if "current_song" not in st.session_state: st.session_state.current_song = None

with st.sidebar:
    st.markdown("# 🕊️ WorshipWave")
    st.caption("One Faith. Five Languages.")
    page = st.radio("NAVIGATION", ["🏠 Home", "🔎 Discover", "❤️ Favorites", "📂 My Playlist"])
    language = st.selectbox("🎵 Choose Language", ["All Languages", *LANGUAGES.keys()])
    category = st.selectbox("🎼 Music Category", ["All Categories", "Worship", "Praise", "Hymns", "Prayer", "Gospel"])
    st.caption("Christian music only ✝️")

st.markdown('<div class="hero"><h1>WorshipWave 🕊️</h1><p>One Faith. Five Languages. Endless Worship.</p><p>Christian praise, worship, gospel and hymns.</p></div>', unsafe_allow_html=True)

search = st.text_input("🔍 Search songs or artists", placeholder="Search Christian music")

def filtered(items):
    if language != "All Languages":
        items = [s for s in items if s["language"] == language]
    if category != "All Categories":
        items = [s for s in items if s["category"] == category]
    if search.strip():
        q = search.strip().lower()
        items = [s for s in items if q in s["title"].lower() or q in s["artist"].lower() or q in s["language"].lower()]
    return items

def play_song(song):
    st.session_state.current_song = song
    st.rerun()

def show_songs(items, key_prefix):
    if not items:
        st.info("No songs found. Try another language or search.")
        return
    for idx in range(0, len(items), 2):
        cols = st.columns(2)
        for col, song in zip(cols, items[idx:idx+2]):
            with col:
                st.markdown(f"""<div class="card"><div style="font-size:32px">🎵</div>
                <h3>{song['title']}</h3><p>{song['artist']}</p>
                <span>{LANGUAGES[song['language']]} {song['language']} · {song['category']}</span></div>""", unsafe_allow_html=True)
                if song["youtube_id"]:
                    if st.button("▶ Play inside WorshipWave", key=f"{key_prefix}_play_{song['title']}"):
                        play_song(song)
                else:
                    query = f"{song['title']} {song['artist']} {song['language']} Christian song official"
                    st.link_button("🔎 Find official recording", "https://www.youtube.com/results?search_query=" + quote_plus(query), key=f"{key_prefix}_search_{song['title']}")
                    st.caption("To play inside this app, add a verified YouTube video ID to this song in app.py.")
                is_fav = any(x["title"] == song["title"] for x in st.session_state.favorites)
                if st.button("💔 Remove Favorite" if is_fav else "❤️ Add to Favorites", key=f"{key_prefix}_fav_{song['title']}"):
                    if is_fav:
                        st.session_state.favorites = [x for x in st.session_state.favorites if x["title"] != song["title"]]
                    else:
                        st.session_state.favorites.append(song)
                    st.rerun()
                in_list = any(x["title"] == song["title"] for x in st.session_state.playlist)
                if st.button("✓ In Playlist" if in_list else "➕ Add to Playlist", key=f"{key_prefix}_list_{song['title']}"):
                    if not in_list:
                        st.session_state.playlist.append(song)
                        st.toast("Added to your playlist!")

if st.session_state.current_song:
    song = st.session_state.current_song
    st.divider()
    st.subheader("🎧 Now Playing")
    st.markdown(f"### {song['title']} — {song['artist']}")
    st.caption("If you do not hear sound, check the player volume and make sure the video is allowed to play in embedded players.")
    components.iframe(f"https://www.youtube-nocookie.com/embed/{song['youtube_id']}?autoplay=1", height=390, scrolling=False)
    st.divider()

if page == "🏠 Home":
    st.subheader("🌍 Browse by language")
    cols = st.columns(5)
    for col, lang in zip(cols, LANGUAGES):
        with col:
            st.markdown(f"### {LANGUAGES[lang]}")
            st.caption(lang)
    st.subheader("🎵 Christian songs")
    show_songs(filtered(SONGS), "home")
elif page == "🔎 Discover":
    st.subheader("🔎 Discover Worship Music")
    show_songs(filtered(SONGS), "discover")
elif page == "❤️ Favorites":
    st.subheader("❤️ Favorites")
    show_songs(filtered(st.session_state.favorites), "fav")
else:
    st.subheader("📂 My Playlist")
    show_songs(filtered(st.session_state.playlist), "list")
    if st.session_state.playlist and st.button("🗑️ Clear Playlist"):
        st.session_state.playlist = []
        st.rerun()

st.markdown('<div style="text-align:center;padding:22px;color:#929bb7">✝️ WorshipWave • Made for Christian Music Lovers</div>', unsafe_allow_html=True)
