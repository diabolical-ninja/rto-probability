# %%
# create an output directory if it doesn't exist, using python best practices
import os
from itertools import product

import pandas as pd
import plotly.express as px

from src.simulator import calculate_office_overlap_probability

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# %%
# Simulation parameters
MAX_PEOPLE = 10
MAX_DAYS_PER_WEEK = 5
PROBABILITY_TYPE = ["at_least_1_day", "all_days"]

# %%
for prob_type in PROBABILITY_TYPE:

    # Iterate across the number of people & number days per week to build a matrix of probabilities
    matrix_results = []
    for num_people, days_per_week in product(
        range(1, MAX_PEOPLE + 1), range(1, MAX_DAYS_PER_WEEK + 1)
    ):

        sim_stats = {
            "num_people": num_people,
            "days_per_week": days_per_week,
            "probability": calculate_office_overlap_probability(
                num_people, days_per_week, prob_type
            ),
        }

        matrix_results.append(sim_stats)

    matrix_results_df = pd.DataFrame(matrix_results)
    matrix_results_df["probability"] = round(matrix_results_df["probability"] * 100, 2)

    matrix_results_df = matrix_results_df[
        ["days_per_week", "num_people", "probability"]
    ].sort_values(by=["days_per_week", "num_people"])

    # Heatmap the results
    # title = f"Probability of everyone being in the office on the same day {prob_type.replace('_', ' ')} per week"
    fig = px.imshow(
        matrix_results_df["probability"].values.reshape(MAX_DAYS_PER_WEEK, MAX_PEOPLE),
        labels=dict(
            y="Days in the Office per Week",
            x="Number of People",
            color="Probability (%)",
        ),
        x=list(range(1, MAX_PEOPLE + 1)),
        y=list(range(1, MAX_DAYS_PER_WEEK + 1)),
        text_auto=True,
        # title=title,
    )
    fig.update_xaxes(side="bottom", tickmode="linear")
    fig.update_yaxes(tickmode="linear")

    fig.write_html(f"{OUTPUT_DIR}/heatmap_{prob_type}_people_vs_days.html")

print("Analysis complete. Results available in `results/` directory")
