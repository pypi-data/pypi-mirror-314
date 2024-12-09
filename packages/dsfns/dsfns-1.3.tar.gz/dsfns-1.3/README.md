## Installation

```bash
pip install dsfns
```

# FNS Package

Function Descriptions

1. outl_iqr(df, columns)
   Identifies and handles outliers in the specified columns using the Interquartile Range (IQR) method.
   Parameters:
   o df: DataFrame — The input data in which outliers will be detected.
   o columns: list — List of column names in which outliers need to be identified.

2. outl_winsor(df, column, capping_method='iqr')
   Applies Winsorization to cap outliers in the specified column using either IQR or other capping methods.
   Parameters:
   o df: DataFrame — The input data to apply Winsorization.
   o column: str — The name of the column to apply the Winsorization to.
   o capping_method: str, default 'iqr' — Method used to define the outlier thresholds (options: 'iqr' , std, 'quantiles' or 'mad').

3. outl_clip(df, columns)
   Clips extreme values to a predefined threshold in the specified columns, effectively handling outliers.
   Parameters:
   o df: DataFrame — The input data to clip outliers from.
   o columns: list — List of columns in which to clip the outliers.

4. miss_repl(df, columns, type='mean')
   Replaces missing values in the specified columns using a chosen method.
   Parameters:
   o df: DataFrame — The input data in which missing values will be replaced.
   o columns: list — List of column names where missing values need to be replaced.
   o type: str, default 'mean' — The method used for replacement ('mean', 'median', or mode)

5. miss_all(df)
   Identifies and returns all rows in the DataFrame that contain missing values with mean for numeric columns and mode (with index[0]) for object.
   Parameters:
   o df: DataFrame — The input data to check for missing values.

6. norm(df)
   Normalizes a given value (or a set of values) to specific scale [0, 1].
   Parameters:
   o df: data to be normalized.

7. outlierColumns(df)
   Returns a list of columns that contain outliers based on IQR.
   Parameters:
   o df: DataFrame — The input data to check for outliers.

#### VERSION 1.3

8. outlierCount(df, columns)
   Counts the number of outliers in the specified columns.
   Parameters:
   o df: DataFrame — The input data to count outliers in.
   o columns: list — List of columns to check for outliers.

9. highFrequency(df, perc=0.5)
   Identifies and returns columns where more than the given percentage (default 70%) of values are identical, typically used to detect low-variance or high-frequency columns.
   Parameters:
   o df: DataFrame — The input data to identify high-frequency columns.
   o perc: float, default 0.7 — The percentage threshold for identifying high-frequency columns.

10. miss_impute(df, columns, strategy='mean')
    The miss_impute function is designed to handle missing values in a pandas DataFrame by applying various imputation strategies. It utilizes the SimpleImputer from scikit-learn to efficiently fill missing values in specified columns.
    Parameters:
    o df: DataFrame — The input data to identify high-frequency columns.
    o columns (list): A list of column names in the DataFrame where missing values need to be imputed.
    o strategy (str, default='mean'):The imputation strategy to be applied. Options include:

    'mean': Replace missing values with the mean of the column.
    'median': Replace missing values with the median of the column.
    'mode' or 'most_frequent': Replace missing values with the most frequently occurring value in the column.
