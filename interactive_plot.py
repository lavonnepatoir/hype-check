import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Paths
metadata_path = "movie_metadata.csv"
csv_folder = "movie-files"
output_path = "interactive_relative_trends.html"

# Read movie metadata
metadata = pd.read_csv(metadata_path)

# Initialize figure
fig = go.Figure()

for _, row in metadata.iterrows():
    title = row["Title"]
    release_date = pd.to_datetime(row["Release Date"])
    filename = f"trends_{title.replace(' ', '_')}.csv"
    full_path = os.path.join(csv_folder, filename)

    if not os.path.exists(full_path):
        print(f"⚠️ File not found: {filename}")
        continue

    try:
        df = pd.read_csv(full_path)
        df.columns = ["Day", "Interest"]  # Normalize headers
        df["Day"] = pd.to_datetime(df["Day"])
        df["day_offset"] = (df["Day"] - release_date).dt.days
        df = df[(df["day_offset"] >= -60) & (df["day_offset"] <= 14)]

        fig.add_trace(go.Scatter(
            x=df["day_offset"],
            y=df["Interest"],
            mode='lines',
            name=title,
            hovertemplate=f"<b>{title}</b><br>Day: %{{x}}<br>Interest: %{{y}}<extra></extra>"
        ))

    except Exception as e:
        print(f"❌ Error processing {title}: {e}")

# Final layout
fig.update_layout(
    title="Interactive Google Trends by Movie",
    xaxis_title="Days from Release (0 = Release Day)",
    yaxis_title="Google Search Interest (0–100)",
    yaxis=dict(range=[0, 105]),
    legend=dict(orientation="h", y=-0.2),
    template="plotly_white"
)

# Save HTML file
fig.write_html(output_path)
print(f"✅ Interactive chart saved to: {os.path.abspath(output_path)}")
