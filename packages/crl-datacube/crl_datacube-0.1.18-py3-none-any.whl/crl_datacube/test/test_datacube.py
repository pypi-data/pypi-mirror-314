from crl_datacube.datacube2 import DataCube
from crl_datacube.storage import PlainOlZarrStore
from crl_datacube.test.test_config import test_config
import logging

def test_datacube_local():
    dc = DataCube(**{
        **test_config,
        "storage": PlainOlZarrStore(
            path="/tmp/test.zarr"
        )
    })
    logging.info(dc)
