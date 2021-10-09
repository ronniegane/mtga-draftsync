import csv
import requests

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
    expansion = "MID"
    format = "PremierDraft"
    outputFilename = f"17-lands-{expansion}-{format}.csv"

    cardRatings = fetch17LandsRatings(expansion, format)

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

    for card in cardRatings:
        # Calculate a 1-10 rating based on winrate
        card["rating"] = rateCardByLastSeenAt(card, minSeen, maxSeen)
        # Lookup the card's MTG Arena id
        card["idArena"] = 12345
        card[
            "note"
        ] = f"ALSA: {card['avg_seen']:.1f} | OH: {card['opening_hand_win_rate']*100:.1f} | GIH: {card['ever_drawn_win_rate']*100:.1f} | IWD: {card['drawn_improvement_win_rate']*100:.1f}"

    return cardRatings


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
