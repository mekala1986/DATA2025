import pandas as pd
import gzip
import os

base_path = "data/raw"

basics = pd.read_csv(
    os.path.join(base_path, "title.basics.tsv.gz"),
    sep="\t",
    compression="gzip",
    low_memory=False
)

ratings = pd.read_csv(
    os.path.join(base_path, "title.ratings.tsv.gz"),
    sep="\t",
    compression="gzip"
)

# Filter movies only
basics = basics[basics["titleType"] == "movie"]

# Filter 2024 movies
basics = basics[basics["startYear"] == "2024"]

# Merge ratings
df = basics.merge(ratings, on="tconst", how="left")

final_df = df[[
    "primaryTitle",
    "genres",
    "averageRating",
    "numVotes",
    "runtimeMinutes"
]]

final_df.columns = [
    "movie_name",
    "genre",
    "rating",
    "votes",
    "duration_minutes"
]

final_df.to_csv("data/raw/imdb_2024_raw.csv", index=False)

print("✅ 2024 IMDb movies saved:", len(final_df))
