from create_flight_plan_graph import create_flight_plan_graph
from create_trajectory_graph import create_trajectory_graph

import os

flight_plan = "flightplan001"
speed = [250, 250, 250]  # km/h
path = [
    ("Yeui-do airport", 37.527426, 126.931572, 0, "2024-09-06 14:00:00"),     # Departure
    ("Waypoint1", 37.552743, 126.897240, 300, "2024-09-06 14:01:00"),   # Waypoint1 (estimated timestamp)
    ("Waypoint2", 37.579413, 126.842308, 300, "2024-09-06 14:02:21"),   # Waypoint2 (estimated timestamp)
    ("Gimpo airport", 37.561725, 126.801109, 0, "2024-09-06 14:03:21")      # Arrival (estimated timestamp)
]

payload = {'operation': 'add-content-update-prefixes'}
endpoint= "http://localhost:12110/datastores/default/content"


def main():

    # if os.path.exists("flight_plan.ttl"):
    #     print("The flight plan in Turtle format has been created. Skipping creation.")
    # else:
    #     create_flight_plan_graph(flight_plan, path)

    create_trajectory_graph(path, speed, payload, endpoint)


if __name__ == "__main__":
    main()
