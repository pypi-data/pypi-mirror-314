from odc.geo.geobox import GeoBox, GeoboxTiles
from odc.geo.xr import xr_zeros
from typing import Callable

import geopandas as gpd
import pandas as pd
import numcodecs

import numpy as np
import xarray as xr
import rioxarray as rxr
from osgeo import gdal
from shapely.geometry import Polygon

from joblib import Parallel, delayed
from tqdm import tqdm
from dataclasses import dataclass
import logging
import os, shutil, sys
from glob import glob
import uuid
from enum import Enum
import warnings

from coastal_resilience_utilities.utils.geo import transform_point
from coastal_resilience_utilities.summary_stats.summary_stats import summary_stats2

from crl_datacube.storage import BaseStorage


logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger("My Personal")
logger.propagate = True
logger.setLevel(logging.DEBUG)


class IntakeMode(Enum):
    READ = "read"
    CREATE = "create"
    WRITE = "write"
    APPEND = "append"


@dataclass(frozen=True)
class DataCube:
    id: str
    dx: float
    epsg: int
    bounds: tuple[float, float, float, float]
    chunk_size: int
    storage: BaseStorage
    varnames: list[str]
    nodata: float = 0.0
    dtype: str = "<f8"

    @property
    def crs(self) -> str:
        return f"epsg:{self.epsg}"

    @property
    def geobox(self) -> GeoBox:
        return GeoBox.from_bbox(self.bounds, crs=self.crs, resolution=self.dx)

    @property
    def chunk_shape(self) -> tuple[int, int]:
        return (self.chunk_size, self.chunk_size)

    @property
    def tiles(self) -> GeoboxTiles:
        return GeoboxTiles(self.geobox, self.chunk_shape)

    def tiles_by_bounds(
        self, left: float, bottom: float, right: float, top: float
    ) -> GeoboxTiles:
        """
        Filter tiles to given bounds, and return the tile indexes
        """
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            if not (
                bbox.left < right
                and bbox.right > left
                and bbox.bottom < top
                and bbox.top > bottom
            ):
                continue
            yield idx

    def tiles_for_da(self, da: xr.DataArray):
        """
        Convenience function to reproject a DataArray
        and get the tiles associated with the bounds
        """

        # Get the bounds in the native CRS
        da_bounds = da.rio.bounds()
        da_bl = transform_point(da_bounds[0], da_bounds[1], da.rio.crs, self.crs)
        da_tr = transform_point(da_bounds[2], da_bounds[3], da.rio.crs, self.crs)

        # Get the tiles that intersect with the data array
        return self.tiles_by_bounds(da_bl.x, da_bl.y, da_tr.x, da_tr.y)

    def get_data_layout(self, varnames: list[str] = []):
        if len(varnames) > 0:
            return (
                (
                    xr_zeros(
                        self.geobox, chunks=self.chunk_shape, dtype="float32"
                    ).expand_dims(
                        {
                            "var": varnames,
                        }
                    )
                )
                .rename({"longitude": "x", "latitude": "y"})
                .to_dataset("var")
            )

        else:
            return xr_zeros(
                self.geobox, chunks=self.chunk_shape, dtype="float32"
            ).rename({"longitude": "x", "latitude": "y"})

    def create_dataset_schema(
        self, group=None, varnames=None, mode: IntakeMode = IntakeMode.CREATE
    ) -> None:
        """
        Initialize a datacube, that has a very simple schema;
        Each array is 2D, and dataarrays within the cube are created for each layer
        """
        varnames_to_create = varnames if varnames else self.varnames

        # Standard 2D schema, could be made more flexible
        big_ds = self.get_data_layout(varnames_to_create)

        lon_encoding = optimize_coord_encoding(big_ds.x.values, self.dx)
        lat_encoding = optimize_coord_encoding(big_ds.y.values, -self.dx)
        encoding = {
            "x": {**lon_encoding},
            "y": {**lat_encoding},
        }

        group_to_modify = self.storage.get_group(group)
        if mode == IntakeMode.CREATE:
            big_ds.to_zarr(
                self.storage.get_storage(),
                group=group,
                mode="w",
                # encoding=encoding,
                compute=False,
            )

        elif mode == IntakeMode.APPEND:
            big_ds.to_zarr(
                self.storage.get_storage(),
                group=group,
                mode="a",
                # encoding=encoding,
                compute=False,
            )

    def get_extents(self) -> None:
        """ """
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            extent = bbox.left, bbox.right, bbox.bottom, bbox.top
            yield idx, extent

    def get_covering_polygons(
        self, idxs: list[tuple[int, int]] = []
    ) -> gpd.GeoDataFrame:
        idxs = [tuple(i) for i in idxs]
        buff = []
        x = []
        y = []
        for idx, extent in self.get_extents():
            if len(idxs) > 0 and idx not in idxs:
                continue

            buff.append(
                Polygon(
                    [
                        (extent[0], extent[2]),
                        (extent[1], extent[2]),
                        (extent[1], extent[3]),
                        (extent[0], extent[3]),
                    ]
                )
            )
            x.append(idx[0])
            y.append(idx[1])

        return gpd.GeoDataFrame(
            pd.DataFrame({"x": x, "y": y}), geometry=buff, crs="EPSG:4326"
        )

    def geobox_to_rxr(self, geobox: GeoBox) -> xr.DataArray:
        # Create a dummy data array with the same shape as the Geobox
        data = np.zeros((geobox.height, geobox.width))
        data_array = xr.DataArray(data, dims=("y", "x"))
        data_array.rio.write_crs(self.crs, inplace=True)
        data_array.rio.write_transform(geobox.transform, inplace=True)

        # Set the x and y coordinates based on the Geobox
        x_coords = (
            np.arange(geobox.width) * geobox.resolution.x
            + geobox.transform.c
            + self.dx / 2.0
        )
        y_coords = (
            np.arange(geobox.height) * geobox.resolution.y
            + geobox.transform.f
            - self.dx / 2.0
        )
        data_array = data_array.assign_coords({"x": x_coords, "y": y_coords})
        data_array = data_array.rio.set_spatial_dims(x_dim="x", y_dim="y")
        data_array.rio.write_nodata(self.nodata, inplace=True)
        # Create a dataset from the data array
        return data_array

    def set_data(
        self,
        var: str,
        idx: tuple[int, int],
        ds: xr.DataArray,
        group: str = None,
        store_idxs: bool = False,
    ):

        src = self.storage.get_group(group)[var]

        if ds.y[0] < ds.y[-1]:
            ds = ds.reindex(y=ds.y[::-1])

        xy_slice = self.get_xy_slice(ds.shape, idx)
        src[xy_slice] = ds.data.astype("float32")

        if store_idxs:
            if "stored_idxs" in self.storage.get_group(group)[var].attrs:
                stored_idxs = self.storage.get_group(group)[var].attrs["stored_idxs"]
            else:
                stored_idxs = []

            stored_idxs.append(idx)
            stored_idxs = list(set([tuple(i) for i in stored_idxs]))
            self.storage.get_group(group)[var].attrs["stored_idxs"] = stored_idxs

    def get_xy_slice(
        self, shape: tuple[int, int], idx: tuple[int, int]
    ) -> tuple[slice, slice]:
        to_return = (
            slice(idx[0] * self.chunk_size, idx[0] * self.chunk_size + shape[0]),
            slice(idx[1] * self.chunk_size, idx[1] * self.chunk_size + shape[1]),
        )
        return to_return

    def intake_data(
        self,
        da: xr.DataArray | xr.Dataset,
        var: str,
        group: str = None,
        only_idxs: list[tuple[int, int]] = [],
        boxbuff: int = 0.1,
        intake_mode: IntakeMode = IntakeMode.APPEND,
        parallelism: int = 1,
        handle_nodata: bool = True,
    ) -> None:
        # Record initial CRS
        init_crs = da.rio.crs
        logging.info(f"Initial CRS: {init_crs}")

        # Handle NoData values
        if handle_nodata:
            try:
                da = da.where(da != da.rio.nodata, self.nodata)
            except:
                da = da.where(da != da.attrs["_FillValue"], self.nodata)
        logging.info(f"Setting nodata to {self.nodata}")
        da.rio.write_nodata(self.nodata, inplace=True)
        da.rio.write_crs(init_crs, inplace=True)

        if intake_mode == IntakeMode.CREATE:
            self.create_dataset_schema(group=group)

        elif intake_mode == IntakeMode.APPEND:
            try:
                self.storage.get_group(group)
            except KeyError:
                self.create_dataset_schema(group=group)

        def prep_single_tile(idx: tuple[int, int], da: xr.DataArray):
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            bl = transform_point(bbox.left, bbox.bottom, self.crs, da.rio.crs)
            tr = transform_point(bbox.right, bbox.top, self.crs, da.rio.crs)

            # Get a dummy data array with the same shape as the tile
            empty_tile_as_da = self.geobox_to_rxr(tile)

            # Clip the data array to the tile in the native CRS of the data array
            # Need to buffer a little bit to avoid edge effects after reprojecting
            # boxbuff = 10000
            try:
                da_clipped = da.rio.clip_box(
                    minx=bl.x - boxbuff,
                    miny=bl.y - boxbuff,
                    maxx=tr.x + boxbuff,
                    maxy=tr.y + boxbuff,
                )
                # Now that data is smaller, reproject it to the tile
                da_tiled = da_clipped.rio.reproject_match(empty_tile_as_da)
                return (idx, da_tiled)
            except (rxr.exceptions.NoDataInBounds, rxr.exceptions.OneDimensionalRaster):
                return None

        # Get the tiles that intersect with the data array
        idxs = self.tiles_for_da(da)

        def f(idx):
            logger = logging.getLogger("botocore")
            logger.setLevel(logging.WARNING)
            logger.propagate = False
            i = prep_single_tile(idx, da)
            if i:
                idx, da_clipped = i
                if np.isnan(da_clipped).all():
                    return

                self.set_data(var, idx, da_clipped, group=group)

        if len(only_idxs) > 0:
            idxs = only_idxs
        else:
            idxs = [i for i in idxs]

        if parallelism > 1:
            Parallel(n_jobs=parallelism)(
                delayed(f)(idx) for idx in tqdm(idxs, total=len(idxs))
            )
        else:
            for idx in tqdm(idxs, total=len(idxs)):
                f(idx)

    def get_single_xarray_tile(
        self, var: str, idx: tuple[int, int], group: str = None
    ) -> xr.DataArray:
        src = self.storage.get_group(group)[var]
        tile = self.tiles[tuple(idx)]
        da = self.geobox_to_rxr(tile)
        xy_slice = self.get_xy_slice(da.shape, idx)
        data = src[xy_slice]
        da.data = data
        da.rio.write_nodata(self.nodata, inplace=True)
        da.rio.write_crs(self.epsg, inplace=True)
        return da

    def get_xarray_tiles(
        self,
        var: str,
        filter_nan: bool = True,
        get_idxs: list[tuple[int, int]] = [],
        group: str = None,
        parallelism: int = 1,
    ) -> list[xr.DataArray]:
        if group:
            src = self.storage.get_group(group)[var]
        else:
            src = self.storage.root_group[var]

        if len(get_idxs) > 0:
            print("filtering idxs")
            all_tiles = get_idxs
        else:
            all_tiles = [i for i in self.tiles._all_tiles()]

        def process(idx):
            # for idx in tqdm(all_tiles, total=len(all_tiles)):
            da = self.get_single_xarray_tile(var, idx, group)
            tile = self.tiles[tuple(idx)]

            if filter_nan:
                if np.isnan(da).all():
                    return
                if np.nanmin(da) == self.nodata and np.nanmax(da) == self.nodata:
                    return
                if np.all(da == np.nan):
                    return

            return da, idx, tile

        to_return = Parallel(n_jobs=parallelism)(
            delayed(process)(idx) for idx in tqdm(all_tiles, total=len(all_tiles))
        )
        return [i for i in to_return if i is not None]

    def apply_function(
        self,
        f: Callable,
        output: str,
        idxs: list[tuple[int, int]],
        args: list = [],
        kwargs: dict() = dict(),
        tile_kwargs: dict = dict(),
        group: str = None,
        parallelism: int = 1,
    ):
        def process(idx):
            _args = []
            for arg in args:
                if isinstance(arg, XArrayAccessor):
                    try:
                        _args.append(arg.get_xarray_tiles(**tile_kwargs)(idx))
                    except IndexError:
                        return

            _kwargs = kwargs.copy()
            for key, value in _kwargs.items():
                if isinstance(value, XArrayAccessor):
                    try:
                        _kwargs[key] = value.get_xarray_tiles(**tile_kwargs)(idx)
                    except IndexError:
                        return

            result = f(*_args, **_kwargs)
            if output is not None:
                self.set_data(output, idx, result, group)
            else:
                return result
            
        if parallelism > 1:
            results = Parallel(n_jobs=parallelism)(delayed(process)(idx) for idx in tqdm(idxs))
        else:
            results = []
            for idx in tqdm(idxs):
                results.append(process(idx))
        
        if not output:
            return results
            
                
    def export_as_tif(self, var: str, output: str, group: str = None, idxs: list[tuple[int, int]] = [], COG=False) -> None:
        id = str(uuid.uuid4())
        tmp_dir = f"/tmp/{id}"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        self.export_as_tif_tiles(var, tmp_dir, group=group, idxs=idxs)
        data = glob(os.path.join(tmp_dir, "*.tif"))
        tmp_vrt = f"{tmp_dir}/vrt.vrt"
        vrt = gdal.BuildVRT(tmp_vrt, data)
        vrt = None
        if COG:
            gdal.Translate(
                output,
                tmp_vrt,
                format="COG",
                creationOptions=["COMPRESS=DEFLATE", "BIGTIFF=YES"],
            )
        else:
            gdal.Translate(
                output,
                tmp_vrt,
                format="GTiff",
                creationOptions=["COMPRESS=LZW", "BIGTIFF=YES"],
            )
        return output

    def export_as_tif_tiles(
        self, var: str, output: str, group: str = None, idxs: list[tuple[int, int]] = []
    ) -> None:
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)

        for da, idx, tile in self.get_xarray_tiles(var, group=group, get_idxs=idxs):
            da.rio.write_crs(self.epsg, inplace=True)
            da.rio.write_nodata(self.nodata, inplace=True)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                da.rio.to_raster(
                    f"{output}/{var}_{idx[0]}_{idx[1]}.tif", compress="LZW"
                )

    def as_da(self, var: str, group=None, idxs: list[tuple[int, int]] = []) -> None:
        id = str(uuid.uuid4())
        tmp_file = f"/tmp/{id}.tif"
        self.export_as_tif(var, tmp_file, group=group, idxs=idxs)
        return rxr.open_rasterio(tmp_file)


@dataclass(frozen=True)
class XArrayAccessor:
    dc: DataCube
    var: str
    group: str = None

    def get_xarray_tiles(self, **kwargs):

        def f(idx):
            return self.dc.get_single_xarray_tile(self.var, idx, group=self.group)

        return f


def optimize_coord_encoding(values, dx):
    dx_all = np.diff(values)
    # dx = dx_all[0]
    np.testing.assert_allclose(dx_all, dx), "must be regularly spaced"

    offset_codec = numcodecs.FixedScaleOffset(
        offset=values[0], scale=1 / dx, dtype=values.dtype, astype="i8"
    )
    delta_codec = numcodecs.Delta("i8", "i2")
    compressor = numcodecs.Blosc(cname="zstd")

    enc0 = offset_codec.encode(values)
    # everything should be offset by 1 at this point
    np.testing.assert_equal(np.unique(np.diff(enc0)), [1])
    enc1 = delta_codec.encode(enc0)
    # now we should be able to compress the shit out of this
    enc2 = compressor.encode(enc1)
    decoded = offset_codec.decode(delta_codec.decode(compressor.decode(enc2)))

    # will produce numerical precision differences
    # np.testing.assert_equal(values, decoded)
    np.testing.assert_allclose(values, decoded)

    return {"compressor": compressor, "filters": (offset_codec, delta_codec)}


def summary_stats(
    dc: DataCube,
    var: str,
    gdf: gpd.GeoDataFrame,
    group: str = None,
    stats=["sum", "count"],
    return_with_fields: bool = False,
):
    logging.info(var)
    tiles = dc.get_xarray_tiles(var, group=group)
    gdf = gdf.reset_index()

    buff = []
    for da, idx, tile in tiles:
        bbox = tile.boundingbox
        extent = bbox.left, bbox.right, bbox.bottom, bbox.top
        _gdf = gdf.cx[extent[0] : extent[1], extent[2] : extent[3]]
        if _gdf.shape[0] == 0:
            continue

        output = summary_stats2(_gdf, da, stats)
        buff.append(output)

    output = (
        pd.concat(buff)
        .groupby(["index", "geometry"])
        .apply(lambda x: x.apply(np.nansum))
        .reset_index()
        .set_index("index")
    )
    # output = pd.concat(buff).groupby(["index", "geometry"]).sum().reset_index().set_index("index")
    if return_with_fields:
        return pd.merge(
            gdf,
            output[[c for c in output.columns if c != "geometry"]],
            left_index=True,
            right_index=True,
            how="left",
        )

    else:
        gdf["dummycolumn"] = 0
        return pd.merge(
            gdf[["dummycolumn"]],
            output[[c for c in output.columns if c != "geometry"]],
            left_index=True,
            right_index=True,
            how="left",
        ).drop(columns=["dummycolumn"])
        # return output
