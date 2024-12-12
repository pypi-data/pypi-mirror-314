# Example dictionary
import re
from coastal_resilience_utilities.utils.dataset import meters_to_degrees

test_config = {
    "id": "caribbean",
    "bounds": (
        -99.90511627,   
        6.42762405, 
        -58.32889149,  
        32.70681188
    ),
    "epsg": "4326",
    "dx": meters_to_degrees(30, 10),
    "chunk_size": 1000,
    "varnames": ["test"],
}