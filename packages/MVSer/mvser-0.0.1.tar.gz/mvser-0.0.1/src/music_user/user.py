# user.py

class User:
    """
    A class to handle user preferences and input for the music recommendation system.
    """

    def __init__(self):
        """
        Initializes user attributes and preferences with default values.
        """
        self.movie_name = "Harry Potter"  # Default test movie name
        self.preference = {               # Default test preferences
            "num_results": 3,
            "music_version": "clean",
            "movie_genre": None,
            "music_genre": None,
            "is_recom": {
                "recom_type": "Both", 
                "num_recom": 3,
                "genre": "pop"
            }
        }

    def user_input(self):
        """
        Collects user preferences interactively through prompts.
        """
        # Movie Name
        self.movie_name = input("Enter the movie name (default: Harry Potter): ") or self.movie_name

        # Number of Results
        try:
            self.preference["num_results"] = int(input("Enter number of results to display (default: 3): ") or 3)
        except ValueError:
            print("Invalid input. Using default value of 3.")

        # Music Version
        self.preference["music_version"] = input(
            "Enter music version (clean/explicit, default: clean): "
        ) or "clean"

        # Recommendation Type
        self.preference["is_recom"]["recom_type"] = input(
            "Enter recommendation type (Music/Movie/Both, default: Both): "
        ) or "Both"

        # Number of Recommendations
        try:
            self.preference["is_recom"]["num_recom"] = int(
                input("Enter number of recommendations (default: 3): ") or 3
            )
        except ValueError:
            print("Invalid input. Using default value of 3.")

        # Recommendation Genre
        self.preference["is_recom"]["genre"] = input(
            "Enter genre for recommendations (e.g., Pop, Rock, default: pop): "
        ) or None

        print("User preferences updated successfully!")

    def check_inputs(self, user_preference: dict):
        """
        Validates the user preferences.

        Args:
            user_preference (dict): User's preference dictionary.
        """
        if not isinstance(user_preference.get("num_results"), int) or user_preference["num_results"] <= 0:
            raise ValueError("Invalid 'num_results'. It must be a positive integer.")

        if user_preference["is_recom"]["recom_type"] not in ["Music", "Movie", "Both"]:
            raise ValueError("Invalid 'recom_type'. Must be 'Music', 'Movie', or 'Both'.")

    def display_preference(self):
        """
        Displays the user's preferences in a readable format.
        """
        print("Movie Name:", self.movie_name)
        print("User Preferences:")
        for key, value in self.preference.items():
            print(f"{key}: {value}")