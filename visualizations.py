import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# === Paths ===
metadata_path = "movie_metadata.csv"
csv_folder = "movie-files"
line_output = "interactive_relative_trends.html"
scatter_output = "interactive_scatter_rating_vs_interest.html"

# === Load Metadata ===
metadata = pd.read_csv(metadata_path)

# === Interactive Line Plot with Genre Filter (as Checkboxes) ===
def plot_interactive_trends():
    fig = go.Figure()
    buttons = []
    genre_map = {}

    for _, row in metadata.iterrows():
        title = row["Title"]
        release_date = pd.to_datetime(row["Release Date"])
        genre = str(row["Genres"]).split(",")[0].strip() if pd.notna(row["Genres"]) else "Unknown"
        filename = f"trends_{title.replace(' ', '_')}.csv"
        full_path = os.path.join(csv_folder, filename)

        if not os.path.exists(full_path):
            print(f"⚠️ File not found: {filename}")
            continue

        try:
            df = pd.read_csv(full_path)
            df.columns = ["Day", "Interest"]
            df["Day"] = pd.to_datetime(df["Day"])
            df["day_offset"] = (df["Day"] - release_date).dt.days
            df = df[(df["day_offset"] >= -60) & (df["day_offset"] <= 14)]

            visible = True  # default all visible

            trace = go.Scatter(
                x=df["day_offset"],
                y=df["Interest"],
                mode='lines',
                name=title,
                hovertemplate=f"<b>{title}</b><br>Day: %{{x}}<br>Interest: %{{y}}<extra></extra>"
            )
            fig.add_trace(trace)

            # group by genre for visibility filter
            genre_map.setdefault(genre, []).append(len(fig.data) - 1)

        except Exception as e:
            print(f"❌ Error processing {title}: {e}")

    # === Add genre-based checkbox filters ===
    for genre, trace_indices in genre_map.items():
        visibility = [False] * len(fig.data)
        for i in trace_indices:
            visibility[i] = True

        buttons.append(dict(
            label=genre,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Google Trends - Genre: {genre}"}]
        ))

    buttons.insert(0, dict(
        label="All Genres",
        method="update",
        args=[{"visible": [True] * len(fig.data)},
              {"title": "Google Trends by Movie"}]
    ))

    fig.update_layout(
        title="Google Trends by Movie",
        xaxis_title="Days from Release (0 = Release Day)",
        yaxis_title="Google Search Interest (0–100)",
        yaxis=dict(range=[0, 110]),
        legend=dict(orientation="h", y=-0.25),
        template="plotly_white",
        updatemenus=[dict(
            type="buttons",
            direction="down",
            showactive=True,
            buttons=buttons,
            x=1.05,
            y=1.15
        )]
    )

    fig.write_html(line_output)
    print(f"✅ Line chart saved to: {os.path.abspath(line_output)}")

# === Interactive Scatter with Genre Checkboxes ===
def plot_interactive_scatter():
    data = {
        "Title": [],
        "Vote Average": [],
        "Avg Interest": [],
        "Genre": []
    }

    for _, row in metadata.iterrows():
        title = row["Title"]
        vote_avg = row["Vote Average"]
        genre = str(row["Genres"]).split(",")[0].strip() if pd.notna(row["Genres"]) else "Unknown"
        release_date = pd.to_datetime(row["Release Date"])
        filename = f"trends_{title.replace(' ', '_')}.csv"
        filepath = os.path.join(csv_folder, filename)

        if not os.path.exists(filepath):
            continue

        try:
            df = pd.read_csv(filepath)
            df.columns = ["Day", "Interest"]
            df["Day"] = pd.to_datetime(df["Day"])
            df["day_offset"] = (df["Day"] - release_date).dt.days
            df = df[(df["day_offset"] >= -60) & (df["day_offset"] <= 14)]

            avg_interest = df["Interest"].mean()

            data["Title"].append(title)
            data["Vote Average"].append(vote_avg)
            data["Avg Interest"].append(avg_interest)
            data["Genre"].append(genre)

        except Exception as e:
            print(f"⚠️ Error in {title}: {e}")

    df_final = pd.DataFrame(data)
    genre_list = sorted(df_final["Genre"].unique())

    fig = px.scatter(
        df_final,
        x="Vote Average",
        y="Avg Interest",
        color="Genre",
        hover_name="Title",
        title="TMDb Score vs Avg Google Trends Interest by Genre",
        labels={"Avg Interest": "Avg Google Search Interest"},
        template="plotly_white"
    )

    # Checkbox filter by genre
    buttons = [{
        "label": "All Genres",
        "method": "restyle",
        "args": [{"visible": [True] * len(fig.data)}]
    }]

    for i, genre in enumerate(genre_list):
        visibility = [trace.name == genre for trace in fig.data]
        buttons.append({
            "label": genre,
            "method": "restyle",
            "args": [{"visible": visibility}]
        })

    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            direction="down",
            showactive=True,
            buttons=buttons,
            x=1.05,
            y=1.15
        )]
    )

    fig.write_html(scatter_output)
    print(f"✅ Scatter chart saved to: {os.path.abspath(scatter_output)}")

# === Run ===
if __name__ == "__main__":
    plot_interactive_trends()
    plot_interactive_scatter()
