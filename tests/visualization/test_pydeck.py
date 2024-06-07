from geochron.visualization.pydeck import *

def test_h3edge_to_coordinates():
    # Example input edge
    edge = ('89283082837ffff', '89283082833ffff', 10)

    # Expected output coordinates
    expected_coordinates = ((37.777493908651344, -122.42904243437428),
                            (37.776167791691506, -122.42545196039973), 10)

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
    G = Graph()
    G.add_edge('8928308280fffff', '8928308280fffff', weight=1)
    result = network_arc_circle(G)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert set(result[0].keys()) == {"start_lat", "start_lng", "end_lat", "end_lng", "width", "origin", "destination"}