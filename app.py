import streamlit as st

from playlist_logic import (
    DEFAULT_PROFILE,
    Song,
    build_playlists,
    compute_playlist_stats,
    history_summary,
    lucky_pick,
    merge_playlists,
    normalize_song,
    search_songs,
)

GENRE_OPTIONS = ["rock", "lofi", "pop", "jazz", "electronic", "ambient", "other"]


def inject_theme():
    """Add the Playlist Chaos visual theme and decorative background."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 12% 12%, rgba(55, 130, 190, .22), transparent 26%),
                radial-gradient(circle at 88% 18%, rgba(126, 55, 180, .22), transparent 28%),
                linear-gradient(145deg, #07111f 0%, #10162d 48%, #180d28 100%);
        }
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: .22;
            background-image: url("data:image/svg+xml,%3Csvg width='900' height='260' viewBox='0 0 900 260' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 150 C120 65 210 230 340 135 S580 70 700 145 S820 210 900 120' fill='none' stroke='%235ddcff' stroke-width='3' stroke-opacity='.55'/%3E%3Cpath d='M0 190 C120 105 210 270 340 175 S580 110 700 185 S820 250 900 160' fill='none' stroke='%23b26cff' stroke-width='2' stroke-opacity='.5'/%3E%3C/svg%3E");
            background-size: cover;
            background-position: center bottom;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(8, 22, 40, .96), rgba(24, 10, 39, .96)); border-right: 1px solid rgba(93, 220, 255, .18); }
        .block-container { position: relative; z-index: 2; }
        .playlist-decor { position: fixed; inset: 0; pointer-events: none; z-index: 1; overflow: hidden; }
        .headphones { position: absolute; top: 7%; left: 4%; font-size: 4.5rem; filter: drop-shadow(0 0 18px #5ddcff); opacity: .8; transform: rotate(-12deg); }
        .storm { position: absolute; top: 8%; right: 7%; font-size: 4rem; filter: drop-shadow(0 0 16px #9c72ff); opacity: .85; }
        .bolt { position: absolute; top: 17%; right: 14%; font-size: 2.8rem; color: #ffe66d; filter: drop-shadow(0 0 16px #ffe66d); animation: pulse 1.8s infinite; }
        .leds { position: absolute; left: 6%; bottom: 8%; display: flex; gap: 12px; }
        .leds i { width: 10px; height: 10px; border-radius: 50%; background: #5ddcff; box-shadow: 0 0 14px 5px #5ddcff; animation: blink 1.7s infinite alternate; }
        .leds i:nth-child(2) { background: #d46cff; box-shadow: 0 0 14px 5px #d46cff; animation-delay: .3s; }
        .leds i:nth-child(3) { background: #ffe66d; box-shadow: 0 0 14px 5px #ffe66d; animation-delay: .6s; }
        .leds i:nth-child(4) { background: #66f2a5; box-shadow: 0 0 14px 5px #66f2a5; animation-delay: .9s; }
        @keyframes pulse { 50% { transform: scale(1.18) rotate(8deg); opacity: .55; } }
        @keyframes blink { from { opacity: .35; } to { opacity: 1; } }
        </style>
        <div class="playlist-decor" aria-hidden="true">
            <div class="headphones">🎧</div>
            <div class="storm">☁️</div>
            <div class="bolt">⚡</div>
            <div class="leds"><i></i><i></i><i></i><i></i></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    """Initialize Streamlit session state."""
    if "songs" not in st.session_state:
        st.session_state.songs = default_songs()
    if "profile" not in st.session_state:
        st.session_state.profile = dict(DEFAULT_PROFILE)
    if "history" not in st.session_state:
        st.session_state.history = []


def default_songs():
    """Return a default list of songs."""
    return [
        {
            "title": "Thunderstruck",
            "artist": "AC/DC",
            "genre": "rock",
            "energy": 9,
            "tags": ["classic", "guitar"],
        },
        {
            "title": "Lo-fi Rain",
            "artist": "DJ Calm",
            "genre": "lofi",
            "energy": 2,
            "tags": ["study"],
        },
        {
            "title": "Night Drive",
            "artist": "Neon Echo",
            "genre": "electronic",
            "energy": 6,
            "tags": ["synth"],
        },
        {
            "title": "Soft Piano",
            "artist": "Sleep Sound",
            "genre": "ambient",
            "energy": 1,
            "tags": ["sleep"],
        },
        {
            "title": "Bohemian Rhapsody",
            "artist": "Queen",
            "genre": "rock",
            "energy": 8,
            "tags": ["classic", "opera"],
        },
        {
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "genre": "pop",
            "energy": 8,
            "tags": ["synth", "dance"],
        },
        {
            "title": "Take Five",
            "artist": "Dave Brubeck",
            "genre": "jazz",
            "energy": 4,
            "tags": ["classic", "instrumental"],
        },
        {
            "title": "Strobe",
            "artist": "Deadmau5",
            "genre": "electronic",
            "energy": 7,
            "tags": ["progressive", "long"],
        },
        {
            "title": "Weightless",
            "artist": "Marconi Union",
            "genre": "ambient",
            "energy": 1,
            "tags": ["relax", "sleep"],
        },
        {
            "title": "Smells Like Teen Spirit",
            "artist": "Nirvana",
            "genre": "rock",
            "energy": 9,
            "tags": ["grunge", "90s"],
        },
        {
            "title": "Levitating",
            "artist": "Dua Lipa",
            "genre": "pop",
            "energy": 8,
            "tags": ["dance", "party"],
        },
        {
            "title": "So What",
            "artist": "Miles Davis",
            "genre": "jazz",
            "energy": 3,
            "tags": ["trumpet", "cool"],
        },
        {
            "title": "Midnight City",
            "artist": "M83",
            "genre": "electronic",
            "energy": 7,
            "tags": ["indie", "dream"],
        },
        {
            "title": "Gymnopedie No.1",
            "artist": "Erik Satie",
            "genre": "ambient",
            "energy": 1,
            "tags": ["piano", "calm"],
        },
        {
            "title": "Sweet Child O' Mine",
            "artist": "Guns N' Roses",
            "genre": "rock",
            "energy": 8,
            "tags": ["guitar", "80s"],
        },
        {
            "title": "Bad Guy",
            "artist": "Billie Eilish",
            "genre": "pop",
            "energy": 6,
            "tags": ["bass", "dark"],
        },
        {
            "title": "Fly Me to the Moon",
            "artist": "Frank Sinatra",
            "genre": "jazz",
            "energy": 5,
            "tags": ["vocal", "swing"],
        },
        {
            "title": "Sandstorm",
            "artist": "Darude",
            "genre": "electronic",
            "energy": 10,
            "tags": ["trance", "meme"],
        },
        {
            "title": "Clair de Lune",
            "artist": "Claude Debussy",
            "genre": "ambient",
            "energy": 2,
            "tags": ["piano", "classical"],
        },
        {
            "title": "Hotel California",
            "artist": "Eagles",
            "genre": "rock",
            "energy": 6,
            "tags": ["classic", "guitar"],
        },
        {
            "title": "Uptown Funk",
            "artist": "Mark Ronson ft. Bruno Mars",
            "genre": "pop",
            "energy": 9,
            "tags": ["funk", "dance"],
        },
        {
            "title": "Feeling Good",
            "artist": "Nina Simone",
            "genre": "jazz",
            "energy": 6,
            "tags": ["soul", "vocal"],
        },
    ]


def profile_sidebar():
    """Render and update the user profile."""
    st.sidebar.header("Mood profile")

    profile = st.session_state.profile

    profile["name"] = st.sidebar.text_input(
        "Profile name",
        value=str(profile.get("name", "")),
    )

    col1, col2 = st.sidebar.columns(2)
    with col1:
        profile["hype_min_energy"] = st.sidebar.slider(
            "Hype min energy",
            min_value=1,
            max_value=10,
            value=int(profile.get("hype_min_energy", 7)),
        )
    with col2:
        profile["chill_max_energy"] = st.sidebar.slider(
            "Chill max energy",
            min_value=1,
            max_value=10,
            value=int(profile.get("chill_max_energy", 3)),
        )

    profile["favorite_genre"] = st.sidebar.selectbox(
        "Favorite genre",
        options=GENRE_OPTIONS,
        index=GENRE_OPTIONS.index(profile.get("favorite_genre", "rock")),
    )

    profile["include_mixed"] = st.sidebar.checkbox(
        "Include Mixed playlist in views",
        value=bool(profile.get("include_mixed", True)),
    )

    st.sidebar.write("Current profile:", profile["name"])


def add_song_sidebar():
    """Render the Add Song controls in the sidebar."""
    st.sidebar.header("Add a song")

    title = st.sidebar.text_input("Title")
    artist = st.sidebar.text_input("Artist")
    genre = st.sidebar.selectbox(
        "Genre",
        options=GENRE_OPTIONS,
    )
    energy = st.sidebar.slider("Energy", min_value=1, max_value=10, value=5)
    tags_text = st.sidebar.text_input("Tags (comma separated)")

    if st.sidebar.button("Add to playlist"):
        raw_tags = [t.strip() for t in tags_text.split(",")]
        tags = [t for t in raw_tags if t]

        song: Song = {
            "title": title,
            "artist": artist,
            "genre": genre,
            "energy": energy,
            "tags": tags,
        }
        if title.strip() and artist.strip():
            normalized = normalize_song(song)
            all_songs = st.session_state.songs[:]
            all_songs.append(normalized)
            st.session_state.songs = all_songs
            st.sidebar.success(f"Added {normalized['title']}.")
        else:
            st.sidebar.error("Title and artist are required.")


def playlist_tabs(playlists):
    """Render playlists in tabs."""
    include_mixed = st.session_state.profile.get("include_mixed", True)

    tab_labels = ["Hype", "Chill"]
    if include_mixed:
        tab_labels.append("Mixed")

    tabs = st.tabs(tab_labels)

    for label, tab in zip(tab_labels, tabs):
        with tab:
            render_playlist(label, playlists.get(label, []))


def render_playlist(label, songs):
    st.subheader(f"{label} playlist")
    if not songs:
        st.write("No songs in this playlist.")
        return

    query = st.text_input(f"Search {label} playlist by artist", key=f"search_{label}")
    filtered = search_songs(songs, query, field="artist")

    if not filtered:
        st.write("No matching songs.")
        return

    for song in filtered:
        mood = song.get("mood", "?")
        tags = ", ".join(song.get("tags", []))
        st.write(
            f"- **{song['title']}** by {song['artist']} "
            f"(genre {song['genre']}, energy {song['energy']}, mood {mood}) "
            f"[{tags}]"
        )


def lucky_section(playlists):
    """Render the lucky pick controls and result."""
    st.header("Lucky pick")

    mode = st.selectbox(
        "Pick from",
        options=["any", "hype", "chill"],
        index=0,
    )

    if st.button("Feeling lucky"):
        pick = lucky_pick(playlists, mode=mode)
        if pick is None:
            st.warning("No songs available for this mode.")
            return

        st.success(
            f"Lucky song: {pick['title']} by {pick['artist']} "
            f"(mood {pick.get('mood', '?')})"
        )

        history = st.session_state.history
        history.append(pick)
        st.session_state.history = history


def stats_section(playlists):
    """Render statistics based on the playlists."""
    st.header("Playlist stats")

    stats = compute_playlist_stats(playlists)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total songs", stats["total_songs"])
    col2.metric("Hype songs", stats["hype_count"])
    col3.metric("Chill songs", stats["chill_count"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Mixed songs", stats["mixed_count"])
    col5.metric("Hype ratio", f"{stats['hype_ratio']:.2f}")
    col6.metric("Average energy", f"{stats['avg_energy']:.2f}")

    top_artist = stats["top_artist"]
    if top_artist:
        st.write(
            f"Most common artist: {top_artist} "
            f"({stats['top_artist_count']} songs)"
        )
    else:
        st.write("No top artist yet.")


def history_section():
    """Render the pick history overview."""
    st.header("History")

    history = st.session_state.history
    if not history:
        st.write("No history yet.")
        return

    summary = history_summary(history)
    st.write("Recent picks by mood:", summary)

    show_details = st.checkbox("Show full history")
    if show_details:
        for song in history:
            st.write(
                f"{song.get('mood', '?')}: {song['title']} by {song['artist']}"
            )


def clear_controls():
    """Render a small section for clearing data."""
    st.sidebar.header("Manage data")
    if st.sidebar.button("Reset songs to default"):
        st.session_state.songs = default_songs()
    if st.sidebar.button("Clear history"):
        st.session_state.history = []


def main():
    st.set_page_config(page_title="Playlist Chaos", layout="wide")
    inject_theme()
    st.title("Playlist Chaos")

    st.write(
        "An AI assistant tried to build a smart playlist engine. "
        "The code runs, but the behavior is a bit unpredictable."
    )

    init_state()
    profile_sidebar()
    add_song_sidebar()
    clear_controls()

    profile = st.session_state.profile
    songs = st.session_state.songs

    base_playlists = build_playlists(songs, profile)
    merged_playlists = merge_playlists(base_playlists, {})

    playlist_tabs(merged_playlists)
    st.divider()
    lucky_section(merged_playlists)
    st.divider()
    stats_section(merged_playlists)
    st.divider()
    history_section()


if __name__ == "__main__":
    main()
