import os
import pandas as pd

# Paths
metadata_path = "movie_metadata.csv"
trends_folder = "movie-files"

# Load movie titles from metadata
metadata = pd.read_csv(metadata_path)
movie_titles = metadata["Title"].tolist()

# Helper to clean and match movie titles
def clean_title(s):
    return s.lower().replace(" ", "").replace(":", "").replace("(", "").replace(")", "").replace("*", "")

# Process each CSV file in the folder
for filename in os.listdir(trends_folder):
    if not filename.startswith("multiTimeline"):
        continue

    file_path = os.path.join(trends_folder, filename)

    try:
        # Read with header skip and guess the correct title
        raw_df = pd.read_csv(file_path, skiprows=1)

        # Guess the movie title from the column
        trend_column = raw_df.columns[1]  # usually like 'Barbie: (United States)'
        base_title = trend_column.split(":")[0].strip()

        # Try to match it against known titles
        match = None
        for title in movie_titles:
            if clean_title(base_title) in clean_title(title):
                match = title
                break

        if not match:
            print(f"❌ No match found for: {base_title} in file {filename}")
            continue

        # Rename and fix headers
        df = raw_df.rename(columns={raw_df.columns[0]: "Day", raw_df.columns[1]: match})
        new_filename = f"trends_{match.replace(' ', '_').replace(':', '').replace('*', '')}.csv"
        new_path = os.path.join(trends_folder, new_filename)

        df.to_csv(new_path, index=False)
        os.remove(file_path)
        print(f"✅ Renamed and fixed: {filename} -> {new_filename}")

    except Exception as e:
        print(f"⚠️ Error processing {filename}: {e}")
