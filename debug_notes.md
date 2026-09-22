# Playlist Chaos debugging notes

I tested the starter logic against the behavior rules in the activity.

Issues identified:

1. Search used `value in query` instead of `query in value`, so searching for part of an artist name returned no matches.
2. Playlist statistics calculated total songs from only the Hype playlist and calculated average energy from Hype songs while dividing by all songs.
3. Hype ratio used the Hype count as its denominator instead of total unique songs.
4. Lucky Pick with `any` ignored the Mixed playlist, and an empty playlist could raise an exception instead of returning no result.
5. Input normalization did not consistently clean tags or handle title/genre comparisons case-insensitively.
6. Adding a song with a blank title or artist failed silently in the user interface.

Validation performed:

- Added focused pytest coverage for classification, normalization, partial search, statistics, and Lucky Pick behavior.
- Ran `python3 -m pytest -q`: 5 tests passed.
- Tested the app startup through Streamlit after the fixes.
