# %%
# %%
# create an output directory if it doesn't exist, using python best practices
import os
from itertools import product

import pandas as pd
import plotly.express as px

from src.simulator import calculate_office_overlap_probability

output_dir = "results"
os.makedirs(output_dir, exist_ok=True)


# %%
# Simulation parameters
MAX_TEAMS = 10
MAX_DAYS_PER_WEEK = 5
PROBABILITY_TYPE = ["at_least_1_day", "all_days"]

# %%

for prob_type in PROBABILITY_TYPE:

    # Iterate across the number of teams & number days per week to build a matrix of probabilities
    matrix_results = []
    for num_teams, days_per_week in product(
        range(1, MAX_TEAMS + 1), range(1, MAX_DAYS_PER_WEEK + 1)
    ):

        sim_stats = {
            "num_teams": num_teams,
            "days_per_week": days_per_week,
            "probability": calculate_office_overlap_probability(
                num_teams, days_per_week, prob_type
            ),
        }

        matrix_results.append(sim_stats)

    matrix_results_df = pd.DataFrame(matrix_results)
    matrix_results_df["probability"] = round(matrix_results_df["probability"] * 100, 2)

    matrix_results_df = matrix_results_df[
        ["days_per_week", "num_teams", "probability"]
    ].sort_values(by=["days_per_week", "num_teams"])

    # Heatmap the results
    title = f"Probability of teams being in the office {prob_type.replace('_', ' ')}"
    fig = px.imshow(
        matrix_results_df["probability"].values.reshape(MAX_DAYS_PER_WEEK, MAX_TEAMS),
        labels=dict(
            y="Days in the Office per Week",
            x="Number of Teams",
            color="Probability (%)",
        ),
        x=list(range(1, MAX_TEAMS + 1)),
        y=list(range(1, MAX_DAYS_PER_WEEK + 1)),
        text_auto=True,
        title=title,
    )
    fig.update_xaxes(side="bottom", tickmode="linear")
    fig.update_yaxes(tickmode="linear")

    fig.write_html(f"{output_dir}/heatmap_{prob_type}_teams_vs_days_optimal.html")

print("Analysis complete. Results available in results/ directory")

# %%
