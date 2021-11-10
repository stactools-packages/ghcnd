import gzip
import os
import shutil

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from shapely.geometry import Point
from tqdm import tqdm

from stactools.ghcnd.constants import (
    DATA_TABLE_COLUMNS,
    STATION_TABLE_COLUMNS,
    STATIONS_URL,
    YEARS_URL,
)


class CreateDataAsset:
    def __init__(self, download_folder: str, unzip_folder: str,
                 output_path: str):
        self.download_folder = download_folder
        self.unzip_folder = unzip_folder
        self.output_path = output_path

        for folder in [download_folder, unzip_folder]:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def download(self, source: str) -> str:
        """Download source file"""
        response = requests.get(source, stream=True)
        download_path = os.path.join(self.download_folder,
                                     os.path.basename(source))

        with open(download_path, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

        return download_path

    def unzip(self, source: str) -> str:
        """Unzip a source file"""
        unzip_fname = os.path.basename(source).replace(".gz", "")
        unzip_path = os.path.join(self.unzip_folder, unzip_fname)
        with gzip.open(source, 'rb') as f_in:
            with open(unzip_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        return unzip_path.replace(".gz", "")

    def get_stations(self) -> pd.DataFrame:
        """Get stations data"""
        stations_fname = os.path.basename(STATIONS_URL)
        stations_fwf = os.path.join(self.download_folder, stations_fname)
        if not os.path.exists(stations_fwf):
            self.download(STATIONS_URL)
        stations_df = pd.read_fwf(
            stations_fwf,
            header=None,
            names=[d["name"] for d in STATION_TABLE_COLUMNS])
        stations_df["ID"] = stations_df.ID.astype(str)
        return stations_df

    def merge_stations(self, year_csv: str,
                       stations_df: pd.DataFrame) -> pd.DataFrame:
        """Merge yearly weather data from a csv file with a stations dataframe"""
        year_df = pd.read_csv(year_csv,
                              header=None,
                              names=[d["name"] for d in DATA_TABLE_COLUMNS])
        year_df["ID"] = year_df.ID.astype(str)
        year_df = year_df.merge(stations_df, how="left")
        year_df["geometry"] = year_df.apply(
            lambda r: Point(r.LONGITUDE, r.LATITUDE), axis=1).astype(str)
        return year_df

    def create_data_asset(self, start_year: int, end_year: int) -> None:
        stations_df = self.get_stations()
        years = range(start_year, end_year + 1)

        # Retrieve and append weather data for dates after last_date
        for i, year in enumerate(years):
            print(f"Processing {year}")
            year_url = f"{YEARS_URL}{year}.csv.gz"
            year_zip = self.download(year_url)
            year_csv = self.unzip(year_zip)
            year_df = self.merge_stations(year_csv, stations_df)
            table = pa.Table.from_pandas(year_df)

            if i == 0:
                pqwriter = pq.ParquetWriter(self.output_path, table.schema)

            pqwriter.write_table(table)

        pqwriter.close()
