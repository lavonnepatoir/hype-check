import os
import csv
import requests
from dotenv import load_dotenv

# === Load TMDb API Key ===
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    print("❌ TMDB API key not loaded.")
    exit()

# === Step 1: Fetch Genre Mapping ===
genre_url = "https://api.themoviedb.org/3/genre/movie/list"
genre_params = {"api_key": API_KEY}
genre_response = requests.get(genre_url, params=genre_params)
genre_map = {}

if genre_response.status_code == 200:
    genre_data = genre_response.json().get("genres", [])
    genre_map = {genre["id"]: genre["name"] for genre in genre_data}
else:
    print("⚠️ Failed to fetch genre mapping.")

# === Movie Titles ===
movie_titles = [
    "Anora",
    "Call Me by Your Name",
    "Barbie",
    "Oppenheimer",
    "Don't Worry Darling",
    "Everything Everywhere All At Once",
    "Ballad of Songbirds and Snakes",
    "Captain America: Brave New World",
    "Thunderbolts*",
    "Wicked",
    "Ant-Man and the Wasp: Quantumania",
    "Birds of Prey and the Fantabulous Emancipation of One Harley Quinn",
    "Thor: Love and Thunder",
    "Mickey 17",
    "Death of a Unicorn",
    "Poor Things",
    "Top Gun Maverick",
    "Don't Look Up",
    "Spider-Man: No Way Home",
    "Dune",
    "The Batman",
    "Guardians of the Galaxy Vol. 3",
    "Doctor Strange in the Multiverse of Madness",
    "Black Panther: Wakanda Forever",
    "The Super Mario Bros. Movie",
    "Avatar: The Way of Water",
    "The Flash",
    "The Little Mermaid",
    "The Marvels",
    "Mission: Impossible – Dead Reckoning Part One",
    "John Wick: Chapter 4",
    "Creed III",
    "The Hunger Games: Mockingjay – Part 2",
    "Inside Out",
    "Coco",
    "Encanto",
    "Turning Red",
    "Soul",
    "Lightyear",
    "Elemental",
    "Wish",
    "Frozen II",
    "Zootopia",
    "Moana",
    "La La Land",
    "A Star is Born",
    "Bohemian Rhapsody",
    "Elvis",
    "Rocketman",
    "Barbarian",
    "Talk to Me",
    "Smile",
    "Nope",
    "Us",
    "Get Out",
    "M3GAN",
    "The Invisible Man",
    "It",
    "It Chapter Two",
    "The Menu",
    "Knives Out",
    "Glass Onion: A Knives Out Mystery",
    "Dungeons & Dragons: Honor Among Thieves",
    "Jumanji: Welcome to the Jungle",
    "Jumanji: The Next Level",
    "Free Guy",
    "Everything, Everything",
    "Love, Simon",
    "To All the Boys I've Loved Before",
    "The Kissing Booth",
    "The Summer I Turned Pretty",
    "Red, White & Royal Blue",
    "The Prom",
    "Tick, Tick... Boom!",
    "The Greatest Showman",
    "Hamilton",
    "In the Heights",
    "West Side Story (2021)",
    "Les Misérables (2019 concert film)",
    "The Banshees of Inisherin",
    "The Whale",
    "Nomadland",
    "CODA",
    "1917",
    "Parasite",
    "The Shape of Water",
    "Three Billboards Outside Ebbing, Missouri",
    "Lady Bird",
    "Marriage Story",
    "The Fabelmans",
    "Air",
    "Tár",
    "Promising Young Woman",
    "The Lost Daughter",
    "The Power of the Dog",
    "Don't Worry Darling",
    "The Last Duel",
    "Eternals",
    "Shang-Chi and the Legend of the Ten Rings",
    "The Suicide Squad",
    "Tenet",
    "The Gentlemen"
]


# === Step 2: Save Metadata ===
with open("movie_metadata.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Release Date", "Popularity", "Vote Average", "Genres"])

    for title in movie_titles:
        search_url = "https://api.themoviedb.org/3/search/movie"
        search_params = {"api_key": API_KEY, "query": title}
        response = requests.get(search_url, params=search_params)

        if response.status_code == 200:
            data = response.json().get("results", [])
            if data:
                movie = data[0]
                genre_ids = movie.get("genre_ids", [])
                genres = [genre_map.get(gid, "Unknown") for gid in genre_ids]
                genre_str = ", ".join(genres)

                writer.writerow([
                    movie["title"],
                    movie["release_date"],
                    movie["popularity"],
                    movie["vote_average"],
                    genre_str
                ])
                print(f"✅ {title} saved with genres: {genre_str}")
            else:
                print(f"⚠️ {title} not found.")
        else:
            print(f"❌ TMDb error for {title}: {response.status_code}")
