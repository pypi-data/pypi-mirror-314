from collections import Counter


def get_statistics_for_table(
    adjusted_data: list[dict[str, str]],
) -> list[dict[str, str]]:
    named_dogs = [row for row in adjusted_data if row["HundenameText"] != "?"]
    unnamed_dogs = [row for row in adjusted_data if row["HundenameText"] == "?"]

    male_named_dogs = [
        row["HundenameText"] for row in named_dogs if row["SexHundCd"] == "1"
    ]
    female_named_dogs = [
        row["HundenameText"] for row in named_dogs if row["SexHundCd"] == "2"
    ]

    longest_dog_name = max(
        (row["HundenameText"] for row in named_dogs), key=len, default="Not known"
    )
    shortest_dog_name = min(
        (row["HundenameText"] for row in named_dogs), key=len, default="Not known"
    )

    top_ten_common_dog_names = Counter(
        [row["HundenameText"] for row in named_dogs]
    ).most_common(10)
    top_ten_female_dog_names = Counter(female_named_dogs).most_common(10)
    top_ten_male_dog_names = Counter(male_named_dogs).most_common(10)

    total_dogs = len(adjusted_data)
    total_named_dogs = len(named_dogs)
    total_unnamed_dogs = len(unnamed_dogs)
    total_male_dogs = len(male_named_dogs)
    total_female_dogs = len(female_named_dogs)

    statistics_data = [
        {"Statistic": "Total Dogs", "Value": str(total_dogs)},
        {"Statistic": "Total Named Dogs", "Value": str(total_named_dogs)},
        {"Statistic": "Total Unnamed Dogs", "Value": str(total_unnamed_dogs)},
        {"Statistic": "Total Male Dogs", "Value": str(total_male_dogs)},
        {"Statistic": "Total Female Dogs", "Value": str(total_female_dogs)},
        {"Statistic": "Longest Name", "Value": longest_dog_name},
        {"Statistic": "Shortest Name", "Value": shortest_dog_name},
    ]

    # Add Top Names
    statistics_data.extend(
        {"Statistic": f"Top {i+1} Most Common Name", "Value": f"{name} ({count})"}
        for i, (name, count) in enumerate(top_ten_common_dog_names)
    )
    statistics_data.extend(
        {"Statistic": f"Top {i+1} Female Name", "Value": f"{name} ({count})"}
        for i, (name, count) in enumerate(top_ten_female_dog_names)
    )
    statistics_data.extend(
        {"Statistic": f"Top {i+1} Male Name", "Value": f"{name} ({count})"}
        for i, (name, count) in enumerate(top_ten_male_dog_names)
    )

    return statistics_data
