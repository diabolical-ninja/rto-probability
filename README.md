# RTO Interaction Probability

Simple question: If two employees are told to work from the office N-days per week, what is the likelihood they attend on the same days?

This is a very simple analysis to calculate this probability and generalise for scenarios 2 workers to 10 and 1 day/wk to 5. 


# To Run

## Optimal (Recommended) - Exact Mathematical Calculation
```sh
poetry install
poetry run python analysis_optimal.py  # ~1 second, exact results
```

## Original - Monte Carlo Simulation
```sh
poetry run python analysis.py  # Much slower, approximate results
```

## Validation
Compare both methods:
```sh
poetry run python validate_optimal.py
```

# Implementation

## `src/simulator.py` (Original)
Uses Monte Carlo simulation with 500,000 iterations per configuration. Slow but intuitive.

## `src/simulator_optimal.py` (New)
Uses exact combinatorial mathematics:
- **"all_days"**: Probability = `1 / C(5, days_per_week)^(num_teams-1)`
- **"at_least_1_day"**: Uses inclusion-exclusion principle to count favorable outcomes

Performance: **~119,000x faster** with exact (not approximate) results. 