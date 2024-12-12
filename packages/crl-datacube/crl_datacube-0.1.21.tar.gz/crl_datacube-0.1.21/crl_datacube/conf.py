import re
from coastal_resilience_utilities.utils.dataset import meters_to_degrees

VARS = [
    "WaterDepthMax",
    "Exposure", 
    "PercentDamage",
    "DDE", 
    "Damages", 
    "Population"
]
CLIMATES = ["Historic", "Future2050"]
SCENARIOS = ["S1", "S2", "S3", "S4"]
RPS = ["Tr10", "Tr25", "Tr50", "Tr100"]

FORMATTER = lambda v, c, s, r : f"{v}_{c}_{s}_{r}"

def get_all(regex=r'.*'):
    from itertools import product
    return [
        i for i in [FORMATTER(v, c, s, r) for v, c, s, r in product(VARS, CLIMATES, SCENARIOS, RPS)]
        if re.match(regex, i)
    ]
    
# Example dictionary
caribbean_config = {
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
    "varnames": get_all(),
    "storage": '/app/data/caribbean-test.zarr'
}

dr_config = dict(   
    id = "hispaniola",
    bounds = (
        -74.8310,
        16.5424,
        -68.0246,
        20.3981,
    ),
    epsg = "4326",
    dx = meters_to_degrees(30, 10),
    chunk_size = 1000,
    varnames = get_all(),
    storage = '/app/data/hispaniola-test.zarr',
)

