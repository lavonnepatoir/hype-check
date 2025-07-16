import os
import pandas as pd

metadata_path = "movie_metadata.csv"
trends_folder = "movie-files"

metadata = pd.read_csv(metadata_path)
movie_titles = metadata["Title"].tolist()

def clean_title(s):
    return s.lower().replace(" ", "").replace(":", "").replace("(", "").replace(")", "").replace("*", "")

for filename in os.listdir(trends_folder):
    if not filename.startswith("multiTimeline"):
        continue

    file_path = os.path.join(trends_folder, filename)

    try:
        raw_df = pd.read_csv(file_path, skiprows=1)

        trend_column = raw_df.columns[1] 
        base_title = trend_column.split(":")[0].strip()

        match = None
        for title in movie_titles:
            if clean_title(base_title) in clean_title(title):
                match = title
                break

        if not match:
            print(f"❌ No match found for: {base_title} in file {filename}")
            continue

        df = raw_df.rename(columns={raw_df.columns[0]: "Day", raw_df.columns[1]: match})
        new_filename = f"trends_{match.replace(' ', '_').replace(':', '').replace('*', '')}.csv"
        new_path = os.path.join(trends_folder, new_filename)

        df.to_csv(new_path, index=False)
        os.remove(file_path)
        print(f"✅ Renamed and fixed: {filename} -> {new_filename}")

    except Exception as e:
        print(f"⚠️ Error processing {filename}: {e}")
