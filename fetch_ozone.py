import json
import os
import requests
from datetime import datetime, timedelta

CACHE_FILE = 'ozone_cache.json'
DEPLETED_FLOOR = 100
HEALTHY_TARGET = 300

# NASA Ozone Watch — daily minimum ozone DU over Antarctica (current year)
OZONE_URL = 'https://ozonewatch.gsfc.nasa.gov/meteorology/figures/ozone/to3mins_2026_toms+omi+omps.txt'

def parse_ozone_txt(text):
    """Parse NASA's plain-text data file and return the most recent DU reading."""
    lines = text.strip().split('\n')
    latest_du = None
    latest_date = None

    for line in lines:
        parts = line.split()
        # Each data row starts with a date in YYYY-MM-DD format
        if len(parts) >= 2 and parts[0].count('-') == 2:
            try:
                du = float(parts[1])
                if du != -9999.0:  # -9999 is NASA's missing data marker
                    latest_du = du
                    date = parts[0]
                    latest_date = date
            except ValueError:
                continue

    return latest_du, latest_date

def get_ozone_data():
    # Return cached data if less than 24 hours old
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        cached_time = datetime.fromisoformat(cache['fetched_at'])
        if datetime.now() - cached_time < timedelta(hours=24):
            return cache

    try:
        response = requests.get(OZONE_URL, timeout=10)
        response.raise_for_status()

        current_du, reading_date = parse_ozone_txt(response.text)

        if current_du is None:
            raise ValueError("No valid DU readings found in data file")

        print(f"Fetched ozone data: {current_du} DU on {reading_date}")

    except Exception as e:
        print(f"API fetch failed: {e} — using fallback")
        current_du = 220
        reading_date = 'unavailable'

    result = {
        'current_du': current_du,
        'progress': round((current_du - DEPLETED_FLOOR) / (HEALTHY_TARGET - DEPLETED_FLOOR) * 100, 1),
        'reading_date': reading_date,
        'fetched_at': datetime.now().isoformat(),
        'last_updated': datetime.now().strftime('%B %d, %Y')
    }

    with open(CACHE_FILE, 'w') as f:
        json.dump(result, f)

    return result