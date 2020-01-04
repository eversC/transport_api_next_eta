import requests
import json
from datetime import datetime
import os

mins = "--:--"
live = False

bus_numbers = os.environ["TRANSPORT_BUS_NUMBERS"].split(" ")

response = requests.get(f"https://transportapi.com/v3/uk/"
                        f"bus/stop/{os.environ['TRANSPORT_BUS_STOP_ATCO']}/"
                        f"live.json?"
                        f"app_id={os.environ['TRANSPORT_APP_ID']}&"
                        f"app_key={os.environ['TRANSPORT_APP_KEY']}&"
                        f"group=route&nextbuses=yes")

for bus in bus_numbers:

    departures = json.loads(response.content).get("departures").get(bus)

    if departures:
        first_departure = departures[0]

        aimed = first_departure.get("aimed_departure_time")
        expected = first_departure.get("expected_departure_time")
        best = first_departure.get("best_departure_estimate")

        # if expected != aimed then hoorah we have a live time
        if aimed != expected:
            live = True

        now = datetime.now()
        best_time = datetime.strptime(best, '%H:%M')
        time_diff = best_time - now

        mins = round(time_diff.seconds / 60, 2)

        break

print(mins)
if live:
    print("live time!")
