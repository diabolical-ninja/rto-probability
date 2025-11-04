from math import comb
from typing import Literal


def calculate_office_overlap_probability(
    num_teams: int,
    days_per_week: int,
    probability_type: Literal["all_days", "at_least_1_day"],
) -> float:
    """Calculate the exact probability of teams being in the office on the same day(s).

    Args:
        num_teams (int): How many teams to consider
        days_per_week (int): The required number of days per week each team is in the office
        probability_type (Literal["all_days", "at_least_1_day"]): Whether to calculate the probability of all teams being in the office:
            - on all of the same day(s) OR
            - at least one day

    Returns:
        float: Probability of teams being in the office on the same day(s).
    """
    TOTAL_DAYS = 5  # Days in a working week

    if probability_type == "all_days":
        return _calculate_all_days_probability(num_teams, days_per_week, TOTAL_DAYS)
    elif probability_type == "at_least_1_day":
        return _calculate_at_least_one_day_probability(
            num_teams, days_per_week, TOTAL_DAYS
        )


def _calculate_all_days_probability(
    num_teams: int, days_per_week: int, total_days: int
) -> float:
    """Calculate probability that all teams have identical schedules.

    Approach:
    - Total possible outcomes: C(5 days in a week, days_per_week)^num_teams
    - Scenarios where all teams pick the same schedule: C(5, days_per_week)
    - Probability: C(5, days_per_week) / C(5, days_per_week)^num_teams
                 = 1 / C(5, days_per_week)^(num_teams - 1)
    """
    total_schedules_per_team = comb(total_days, days_per_week)

    # Probability can only be 1 if there's only 1 team
    if num_teams == 1:
        return 1.0

    probability = 1.0 / (total_schedules_per_team ** (num_teams - 1))

    return probability


def _calculate_at_least_one_day_probability(
    num_teams: int, days_per_week: int, total_days: int
) -> float:
    """Calculate probability that all teams share at least one common day.

    Uses the inclusion-exclusion principle:
    - Let A_i be the event that day i is included in all teams' schedules
    - We want P(A_1 ∪ A_2 ∪ A_3 ∪ A_4 ∪ A_5)

    For k specific days to be in all teams' schedules:
    - Each team must include those k days, then choose (days_per_week - k) from remaining (5 - k) days
    - Number of ways per team: C(5-k, days_per_week - k)
    - Number of ways for all teams: C(5-k, days_per_week - k)^num_teams

    By inclusion-exclusion:
    favorable_outcomes = Σ (-1)^(k+1) * C(5, k) * C(5-k, days_per_week - k)^num_teams
                         k=1 to min(5, days_per_week)
    """
    total_schedules_per_team = comb(total_days, days_per_week)
    total_outcomes = total_schedules_per_team**num_teams

    # Apply inclusion-exclusion principle
    favorable_outcomes = 0
    max_k = min(total_days, days_per_week)

    for k in range(1, max_k + 1):
        # Number of ways to choose which k days must be common
        ways_to_choose_k_days = comb(total_days, k)

        # Number of ways for each team to include those k days and choose the rest
        remaining_days = total_days - k
        days_to_choose = days_per_week - k

        # Check if it's possible to choose the remaining days
        if days_to_choose < 0 or days_to_choose > remaining_days:
            continue

        ways_per_team = comb(remaining_days, days_to_choose)
        ways_all_teams = ways_per_team**num_teams

        # Apply inclusion-exclusion: alternate adding and subtracting
        sign = (-1) ** (k + 1)
        favorable_outcomes += sign * ways_to_choose_k_days * ways_all_teams

    probability = favorable_outcomes / total_outcomes

    return probability
