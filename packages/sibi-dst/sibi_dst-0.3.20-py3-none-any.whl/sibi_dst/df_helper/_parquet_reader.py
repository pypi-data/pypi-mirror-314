from typing import Optional

import dask.dataframe as dd
import fsspec

from sibi_dst.df_helper import DfHelper

class ParquetReader(DfHelper):
    DEFAULT_CONFIG = {
        'backend': 'parquet'
    }

    def __init__(self, filesystem_type="file", filesystem_options=None, **kwargs):
        self.config = {
            **self.DEFAULT_CONFIG,
            **kwargs,
        }
        self.df: Optional[dd.DataFrame] = None
        self.parquet_storage_path = self.config.setdefault('parquet_storage_path', None)
        if self.parquet_storage_path is None:
            raise ValueError('parquet_storage_path must be set')
        self.parquet_start_date = self.config.setdefault('parquet_start_date', None)
        if self.parquet_start_date is None:
            raise ValueError('parquet_start_date must be set')

        self.parquet_end_date = self.config.setdefault('parquet_end_date', None)
        if self.parquet_end_date is None:
            raise ValueError('parquet_end_date must be set')

        # Filesystem setup
        self.filesystem_type = filesystem_type
        self.filesystem_options = filesystem_options or {}
        self.fs = fsspec.filesystem(self.filesystem_type, **self.filesystem_options)

        if not self.directory_exists():
            raise ValueError(f"{self.parquet_storage_path} does not exist")

        super().__init__(**self.config)

    def load(self, **kwargs):
        self.df = super().load(**kwargs)
        return self.df

    def directory_exists(self):
        try:
            info = self.fs.info(self.parquet_storage_path)
            return info['type'] == 'directory'
        except FileNotFoundError:
            return False