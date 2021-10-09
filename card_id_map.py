import json
import requests

map_filename = "card_map.json"


def main():
    # Fetch latest data from MTGAHelper and stores a cardname -> card id map
    # Note the API call is currently a 1.5MB JSON response
    # so do this sparingly
    print("fetching cardlist from MTGAHelper to build idArena mapping")
    response = requests.get(
        "https://mtgahelper.com/api/User/customDraftRatingsForDisplay"
    )
    card_list = response.json()

    print("generating map")
    # Response is a list of cards and their ratings
    # Turn into a map of cardname -> MTGA card id
    card_map = {}
    for entry in card_list:
        name = entry["card"]["name"]
        id = entry["card"]["idArena"]
        card_map[name] = id

    with open(map_filename, "w") as output:
        json.dump(card_map, output, indent=4, sort_keys=True)

    print(f"map written to {map_filename}")


def load_map():
    with open(map_filename, "r") as map_json:
        card_map = json.load(map_json)
    return card_map


if __name__ == "__main__":
    main()
