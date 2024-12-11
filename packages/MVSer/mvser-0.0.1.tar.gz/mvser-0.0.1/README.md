# MVSer (Movie and Music Tracker)

[![Build Status](https://app.travis-ci.com/TenTen-Teng/MVSer.svg?token=1PJB3dvKbCVRgPaN4tdQ&branch=main)](https://app.travis-ci.com/TenTen-Teng/MVSer)

- [MVSer (Movie and Music Tracker)](#mvser-movie-and-music-tracker)
  - [Structure](#structure)
    - [Sub-packages](#sub-packages)
      - [movie.py](#moviepy)
        - [Module: MVS](#module-mvs)
        - [Module: Movie](#module-movie)
      - [music\_user.py](#music_userpy)
        - [Module: Music](#module-music)
        - [Module: User](#module-user)
  - [How to use](#how-to-use)
    - [Set up appropriate API keys](#set-up-appropriate-api-keys)
    - [Steps](#steps)

MVSer stands for **M**o**v**ie and Mu**s**ic Track**er**. It is a Python package designed to help users search for music featured in movies, explore detailed movie and music information, and get recommendations. Using public APIs like TMDB and Spotify, MVSer offers a seamless experience that combines movie and music data tailored to the user's preferences.

## Structure

![MVSer](./img/MVSer.png)

There are two sub-packages in this package, `movie` and `music_user` respectively. 

### Sub-packages

#### movie.py
Sub-package, `movie` is used to search movie information from TMDB public API, and parse API response based on user inputs and preferences. This sub-package also recommands the most trendy movies.

##### Module: MVS
> This module inherits functionality from the Movie and Music modules.

Belongs to `movie.py` sub-package.

**Main functions**:
- `return_movie_results`: Call `Movie` class to search for movie information based on user inputs and preferences. Return a dictionary of results.
- `return_music_results`: Call `Music` class to search related music information based on user inputs and preferences. Return a list of results.
- `return_recom`: Call recommandation functions from both classes. Return a tuple of lists for movie and music recommendations..
- `display_movie_details`: Display movie results.
- `display_music_details`: Display music results.
- `decoration`: Display a pretty layout.
- `start`: Start function for MVSer package.

##### Module: Movie
Belongs to `movie.py` sub-package.

**Main functions**:
- `movie_search`: Fetch movies and extract useful information.
- `movie_recom`: Fetch recommendations and extract useful information.
- `fetch_movie`: Call TMDB API to get movie information. 
- `fetch_collection`: Call TMDB to get movie collection information.
- `fetch_recom`: Call TMDB API to get movie recommendations.
- `movie_parse_response`: Extract information from API response and wrap up results into a dictionary.
- `test_api_connection`: Test API connection.

#### music_user.py
Sub-package, `music_user` is used to search related music information from Spoify public API and parse API response based on user inputs and preferences. This sub-package also recommends same artist's music.

##### Module: Music
Belongs to `music_user.py` sub-package.

**Main functions**:
- `music_search`: Fetch music albums and extract useful information.
- `fetch_music`: Call Spotify API to get raw album data.
- `music_recom`: Fetch recommendations and extract useful information.
- `fetch_recommendations`: Call Spotify API to get recommended albums.
- `music_parse_response`: Extract information from the API response and wrap up results into a dictionary.

##### Module: User
Belongs to `music_user.py` sub-package.

**Main functions**:
- `user_input`: Collect user preferences interactively through prompts.
- `check_inputs`: Validate user preferences for correctness.
- `display_preference`: Display the current user preferences.

## How to use

### Set up appropriate API keys

To access [TMDB API](https://developer.themoviedb.org/reference/intro/getting-started) and [Spotify API](https://developer.spotify.com/), available API keys are necessary. You can register to TMDB [here](https://developer.themoviedb.org/docs/getting-started) to get your own API Key, and [here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) to register a client ID and client secret for Spoify API.

> [!TIP]
> We have attached our test API keys on Canvas for testing purposes. Please use them if you don't want to create your own. :)

### Steps
1. Save your API keys as environment variables. MVSer will fetch API keys accordingly. 

```bash
# In console.
export TMDB_API_KEY=<your_TMDB_API_token>
export SPOTIFY_CLIENT_ID=<your_spotipy_client_id>
export SPOTIFY_CLIENT_SECRET=<your_spotify_client_secert>
```

2. Run MVSer

```python
from movie.mvs import MVS

mvser = MVS()
mvser.start()
```

>[!NOTE]
> Please see [test.ipynb](./src/test.ipynb) as exmaple to call MVSer package.