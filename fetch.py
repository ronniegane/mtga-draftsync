import csv
import requests
import card_id_map

CSV_FIELD_NAMES = [
    "idArena",
    "name",
    "rating",
    "note",
    "color",
    "rarity",
]  # Fields to include from 17Lands


def main():
    # If called directly, download and store as CSV
    expansion = (
        input("Enter MTG set to update, or leave blank to default to MID: ") or "MID"
    )
    format = (
        input(
            "Enter draft type to fetch ratings for, or leave blank to default to Premier: "
        )
        or "PremierDraft"
    )
    outputFilename = f"17-lands-{expansion}-{format}.csv"

    rawRatings = fetch17LandsRatings(expansion, format)

    cardRatings = convert17LandsRatings(rawRatings)

    writeToCSV(cardRatings, outputFilename)

    print(f"17Lands ratings output to {outputFilename}")


def fetch17LandsRatings(expansion, format):
    # Fetch latest data
    queryParams = {
        "expansion": expansion,
        "format": format,
        "start_date": "2021-01-01",
        "end_date": "2021-10-09",
    }
    print(f"Set: {expansion} | Format: {format}")
    print("Requesting latest card ratings from 17Lands...")
    response = requests.get(
        "https://www.17lands.com/card_ratings/data", params=queryParams
    )

    cardRatings = response.json()
    print(f"Received ratings for {len(cardRatings)} cards.")
    return cardRatings


def convert17LandsRatings(cardRatings):
    # Find min and max of key states to scale ratings
    minSeen = cardRatings[0]["avg_seen"]
    maxSeen = minSeen
    minWR = cardRatings[0]["win_rate"]
    maxWR = minWR
    for card in cardRatings:
        if card["win_rate"] > maxWR:
            maxWR = card["win_rate"]
        if card["win_rate"] < minWR:
            minWR = card["win_rate"]
        if card["avg_seen"] < minSeen:
            minSeen = card["avg_seen"]
        if card["avg_seen"] > maxSeen:
            maxSeen = card["avg_seen"]

    # Load name-to-arenaID lookup map
    arenaIdLookup = card_id_map.load_map()

    # Return just the fields we are interested in
    convertedRatings = []
    for card in cardRatings:
        newCard = {}
        newCard["name"] = card["name"]
        newCard["color"] = card["color"]
        newCard["rarity"] = card["rarity"]
        # Calculate a 1-10 rating based on winrate
        newCard["rating"] = rateCardByLastSeenAt(card, minSeen, maxSeen)
        # Lookup the card's MTG Arena id
        newCard["idArena"] = arenaIdLookup[card["name"]]
        newCard[
            "note"
        ] = f"ALSA: {card['avg_seen']:.1f} | OH: {card['opening_hand_win_rate']*100:.1f} | GIH: {card['ever_drawn_win_rate']*100:.1f} | IWD: {card['drawn_improvement_win_rate']*100:.1f}"
        convertedRatings.append(newCard)

    return convertedRatings


def rateCardByLastSeenAt(card, minSeen, maxSeen):
    # based on how late a card was still being passed round in packs
    return round(10 - 10 * (card["avg_seen"] - minSeen) / (maxSeen - minSeen))


def writeToCSV(cardRatings, outputFilename):
    with open(outputFilename, "w") as csvFile:
        writer = csv.DictWriter(
            csvFile, fieldnames=CSV_FIELD_NAMES, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(cardRatings)


if __name__ == "__main__":
    main()
