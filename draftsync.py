import csv
import requests
import time


def main():
    ratingsFile = input("CSV file to load from:")
    # Parse CSV
    with open(ratingsFile) as f:
        ratings = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)
        ]

    # Upload to MTGAHelper endpoint
    userId = input("Enter your MTGAHelper user ID (from your Profile page):")
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