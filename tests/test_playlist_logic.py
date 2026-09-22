import pytest

from playlist_logic import (
    DEFAULT_PROFILE,
    build_playlists,
    classify_song,
    compute_playlist_stats,
    lucky_pick,
    normalize_song,
    search_songs,
)


def song(title='Track', artist='Artist', genre='pop', energy=5):
    return {'title': title, 'artist': artist, 'genre': genre, 'energy': energy, 'tags': []}


def test_classification_uses_case_insensitive_keywords_and_profile():
    assert classify_song(song(genre=' ROCK ', energy=4), DEFAULT_PROFILE) == 'Hype'
    assert classify_song(song(title='Late Night Lofi', genre='other', energy=5), DEFAULT_PROFILE) == 'Chill'


def test_normalization_cleans_user_input():
    result = normalize_song({'title': '  Track  ', 'artist': '  DJ Test ', 'genre': ' POP ', 'energy': '7', 'tags': [' Dance ', '']})
    assert result == {'title': 'Track', 'artist': 'dj test', 'genre': 'pop', 'energy': 7, 'tags': ['dance']}


def test_search_uses_query_inside_field():
    songs = [song(title='Thunder', artist='AC/DC'), song(title='Soft', artist='DJ Calm')]
    assert [x['title'] for x in search_songs(songs, 'AC', 'artist')] == ['Thunder']


def test_stats_use_all_unique_songs_and_all_energy_values():
    playlists = build_playlists([song('A', energy=10), song('B', energy=2), song('C', energy=5)], DEFAULT_PROFILE)
    stats = compute_playlist_stats(playlists)
    assert stats['total_songs'] == 3
    assert stats['avg_energy'] == pytest.approx(17 / 3)
    assert stats['hype_ratio'] == pytest.approx(1 / 3)


def test_lucky_pick_empty_playlist_returns_none_and_any_includes_mixed():
    assert lucky_pick({'Hype': [], 'Chill': [], 'Mixed': []}, 'hype') is None
    mixed = song('Mixed Track', energy=5)
    assert lucky_pick({'Hype': [], 'Chill': [], 'Mixed': [mixed]}, 'any') == mixed
