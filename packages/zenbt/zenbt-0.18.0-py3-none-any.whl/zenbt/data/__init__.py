from .data import download_okx_data, read_data, read_data_pl


def get_sample_btc_data():
    from pathlib import Path
    import polars as pl

    # Resolve the file path relative to the current script
    current_file = Path(__file__).resolve()
    file_directory = current_file.parent
    parquet_file = file_directory / "btc_small.parquet"

    df = pl.read_parquet(parquet_file)
    return df
