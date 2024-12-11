import polars as pl


def create_session(
    df: pl.DataFrame,
    session_name: str,
    session_hour_start,
    session_hour_end,
    time_col_name="time",
) -> pl.DataFrame:
    df = df.with_columns(
        (
            (
                pl.col(time_col_name).cast(pl.Datetime("ms")).dt.hour()
                >= session_hour_start
            )
            & (
                pl.col(time_col_name).cast(pl.Datetime("ms")).dt.hour()
                < session_hour_end
            )
        ).alias(session_name)
    )
    return df
