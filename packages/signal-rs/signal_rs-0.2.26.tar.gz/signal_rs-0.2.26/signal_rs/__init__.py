# import the contents of the Rust library into the Python extension

#from .signal_rs.signal_rs import integral_calculation_rust
from .signal_rs import integral_calculation_rust

__all__ = [
    'amvParameters',
    'amvSignalAnalysis',
    'integral_calculation_rust'
]

import polars as pl
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import plotly.io as pio

#from scipy import integrate
from typing import Optional, Union, List, Tuple

class amvParameters:
    def __init__(self, **kwargs: dict):
        # Set default parameters
        self.P0000: int = kwargs.get('P0000', 4095)
        self.P0001: int = kwargs.get('P0001', 5)
        self.P0002: int = kwargs.get('P0002', 40)
        self.P0003: int = kwargs.get('P0003', 40)
        self.P0004: int = kwargs.get('P0004', 1)
        self.P0005: int = kwargs.get('P0005', 50)
        self.P0006: int = kwargs.get('P0006', 30)
        self.P0007: int = kwargs.get('P0007', 1800)
        self.P0008: int = kwargs.get('P0008', 100)
        self.P0009: int = kwargs.get('P0009', 1)
        self.P000A: int = kwargs.get('P000A', 0)
        self.P000B: int = kwargs.get('P000B', 50)
        self.P000C: int = kwargs.get('P000C', 50)
        self.P000D: int = kwargs.get('P000D', 50)
        self.P000E: int = kwargs.get('P000E', 50)
        self.P000F: int = kwargs.get('P000F', 75)
        self.P0010: int = kwargs.get('P0010', 55)
        self.P0011: int = kwargs.get('P0011', 1)
        self.P0012: int = kwargs.get('P0012', 50)
        self.P0013: int = kwargs.get('P0013', 2)
        self.P0014: int = kwargs.get('P0014', 0)
        self.P0015: int = kwargs.get('P0015', 40)

class amvSignalAnalysis:
    '''Class for AMV Signal analysis.'''
    def __init__(self, df: Union[pd.DataFrame, pl.DataFrame], **kwargs: dict):
        """Initializes the analysis class and converts DataFrame to Polars if necessary."""
        if isinstance(df, pd.DataFrame):
            self.df: pl.DataFrame = pl.from_pandas(df)
            self.backend: str = "pandas"
        elif isinstance(df, pl.DataFrame):
            self.df: pl.DataFrame = df
            self.backend: str = "polars"
        else:
            raise TypeError("Unsupported dataframe type. Must be pandas.DataFrame or polars.DataFrame.")

        self.parameters: amvParameters = amvParameters(**kwargs)

    def __str__(self) -> str:
        """String representation of the dataframe and parameters."""
        return f"Converted to Polars DataFrame, Parameters: {self.parameters}"

    def get_column_names(self) -> List[str]:
        """Retrieve column names."""
        return self.df.columns

    def filter_rows(self, column_name: str, value: Union[int, float], df: Optional[pl.DataFrame] = None) -> pl.DataFrame:
        """Filter rows where the column equals a specific value."""
        if column_name not in self.df.columns:
            raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")
        if df is None:
            return self.df.filter(pl.col(column_name) == value)
        else:  # Filter the passed DataFrame
            return df.filter(pl.col(column_name) == value)

    def add_column(self, column_name: str, values: List[Union[int, float]]) -> pl.DataFrame:
        """Add a new column to the Polars DataFrame."""
        self.df = self.df.with_columns(pl.Series(column_name, values))
        return self.df

    def to_pandas(self) -> pd.DataFrame:
        """Convert the Polars DataFrame back to Pandas DataFrame."""
        return self.df.to_pandas()

    def get_baseline(self, column_name: str = "data") -> pl.DataFrame:
        """Get baseline by calculating medians of start and end segments and interpolating."""
        start_median = self.df[:20].select(pl.col(column_name).median()).item()
        end_median = self.df[-20:].select(pl.col(column_name).median()).item()

        baseline = [None] * len(self.df)
        baseline[0] = start_median
        baseline[-1] = end_median

        self.df = self.df.with_columns(pl.Series("baseline", baseline))

        # Interpolate baseline
        self.df = self.df.select(
            pl.col("*"),
            pl.col("baseline").interpolate().alias("baseline_interpolated")
        )
        return self.df

    def smooth(self, column_name: str = "data", span: int = 25, method: str = "both") -> pl.DataFrame:
        """Apply smoothing methods (EWMA, SMA, or both)."""
        alpha = 2 / (span + 1)

        if method in ["ewma", "both"]:
            self.df = self.df.with_columns(
                pl.col(column_name)
                .ewm_mean(alpha=alpha)
                .alias("ewma")
            )

        if method in ["sma", "both"]:
            self.df = self.df.with_columns(
                pl.col(column_name)
                .rolling_mean(window_size=span, min_periods=1)
                .alias("sma")
            )

        return self.df

    def get_peak_and_peak_position(self, column_name: str = "data", other_column: str = "duration") -> tuple:
        """Get the maximum value, its position, and the corresponding value from another column."""
        max_value = self.df[column_name].max()
        max_index = self.df[column_name].arg_max()
        other_column_value = self.df[max_index][other_column]
        return max_value, max_index, other_column_value
    
    
    def width_calculation(self, df: pl.DataFrame , column_name: str = "data", other_column: str= "duration") -> Tuple[Optional[int], Optional[float], Optional[float]]:
        """Calculates the width with param P0006."""
        P0006 = self.parameters.P0006  # Get P0006 parameter value
        
        # Check if maximum value exceeds P0006
        max_value = df[column_name].max()
        if max_value > P0006:
            # Find the index of the first value greater than P0006
            index_first_time_over = df.filter(pl.col(column_name) > P0006).select(pl.col(other_column)).first()

            # Position when first exceeds P0006
            pos_analog_over = index_first_time_over[0, 0] if index_first_time_over else None

            if pos_analog_over is not None:
                # Filter rows after the time_step where the value first exceeds P0006
                df_after_over = df.filter(pl.col(other_column) > pos_analog_over)

                # Find the index where the value drops below P0006
                index_first_time_under = df_after_over.filter(pl.col(column_name) < P0006).select(pl.col(other_column)).first()
                pos_analog_under = index_first_time_under[0, 0] if index_first_time_under else None

                # Calculate width as the difference between the two positions
                width = pos_analog_under - pos_analog_over if pos_analog_under is not None else None
            else:
                width = None
                pos_analog_over = None
                pos_analog_under = None
        else:
            width = None
            pos_analog_over = None
            pos_analog_under = None

        return width, pos_analog_over, pos_analog_under
    
    
    def integral_calculation(self, column_name: str = "data", other_column: str = "duration") -> float:
        """Calculates the integral using the trapezoidal method, calling the Rust function."""
        # Extract the necessary column data as NumPy arrays
        #from signal_rs import integral_calculation_rust
        analog_values = self.df[column_name].to_numpy()  # Convert to NumPy array
        time_steps = self.df[other_column].to_numpy()    # Convert to NumPy array
        
        # Extract P0001 parameter value
        P0001 = self.parameters.P0001

        # Call the Rust function to calculate the integral
        integral = integral_calculation_rust(analog_values, time_steps, P0001)
        print(f"Integral: {integral}")

        return integral
    
    
    def plot_unmodified_signal(self, df:pl.DataFrame =None ,column_name: str = "data", other_column: str = "duration",
                           path: str = "output", name: str = "0", mode: str = "markers", title: str= "title") -> go.Figure:
        """Plot the unmodified signal with color grading for each cycle."""
        if df is None:
            df = self.df
            
        fig = go.Figure()

        # Define a color scale (e.g., 'Viridis' or 'Blues')
        
        color_scale = 'Viridis'
        
        # Get the number of unique cycles
        cycles = df['run_counter'].unique()

        # Loop through each unique cycle and plot each cycle's data with increasing color
        for idx, cycle in enumerate(cycles):
            # Filter the data for the specific cycle using Polars syntax
            cycle_data = df.filter(pl.col('run_counter') == cycle)

            colors = sample_colorscale(color_scale, [i / (len(cycles) - 1) for i in range(len(cycles))])
            color = colors[idx]  # Get the color based on the cycle index
            
            # Add the trace to the figure with the specific color
            fig.add_trace(go.Scatter(
                x=(cycle_data[other_column]/1000).to_numpy(),  # Convert to numpy for compatibility with Plotly
                y=(cycle_data[column_name]).to_numpy(),  # Scale the signal
                mode=mode,
                name=f"Cycle {cycle}",  # Name the trace by cycle
                marker=dict(size=6, color=color),  # Set marker color based on the cycle index
                line=dict(color=color)
            ))

        # Update layout and axis titles
        fig.update_layout(
            title=f"{title}",  # Access the first channel
            xaxis_title="Time (ms)",
            yaxis_title="Signal (dig)",
            template="simple_white",
            font=dict(family="Courier New, monospace", size=14),
            coloraxis_colorbar=dict(title="Cycle Index")  # Adding color bar for reference
        )

        return fig

