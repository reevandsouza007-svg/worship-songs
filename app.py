import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote_plus

st.set_page_config(
    page_title="WorshipWave | Christian Music",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background: linear-gradient(135deg,#0b1020,#15102a,#090d18); color:#fff; }
section[data-testid="stSidebar"] { background:#101526; border-right:1px solid #292d43; }
h1,h2,h3,p,label { color:#fff; }
.hero { padding:32px; border-radius:24px; background:linear-gradient(120deg,#5936b4,#bd5cf0,#ee83bd); margin-bottom:24px; }
.hero h1 { font-size:42px; font-weight:800; margin:0 0 8px 0; }
.hero p { color:#fff; }
.song-card { background:#171d30; border:1px solid #292f49; border-radius:18px; padding:18px; margin-bottom:10px; }
.badge { display:inline-block; padding:5px 10px; border-radius:20px; background:#30254e; color:#e2c8ff; font-size:12px; }
div.stButton > button { width:100%; border-radius:12px; border:1px solid #5c4a9b; background:#6e49cf; color:white; font-weight:600; min-height:40px; }
div.stButton > button:hover { background:#895ce8; border-color:#b89aff; color:white; }
.footer { text-align:center; padding:25px 0; color:#8e97b2; font-size:12px; }
</style>
""", unsafe_allow_html=True)

LANGUAGES = {
    "English": "🇬🇧",
    "Hindi": "🇮🇳",
    "Kannada": "🇮🇳",
    "Spanish": "🇪🇸",
    "Konkani": "🎶",
}

# Add a verified YouTube video ID to a song's youtube_id field to embed it.
# These starter entries are search shortcuts, not verified recordings.
SONGS = [
    {"title":"What a Beautiful Name","artist":"Hillsong Worship","language":"English","category":"Worship","youtube_id":"","emoji":"🕊️"},
    {"title":"Goodness of God","artist":"Bethel Music","language":"English","category":"Praise","youtube_id":"","emoji":"🙏"},
    {"title":"Way Maker","artist":"Sinach","language":"English","category":"Praise","youtube_id":"","emoji":"✨"},
    {"title":"Hindi Christian Worship","artist":"Hindi Worship","language":"Hindi","category":"Worship","youtube_id":"","emoji":"🎶"},
    {"title":"Hindi Praise and Worship","artist":"Hindi Christian Music","language":"Hindi","category":"Praise","youtube_id":"","emoji":"🙏"},
    {"title":"Kannada Christian Worship","artist":"Kannada Worship","language":"Kannada","category":"Worship","youtube_id":"","emoji":"🕊️"},
    {"title":"Kannada Praise Songs","artist":"Kannada Christian Music","language":"Kannada","category":"Praise","youtube_id":"","emoji":"🎵"},
    {"title":"Alabanzas Cristianas","artist":"Spanish Christian Music","language":"Spanish","category":"Praise","youtube_id":"","emoji":"✨"},
    {"title":"Adoración Cristiana","artist":"Spanish Worship","language":"Spanish","category":"Worship","youtube_id":"","emoji":"🙏"},
    {"title":"Konkani Christian Hymns","artist":"Konkani Worship","language":"Konkani","category":"Hymns","youtube_id":"","emoji":"🕊️"},
    {"title":"Konkani Praise and Worship","artist":"Konkani Christian Music","language":"Konkani","category":"Praise","youtube_id":"","emoji":"🎶"},
]

if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "playlist" not in st.session_state:
    st.session_state.playlist = []
if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

with st.sidebar:
    st.markdown("# 🕊️ WorshipWave")
    st.caption("One Faith. Five Languages.")
    page = st.radio("NAVIGATION", ["🏠 Home", "🔎 Discover", "❤️ Favorites", "📂 My Playlist"])
    st.divider()
    language = st.selectbox("🎵 Choose Language", ["All Languages", *LANGUAGES.keys()])
    category = st.selectbox("🎼 Music Category", ["All Categories", "Worship", "Praise", "Hymns", "Prayer", "Gospel"])
    st.divider()
    st.caption("Christian music only ✝️")
    st.caption("English • Hindi • Kannada")
    st.caption("Spanish • Konkani")

st.markdown("""
<div class="hero">
  <h1>WorshipWave 🕊️</h1>
  <p>One Faith. Five Languages. Endless Worship.</p>
  <p>Discover Christian praise, worship, gospel and hymns.</p>
</div>
""", unsafe_allow_html=True)

search = st.text_input("🔍 Search songs, artists, or worship styles", placeholder="Search Christian music...")

def filter_songs(song_list):
    results = song_list
    if language != "All Languages":
        results = [s for s in results if s["language"] == language]
    if category != "All Categories":
        results = [s for s in results if s["category"] == category]
    if search.strip():
        q = search.strip().lower()
        results = [s for s in results if q in s["title"].lower() or q in s["artist"].lower()
                   or q in s["language"].lower() or q in s["category"].lower()]
    return results

def show_songs(song_list, prefix):
    if not song_list:
        st.info("No songs match these filters. Try another language or search term.")
        return
    for start in range(0, len(song_list), 2):
        cols = st.columns(2)
        for col, song in zip(cols, song_list[start:start+2]):
            with col:
                st.markdown(f"""
                <div class="song-card">
                  <div style="font-size:38px">{song['emoji']}</div>
                  <h3>{song['title']}</h3>
                  <p>{song['artist']}</p>
                  <span class="badge">{LANGUAGES[song['language']]} {song['language']}</span>
                  &nbsp;<span class="badge">{song['category']}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("▶ Play / Open Song", key=f"{prefix}_play_{song['title']}"):
                    st.session_state.selected_song = song
                    st.rerun()
                is_fav = any(x["title"] == song["title"] for x in st.session_state.favorites)
                if st.button("💔 Remove Favorite" if is_fav else "❤️ Add to Favorites", key=f"{prefix}_fav_{song['title']}"):
                    if is_fav:
                        st.session_state.favorites = [x for x in st.session_state.favorites if x["title"] != song["title"]]
                    else:
                        st.session_state.favorites.append(song)
                    st.rerun()
                in_playlist = any(x["title"] == song["title"] for x in st.session_state.playlist)
                if st.button("✓ In Playlist" if in_playlist else "➕ Add to Playlist", key=f"{prefix}_list_{song['title']}"):
                    if not in_playlist:
                        st.session_state.playlist.append(song)
                        st.toast("Added to your playlist!")
                    else:
                        st.toast("This song is already in your playlist.")

if st.session_state.selected_song:
    song = st.session_state.selected_song
    st.divider()
    st.subheader("🎧 Now Playing")
    st.markdown(f"### {song['emoji']} {song['title']}")
    st.write(f"{song['artist']} • {song['language']}")
    if song["youtube_id"].strip():
        components.iframe(f"https://www.youtube-nocookie.com/embed/{song['youtube_id']}", height=380, scrolling=False)
    else:
        st.info("This starter entry has no verified video ID yet. Use the search button below to find an official upload.")
        query = f"{song['title']} {song['artist']} {song['language']} Christian worship official"
        st.link_button("🔎 Find this song on YouTube", "https://www.youtube.com/results?search_query=" + quote_plus(query))
    st.divider()

if page == "🏠 Home":
    st.subheader("✨ Explore Christian Music")
    st.write("Find songs that help you praise, pray, worship, and grow in faith.")
    st.markdown("#### 🌍 Browse by Language")
    cols = st.columns(5)
    for col, lang in zip(cols, LANGUAGES):
        with col:
            st.markdown(f"### {LANGUAGES[lang]}")
            st.caption(lang)
    st.divider()
    st.subheader("🎵 Songs for You")
    show_songs(filter_songs(SONGS), "home")
elif page == "🔎 Discover":
    st.subheader("🔎 Discover Worship Music")
    show_songs(filter_songs(SONGS), "discover")
elif page == "❤️ Favorites":
    st.subheader("❤️ Your Favorite Songs")
    show_songs(filter_songs(st.session_state.favorites), "favorites")
elif page == "📂 My Playlist":
    st.subheader("📂 My Worship Playlist")
    show_songs(filter_songs(st.session_state.playlist), "playlist")
    if st.session_state.playlist and st.button("🗑️ Clear My Playlist"):
        st.session_state.playlist = []
        st.rerun()

st.markdown("""
<div class="footer">
  ✝️ WorshipWave • Made for Christian Music Lovers<br><br>
  Music playback uses official or otherwise authorized sources.
</div>
""", unsafe_allow_html=True)
