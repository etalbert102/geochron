'Pydeck helpers'
import h3
from networkx import Graph

def h3edge_to_coordinates(edge:tuple):
    """
    Creates a tuple with coordinate locations from a tuple containing h3
    hexes and weight representing a geographic network edge.

    Args:
        edge: A tuple in the form (h3encoding_origin:str, 
        h3encoding_destination:str, edge_weight:int) 

    Returns:
        A tuple in the form of (coordinate_origin:float, 
        coordinate_destination:float, edge_weight:int)
    """

    edge_coordinate = (h3.h3_to_geo(edge[0]), h3.h3_to_geo(edge[1]), edge[2])

    return edge_coordinate


def convert_to_pydeckdict(edgecoordinates:tuple, origin:str, destination:str):
    """
    Converts a tuple with coordinate locations from a tuple containing h3
    hexes and weight representing a geographic network edge.

    Args:
        edgecoordinates: A tuple in the form of 
        (coordinate_origin:float, coordinate_destination:float, edge_weight:int)
        origin: the origin hex in string format
        destination: the origin hex in string format

    Returns:
        A dictionary for pydeck consumption
    """
    return {
        "start_lat": edgecoordinates[0][0],
        "start_lng": edgecoordinates[0][1],
        "end_lat": edgecoordinates[1][0],
        "end_lng": edgecoordinates[1][1],
        "width": edgecoordinates[2],
        "origin": origin,
        "destination": destination
    }



def network_arc_circle(network:Graph):
    """
    Creates data suitable for pydeck visualization in the Great Circle and Arc layers
    from a chron net or geosyync network that uses h3 hashing.

    Args:
        network: A networkx network

    Returns:
        A list of dictionaries for pydeck consumption
    """
    pydeck_data = []
    edgelist = list(network.edges.data('weight'))
    for edge in edgelist:
        edgecoordinates = h3edge_to_coordinates(edge)
        dict_edge = convert_to_pydeckdict(edgecoordinates, edge[0], edge[1])
        pydeck_data.append(dict_edge)
    return pydeck_data
