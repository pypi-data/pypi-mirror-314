import unittest
import polars as pl
import pandas as pd
from analysis import amvSignalAnalysis, amvParameters  # Update with the correct import path

# Sample data for testing
sample_data = {
    "column1": [1, 2, 3, 4, 5],
    "column2": [10, 20, 30, 40, 50],
    "column3": [100, 200, 300, 400, 500],
    "column4": [1000, 2000, 3000, 4000, 5000]
}
df_pandas = pd.DataFrame(sample_data)
df_polars = pl.from_pandas(df_pandas)

class TestAmvSignalAnalysis(unittest.TestCase):

    def setUp(self):
        # Set up a signal analysis instance with pandas and polars
        self.signal_analysis_pandas = amvSignalAnalysis(df_pandas)
        self.signal_analysis_polars = amvSignalAnalysis(df_polars)

    def test_initialization_pandas(self):
        # Test that the class is initialized with a pandas DataFrame
        self.assertEqual(self.signal_analysis_pandas.backend, "pandas")
        self.assertIsInstance(self.signal_analysis_pandas.df, pl.DataFrame)  # Should be converted to Polars DataFrame

    def test_initialization_polars(self):
        # Test that the class is initialized with a polars DataFrame
        self.assertEqual(self.signal_analysis_polars.backend, "polars")
        self.assertIsInstance(self.signal_analysis_polars.df, pl.DataFrame)

    def test_invalid_dataframe_type(self):
        # Test that an exception is raised for an unsupported DataFrame type
        with self.assertRaises(TypeError):
            amvSignalAnalysis("invalid_data")  # Passing a string instead of DataFrame

    def test_get_column_names(self):
        # Test if get_column_names returns correct column names
        column_names = self.signal_analysis_pandas.get_column_names()
        self.assertEqual(column_names, ["column1", "column2", "column3", "column4"])

    def test_filter_rows(self):
        # Test if filter_rows filters the rows correctly
        filtered_df = self.signal_analysis_pandas.filter_rows("column1", 3)
        
        # Convert Polars DataFrame to Pandas DataFrame (for testing)
        filtered_rows = filtered_df.to_pandas()
        
        # Check if filtering worked as expected
        self.assertEqual(len(filtered_rows), 1)
        self.assertEqual(filtered_rows.iloc[0]["column1"], 3)

        # Test filtering on another column
        filtered_df = self.signal_analysis_pandas.filter_rows("column2", 20)
        filtered_rows = filtered_df.to_pandas()
        
        # Check if the filtered row matches the expected value
        self.assertEqual(len(filtered_rows), 1)
        self.assertEqual(filtered_rows.iloc[0]["column2"], 20)

    def test_add_column(self):
        # Test if add_column adds a new column to the DataFrame
        new_values = [100, 200, 300, 400, 500]
        updated_df = self.signal_analysis_pandas.add_column("column3", new_values)
        self.assertIn("column3", updated_df.columns)
        self.assertEqual(updated_df["column3"].to_list(), new_values)

    def test_to_pandas(self):
        # Test if to_pandas correctly converts the Polars DataFrame to Pandas DataFrame
        pandas_df = self.signal_analysis_polars.to_pandas()
        self.assertIsInstance(pandas_df, pd.DataFrame)
        self.assertEqual(pandas_df.shape, df_pandas.shape)  # Same shape as the original Pandas DataFrame

    def test_amvParameters_initialization(self):
        # Test initialization of amvParameters with custom values
        params = amvParameters(P0000=5000, P0001=10)
        self.assertEqual(params.P0000, 5000)
        self.assertEqual(params.P0001, 10)
        self.assertEqual(params.P0002, 40)  # Default value

        # Test initialization with default values
        default_params = amvParameters()
        self.assertEqual(default_params.P0000, 4095)
        self.assertEqual(default_params.P0001, 5)

    def test_str_method(self):
        # Test if the __str__ method works as expected
        result = str(self.signal_analysis_pandas)
        self.assertIn("Converted to Polars DataFrame", result)
        self.assertIn("Parameters", result)

if __name__ == "__main__":
    unittest.main()