from geochron.visualization.pydeck import *
import networkx as nx

def test_h3edge_to_coordinates():
    # Example input edge
    edge = ('8a2a1072b59ffff', '8a2a1072b5bffff', 10)

    # Expected output coordinates
    expected_coordinates = (
        (38.895110, -77.036370),  # Origin coordinates
        (38.895110, -77.036370),  # Destination coordinates
        10  # Edge weight
    )

    # Call the function
    result = h3edge_to_coordinates(edge)

    # Check if the result matches the expected coordinates
    assert result == expected_coordinates


def test_convert_to_pydeckdict():
    edgecoordinates = ((37.7749, -122.4194, 5), (34.0522, -118.2437, 10), 15)
    origin = "8928308280fffff"
    destination = "8928308280fffff"
    
    expected_output = {
        "start_lat": 37.7749,
        "start_lng": -122.4194,
        "end_lat": 34.0522,
        "end_lng": -118.2437,
        "width": 15,
        "origin": "8928308280fffff",
        "destination": "8928308280fffff"
    }
    
    assert convert_to_pydeckdict(edgecoordinates, origin, destination) == expected_output

def test_network_arc_circle():
    # Create a simple graph for testing
    G = nx.Graph()
    G.add_edge('A', 'B', weight=1.0)
    G.add_edge('B', 'C', weight=2.0)

    # Call the function with the test graph
    result = network_arc_circle(G)

    # Check the type of the result
    assert isinstance(result, list), "Result should be a list"

    # Check the length of the result
    assert len(result) == 2, "Result length should match the number of edges"

    # Check the type of the elements in the result
    for item in result:
        assert isinstance(item, dict), "Each item in the result should be a dictionary"
