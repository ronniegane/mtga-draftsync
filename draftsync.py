import csv
import requests
import time


CSV_FIELD_NAMES = [
    "idArena",
    "name",
    "rating",
    "color",
    "rarity",
]  # Fields to include from 17Lands


def main():
    expansion = "MID"
    format = "PremierDraft"

    # Grab data from 17Lands
    outputFilename = f"17-lands-{expansion}-{format}.csv"
    fetch17LandsRatings(expansion, format, outputFilename)
    print(f"17Lands ratings output to {outputFilename}")

    ratingsFile = input("CSV file to load from:")
    # Parse CSV
    ratings = parseCSV(ratingsFile)

    # Upload to MTGAHelper endpoint
    userId = input("Enter your MTGAHelper user ID (from your Profile page):")
    upload(userId, ratings)


def fetch17LandsRatings(expansion, format, outputFilename):
    # Fetch latest data
    queryParams = {
        "expansion": expansion,
        "format": format,
        "start_date": "2021-01-01",
        "end_date": "2021-10-09",
    }
    response = requests.get(
        "https://www.17lands.com/card_ratings/data", params=queryParams
    )

    cardRatings = response.json()

    for card in cardRatings:
        # Calculate a 1-10 rating based on winrate
        card["rating"] = rateCard(card)
        # Lookup the card's MTG Arena id
        card["idArena"] = 12345

    # Write to CSV
    with open(outputFilename, "w") as csvFile:
        writer = csv.DictWriter(
            csvFile, fieldnames=CSV_FIELD_NAMES, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(cardRatings)
    print("done")


def rateCard(card):
    # Turn 17Lands card statistics
    return 5


def parseCSV(filename):
    with open(filename) as f:
        ratings = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)
        ]
    return ratings


def upload(userId, ratings):
    cookies = {"userId": userId}
    totalTime = 0
    for i in range(len(ratings)):
        card = ratings[i]
        print(f"uploading card {i+1}/{len(ratings)}: {card['name']}")
        # Just send the necessary fields
        payload = {
            "idArena": card["idArena"],
            "note": card["note"],
            "rating": card["rating"],
        }
        startTime = time.time()
        requests.put(
            "https://mtgahelper.com/api/User/CustomDraftRating",
            json=payload,
            cookies=cookies,
        )
        duration = time.time() - startTime
        totalTime += duration
        print(f"uploaded in {duration:.3f} seconds")

    print(f"uploaded {len(ratings)} cards in {totalTime:.2f} seconds")


if __name__ == "__main__":
    main()
