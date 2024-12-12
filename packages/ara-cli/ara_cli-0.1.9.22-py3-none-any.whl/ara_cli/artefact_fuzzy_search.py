import difflib


def suggest_close_name_matches(artefact_name: str, all_artefact_names: list[str]):
    closest_matches = difflib.get_close_matches(artefact_name, all_artefact_names)
    print(f"No match found for artefact with name '{artefact_name}'")
    if not closest_matches:
        return
    print("Closest matches:")
    for match in closest_matches:
        print(f"  - {match}")
