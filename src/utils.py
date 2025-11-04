from random import sample


def generate_in_office_schedule(days_per_week: int) -> set:
    days_of_the_week = [1, 2, 3, 4, 5]
    return set(sample(days_of_the_week, days_per_week))
