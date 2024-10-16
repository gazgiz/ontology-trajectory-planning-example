from helper import create_unique_coodinates_instance
from rdflib import Graph, Namespace, Literal, RDF, Literal, XSD

def create_flight_plan_graph(flight_plan, path):
    g = Graph()
    ns = Namespace("http://www.rdfox.com#")
    g.bind("", ns)

    departure_airport = path[0][0].replace(" ", "_").lower()
    waypoint1 = path[1][0].replace(" ", "_").lower()
    waypoint2 = path[2][0].replace(" ", "_").lower()
    arrival_airport = path[3][0].replace(" ", "_").lower()

    departure_time_str = path[0][4]
    waypoint1_estimated_time_str = path[1][4]
    waypoint2_estimated_time_str = path[2][4]
    # arrival_estimated_time_str = path[3][4]

    departure_time_rdf = departure_time_str.replace(" ","T")
    waypoint1_estimated_time_rdf = waypoint1_estimated_time_str.replace(" ","T")
    waypoint2_estimated_time_rdf = waypoint2_estimated_time_str.replace(" ","T")

    g.add((ns[flight_plan], RDF.type, ns.FlightPlan))
    g.add((ns[flight_plan], ns.hasDepartureAirport, ns[departure_airport]))
    g.add((ns[flight_plan], ns.hasArrivalAirport, ns[arrival_airport]))
    g.add((ns[flight_plan], ns.hasDepartureTime, Literal(departure_time_rdf, datatype=XSD.dateTime)))
    g.add((ns[flight_plan], ns.hasWaypoint, ns[waypoint1]))
    g.add((ns[flight_plan], ns.hasWaypoint, ns[waypoint2]))

    departure_coordinates = create_unique_coodinates_instance(departure_airport)
    g.add((ns[departure_airport], RDF.type, ns.Airport))
    g.add((ns[departure_airport], ns.hasAirportCoordinates, ns[departure_coordinates]))
    g.add((ns[departure_coordinates], RDF.type, ns.Coordinates))
    g.add((ns[departure_coordinates], ns.hasLatitude, Literal(path[0][1], datatype=XSD.decimal)))
    g.add((ns[departure_coordinates], ns.hasLongitude, Literal(path[0][2], datatype=XSD.decimal)))
    g.add((ns[departure_coordinates], ns.hasAltitude, Literal(path[0][3], datatype=XSD.decimal)))

    waypoint1_coordinates = create_unique_coodinates_instance(waypoint1)
    g.add((ns[waypoint1], RDF.type, ns.Waypoint))
    g.add((ns[waypoint1], ns.hasWaypointIndex, Literal("1", datatype=XSD.integer)))
    g.add((ns[waypoint1], ns.hasWaypointTimestamp, Literal(waypoint1_estimated_time_rdf, datatype=XSD.dateTime)))
    g.add((ns[waypoint1], ns.hasWaypointCoordinates, ns[waypoint1_coordinates]))
    g.add((ns[waypoint1_coordinates], RDF.type, ns.Coordinates))
    g.add((ns[waypoint1_coordinates], ns.hasLatitude, Literal(path[1][1], datatype=XSD.decimal)))
    g.add((ns[waypoint1_coordinates], ns.hasLongitude, Literal(path[1][2], datatype=XSD.decimal)))
    g.add((ns[waypoint1_coordinates], ns.hasAltitude, Literal(path[1][3], datatype=XSD.decimal)))
    
    waypoint2_coordinates = create_unique_coodinates_instance(waypoint2)
    g.add((ns[waypoint2], RDF.type, ns.Waypoint))
    g.add((ns[waypoint2], ns.hasWaypointIndex, Literal("2", datatype=XSD.integer)))
    g.add((ns[waypoint2], ns.hasWaypointTimestamp, Literal(waypoint2_estimated_time_rdf, datatype=XSD.dateTime)))
    g.add((ns[waypoint2], ns.hasWaypointCoordinates, ns[waypoint2_coordinates]))
    g.add((ns[waypoint2_coordinates], RDF.type, ns.Coordinates))
    g.add((ns[waypoint2_coordinates], ns.hasLatitude, Literal(path[2][1], datatype=XSD.decimal)))
    g.add((ns[waypoint2_coordinates], ns.hasLongitude, Literal(path[2][2], datatype=XSD.decimal)))
    g.add((ns[waypoint2_coordinates], ns.hasAltitude, Literal(path[2][3], datatype=XSD.decimal)))

    arrival_coordinates = create_unique_coodinates_instance(arrival_airport)
    g.add((ns[arrival_airport], RDF.type, ns.Airport))
    g.add((ns[arrival_airport], ns.hasAirportCoordinates, ns[arrival_coordinates]))
    g.add((ns[arrival_coordinates], RDF.type, ns.Coordinates))
    g.add((ns[arrival_coordinates], ns.hasLatitude, Literal(path[3][1], datatype=XSD.decimal)))
    g.add((ns[arrival_coordinates], ns.hasLongitude, Literal(path[3][2], datatype=XSD.decimal)))
    g.add((ns[arrival_coordinates], ns.hasAltitude, Literal(path[3][3], datatype=XSD.decimal)))

    print("== Serializing the graph ==")

    g.serialize(destination='flight_plan_test.ttl', format='turtle')