import datetime
import numpy as np
import requests

from scipy.interpolate import interp1d
from geopy.distance import geodesic 
from rdflib import Graph, Namespace, Literal, RDF, Literal, XSD
from helper import assert_response_ok, create_unique_coodinates_instance


def calculate_distances_between_points(path):
    distances = []
    total_distance = 0
    for i in range(len(path) - 1):
        dist = geodesic(path[i][1:3], path[i+1][1:3]).kilometers
        distances.append(dist)
        total_distance += dist
    return total_distance, distances


def calculate_total_travel_time(distances, speed):
    time_section1 = (distances[0]/speed[0]) * 3600
    time_section2 = (distances[1]/speed[1]) * 3600
    time_section3 = (distances[2]/speed[2]) * 3600
    total_time = (time_section1 + time_section2 + time_section3)
    return total_time


def calculate_time_ratio_per_section(total_distance, distances):
    time_ratios = [d / total_distance for d in distances]
    return time_ratios


def interpolate_position_over_time(time_ratios, path):
    cumulative_ratios = [0] + list(np.cumsum(time_ratios))
    lat_interp = interp1d(cumulative_ratios, [c[1] for c in path])
    lon_interp = interp1d(cumulative_ratios, [c[2] for c in path])
    alt_interp = interp1d(cumulative_ratios, [c[3] for c in path])
    return lat_interp, lon_interp, alt_interp


def send_request_to_rdfox(endpoint, payload, data):    
    response = requests.patch(endpoint, params=payload, data=data)
    assert_response_ok(response, "Failed to run select query.")
    return response


def create_trajectory_graph(path, speed, payload, endpoint):
    total_distance, distances = calculate_distances_between_points(path)
    total_time = calculate_total_travel_time(distances, speed)
    time_ratios = calculate_time_ratio_per_section(total_distance, distances)
    lat_interp, lon_interp, alt_interp = interpolate_position_over_time(time_ratios, path)
    departure_time_str = path[0][4]
    timestamp_str = departure_time_str

    i = 0
    for t in range(int(total_time) + 1):

        g = Graph()
        ns = Namespace("http://www.rdfox.com#")
        g.bind("", ns)
        data = ""

        # if i == 4:
        #     break
        
        dp_label = "dataPoint" + str(i)
        ratio = t / total_time
        lat = lat_interp(ratio)
        lon = lon_interp(ratio)
        alt = alt_interp(ratio)
        
        dp_coordinates = create_unique_coodinates_instance(dp_label)
        timestamp_rdf = timestamp_str.replace(" ","T")
        g.add((ns[dp_label], RDF.type, ns.DataPoint))
        g.add((ns[dp_label], ns.hasTimestamp, Literal(timestamp_rdf, datatype=XSD.dateTime)))
        g.add((ns[dp_label], ns.hasDataPointCoordinates, ns[dp_coordinates]))
        g.add((ns[dp_coordinates], RDF.type, ns.Coordinates))
        g.add((ns[dp_coordinates], ns.hasLatitude, Literal(lat, datatype=XSD.decimal)))
        g.add((ns[dp_coordinates], ns.hasLongitude, Literal(lon, datatype=XSD.decimal)))
        g.add((ns[dp_coordinates], ns.hasAltitude, Literal(alt, datatype=XSD.decimal)))

        data = g.serialize(format='turtle')

        send_request_to_rdfox(endpoint, payload, data)

        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        timestamp += datetime.timedelta(seconds=1)
        timestamp_str = str(timestamp)

        i += 1
