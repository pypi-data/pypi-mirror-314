# music.py

import os

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except ModuleNotFoundError:
    print(
        "Warning: module 'spotipy' is not installed. To install, please run "
        "'pip install spotipy'. For more detail, please see "
        "https://github.com/spotipy-dev/spotipy"
            )

class Music:
    """Music class for handling Spotify API interactions."""

    def __init__(self):
        """Initialize Spotify API client using environment variables."""
        # Fetch Spotify credentials from the environment
        client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not set. Use %env to set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.")

        # Initialize Spotipy client
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def music_search(self, movie_name: str = None, user_preference: dict = {}) -> list:
        """
        Search music information from Spotify API using user input.

        Args:
            movie_name (str, optional): The movie name. Defaults to None.
            user_preference (dict, optional): A dictionary of user preferences. Defaults to {}.

        Returns:
            list: A list of music information related to user input.
        """
        try:
            music_response = self.fetch_music(movie_name)
            return self.music_parse_response(
                music_response=music_response,
                num_results=user_preference.get("num_results", 3)
            )
        except Exception as e:
            print(f"Error during music search: {e}")
            return []

    def fetch_music(self, movie_name: str = None) -> dict:
        """
        Fetch basic music information from Spotify API.

        Args:
            movie_name (str): The movie name.

        Returns:
            dict: The response dictionary from the Spotify API.
        """
        try:
            result = self.sp.search(q=f"{movie_name} soundtrack", type="album", limit=10)
            return result
        except Exception as e:
            print(f"Error fetching music data: {e}")
            return {}

    def music_recom(self, recom_preference: dict = {}) -> list:
        """
        Get music recommendations.

        Args:
            recom_preference (dict): The user preferences dictionary.

        Returns:
            list: A list of recommended music albums.
        """
        try:
            recom_response = self.fetch_recommendations(recom_preference)
            return self.music_parse_response(
                music_response=recom_response,
                num_results=recom_preference.get("num_recom", 3)
            )
        except Exception as e:
            print(f"Error during music recommendations: {e}")
            return []

    def fetch_recommendations(self, recom_preference: dict) -> dict:
        """
        Fetch music recommendations based on user input.

        Args:
            recom_preference (dict): The user preference dictionary.

        Returns:
            dict: The response dictionary from the Spotify API.
        """
        try:
            # genre = recom_preference.get("genre", "pop")
            if not recom_preference["genre"]:
                genre = "pop"
            else:
                genre = recom_preference["genre"]
                
            result = self.sp.search(q=genre, type="album", limit=recom_preference.get("num_recom", 3))
            return result
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return {}

    def music_parse_response(self, music_response: dict, num_results: int = 3) -> list:
        """
        Parse API response to extract relevant music information.

        Args:
            music_response (dict): The API response.
            num_results (int, optional): The number of results to return. Defaults to 3.

        Returns:
            list: A list of dictionaries with music details.
        """
        albums = music_response.get("albums", {}).get("items", [])
        music_results = []
        for album in albums[:num_results]:
            album_info = {
                "album_urls": album['external_urls']['spotify'],  # Spotify album URL
                "img_url": album['images'][0]['url'] if album['images'] else None,  # Album cover image URL
                "name": album['name'],  # Album name
                "release_date": album.get('release_date', 'Unknown'),  # Release date of the album
                "artists": ", ".join([artist['name'] for artist in album['artists']])  # Comma-separated list of artists
            }
            music_results.append(album_info)
        return music_results