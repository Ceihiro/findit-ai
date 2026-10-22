"""Shared settings. Teammates: change values here, not inside the other files."""

CATEGORIES = [
    "Umbrella", "Water bottle", "Flash drive", "Charger", "Calculator",
    "ID / Card", "Bag", "Notebook / Book", "Keys", "Other",
]

COLORS = [
    "Black", "White", "Gray", "Blue", "Red", "Green",
    "Yellow", "Brown", "Pink", "Purple", "Orange", "Other",
]

# Edit this list to match the real KLL rooms.
LOCATIONS = [
    "Lab 1", "Lab 2", "Lab 3", "Room 101", "Room 102", "Room 201",
    "Room 202", "Hallway", "Faculty room", "Other",
]

# How much each attribute counts in the attribute score (must add up to 1.0).
ATTRIBUTE_WEIGHTS = {
    "category": 0.30,
    "color": 0.20,
    "brand": 0.10,
    "location": 0.20,
    "time": 0.20,
}

# Final score = ATTRIBUTE_SHARE * attribute score + TEXT_SHARE * text score.
ATTRIBUTE_SHARE = 0.5
TEXT_SHARE = 0.5

# A found item more than this many hours away from the lost time scores 0 on "time".
TIME_WINDOW_HOURS = 72

# How many suggestions to show per lost report.
TOP_N = 3
