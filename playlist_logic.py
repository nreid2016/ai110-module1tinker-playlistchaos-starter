import random
from typing import Dict, List, Optional, Tuple

Song = Dict[str, object]
PlaylistMap = Dict[str, List[Song]]

DEFAULT_PROFILE = {
    "name": "Default",
    "hype_min_energy": 7,
    "chill_max_energy": 3,
    "favorite_genre": "rock",
    "include_mixed": True,
}


def normalize_title(title: str) -> str:
    """Normalize a song title for comparisons."""
    return title.strip() if isinstance(title, str) else ""


def normalize_artist(artist: str) -> str:
    """Normalize an artist name for comparisons."""
    return artist.strip().lower() if isinstance(artist, str) else ""


def normalize_genre(genre: str) -> str:
    """Normalize a genre name for comparisons."""
    return genre.strip().lower() if isinstance(genre, str) else ""


def normalize_song(raw: Song) -> Song:
    """Return a normalized song dict with expected keys."""
    title = normalize_title(str(raw.get("title", "")))
    artist = normalize_artist(str(raw.get("artist", "")))
    genre = normalize_genre(str(raw.get("genre", "")))
    energy = raw.get("energy", 0)

    if isinstance(energy, str):
        try:
            energy = int(energy.strip())
        except ValueError:
            energy = 0

    tags = raw.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    tags = [str(tag).strip().lower() for tag in tags if str(tag).strip()]

    return {"title": title, "artist": artist, "genre": genre, "energy": energy, "tags": tags}


def classify_song(song: Song, profile: Dict[str, object]) -> str:
    """Return a mood label given a song and user profile."""
    energy = song.get("energy", 0)
    genre = normalize_genre(str(song.get("genre", "")))
    title = normalize_title(str(song.get("title", ""))).lower()
    hype_min_energy = int(profile.get("hype_min_energy", 7))
    chill_max_energy = int(profile.get("chill_max_energy", 3))
    favorite_genre = normalize_genre(str(profile.get("favorite_genre", "")))

    hype_keywords = ["rock", "punk", "party"]
    chill_keywords = ["lofi", "lo-fi", "ambient", "sleep"]

    if genre == favorite_genre or energy >= hype_min_energy or any(k in genre for k in hype_keywords):
        return "Hype"
    if energy <= chill_max_energy or any(k in title for k in chill_keywords):
        return "Chill"
    return "Mixed"


def build_playlists(songs: List[Song], profile: Dict[str, object]) -> PlaylistMap:
    """Group songs into playlists based on mood and profile."""
    playlists: PlaylistMap = {"Hype": [], "Chill": [], "Mixed": []}
    for song in songs:
        normalized = normalize_song(song)
        normalized["mood"] = classify_song(normalized, profile)
        playlists[normalized["mood"]].append(normalized)
    return playlists


def _song_key(song: Song) -> Tuple[str, str, str]:
    return (normalize_title(str(song.get("title", ""))).lower(), str(song.get("artist", "")).lower(), str(song.get("genre", "")).lower())


def _unique_songs(songs: List[Song]) -> List[Song]:
    """Return songs with duplicate title/artist/genre records removed."""
    unique: List[Song] = []
    seen = set()
    for song in songs:
        key = _song_key(song)
        if key not in seen:
            seen.add(key)
            unique.append(song)
    return unique


def merge_playlists(a: PlaylistMap, b: PlaylistMap) -> PlaylistMap:
    """Merge playlist maps without mutating either input map."""
    merged: PlaylistMap = {}
    for key in set(a) | set(b):
        merged[key] = _unique_songs(a.get(key, []) + b.get(key, []))
    return merged


def compute_playlist_stats(playlists: PlaylistMap) -> Dict[str, object]:
    """Compute statistics across unique songs in all playlists."""
    all_songs = _unique_songs([song for songs in playlists.values() for song in songs])
    hype = _unique_songs(playlists.get("Hype", []))
    chill = _unique_songs(playlists.get("Chill", []))
    mixed = _unique_songs(playlists.get("Mixed", []))
    total = len(all_songs)
    hype_ratio = len(hype) / total if total else 0.0
    avg_energy = sum(int(song.get("energy", 0)) for song in all_songs) / total if total else 0.0
    top_artist, top_count = most_common_artist(all_songs)
    return {"total_songs": total, "hype_count": len(hype), "chill_count": len(chill), "mixed_count": len(mixed), "hype_ratio": hype_ratio, "avg_energy": avg_energy, "top_artist": top_artist, "top_artist_count": top_count}


def most_common_artist(songs: List[Song]) -> Tuple[str, int]:
    """Return the most common artist and count."""
    counts: Dict[str, int] = {}
    for song in songs:
        artist = str(song.get("artist", ""))
        if artist:
            counts[artist] = counts.get(artist, 0) + 1
    return max(counts.items(), key=lambda item: item[1]) if counts else ("", 0)


def search_songs(songs: List[Song], query: str, field: str = "artist") -> List[Song]:
    """Return songs where the query is contained in the selected field."""
    q = query.strip().lower()
    if not q:
        return songs
    return [song for song in songs if q in str(song.get(field, "")).lower()]


def lucky_pick(playlists: PlaylistMap, mode: str = "any") -> Optional[Song]:
    """Pick a song from the requested playlist, or all playlists for any mode."""
    if mode == "hype":
        songs = playlists.get("Hype", [])
    elif mode == "chill":
        songs = playlists.get("Chill", [])
    else:
        songs = playlists.get("Hype", []) + playlists.get("Chill", []) + playlists.get("Mixed", [])
    return random_choice_or_none(songs)


def random_choice_or_none(songs: List[Song]) -> Optional[Song]:
    """Return a random song, or None when the playlist is empty."""
    return random.choice(songs) if songs else None


def history_summary(history: List[Song]) -> Dict[str, int]:
    """Return a summary of moods seen in the history."""
    counts = {"Hype": 0, "Chill": 0, "Mixed": 0}
    for song in history:
        mood = song.get("mood", "Mixed")
        counts[mood if mood in counts else "Mixed"] += 1
    return counts
