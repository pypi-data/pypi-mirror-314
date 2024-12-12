## Installation

```bash
pip install dsfns
```

# FNS Package

## FUNCTION DESCRIPTIONS

1. Outlier_IQR(df, columns)
   Identifies and handles outliers in the specified columns using the Interquartile Range (IQR) method.
   Parameters:

    - df: DataFrame — The input data in which outliers will be detected.
    - columns: list — List of column names in which outliers need to be identified.

2. Outlier_Winsorizer(df, column, capping_method='iqr')
   Applies Winsorization to cap outliers in the specified column using either IQR or other capping methods.
   Parameters:

    - df: DataFrame — The input data to apply Winsorization.
    - column: str — The name of the column to apply the Winsorization to.
    - capping_method: str, default 'iqr' — Method used to define the outlier thresholds (options: 'iqr' , std, 'quantiles' or 'mad').

3. Outlier_Clip(df, columns)
   Clips extreme values to a predefined threshold in the specified columns, effectively handling outliers.
   Parameters:

    - df: DataFrame — The input data to clip outliers from.
    - columns: list — List of columns in which to clip the outliers.

4. MissingVal_Repl(df, columns, type='mean')
   Replaces missing values in the specified columns using a chosen method.
   Parameters:

    - df: DataFrame — The input data in which missing values will be replaced.
    - columns: list — List of column names where missing values need to be replaced.
    - type: str, default 'mean' — The method used for replacement ('mean', 'median', or mode)

5. MissingVal_Imputer(df,columns,strategy='mean')
   The MissingVal_Imputer function is designed to handle missing values in specified columns of a pandas DataFrame using different imputation strategies. It replaces missing values (NaN) with appropriate values based on the chosen strategy.
   Parameters:

    - df (pandas.DataFrame): The input DataFrame where missing values need to be imputed.
    - columns (list): A list of column names where missing value imputation is to be applied.
    - strategy (str, default='mean'):The strategy for imputing missing values. Supported values:
      'mean': Replaces missing values with the mean of the column.
      'median': Replaces missing values with the median of the column.
      'mode': Replaces missing values with the most frequent value in the column (converted to 'most_frequent' internally).

6. MissingVal_Fillna(df)
   Identifies and returns all rows in the DataFrame that contain missing values with mean for numeric columns and mode (with index[0]) for object.
   Parameters:

    - df: DataFrame — The input data to check for missing values.

#### VERSION 1.3

7. outlierColumns(df)
   Returns a list of columns that contain outliers based on IQR.
   Parameters:

    - df: DataFrame — The input data to check for outliers.

8. outlierCount(df, columns)
   Counts the number of outliers in the specified columns.
   Parameters:

    - df: DataFrame — The input data to count outliers in.
    - columns: list — List of columns to check for outliers.

9. highFrequency(df, perc=0.5)
   Identifies and returns columns where more than the given percentage (default 70%) of values are identical, typically used to detect low-variance or high-frequency columns.
   Parameters:
    - df: DataFrame — The input data to identify high-frequency columns.
    - perc: float, default 0.5 — The percentage threshold for identifying high-frequency columns.

#### VERSION 1.4

10. Encoding(df, method='label')
    Encodes categorical columns into numeric labels for compatibility with machine learning algorithms.
    Parameters:

    -   df: A Pandas DataFrame containing the dataset.
    -   method: 'label' for label encoding OR 'onehot' for OneHotEncoding

11. Scaler(df, method='minmax')
    Scales numerical data for better performance during machine learning model training.
    Parameters:

    -   df: A Pandas DataFrame containing numeric data.
    -   method: Specifies the scaling technique to use. Options are:
        'minmax' (default): Rescales data to a range of 0 to 1.
        'standard': Standardizes data to have a mean of 0 and a standard deviation of 1.
        'robust': Scales data using the median and interquartile range, making it robust to outliers.

#### VERSION 1.5

General code fixes

#### VERSION 1.6

12. outlierDecider(df, columns, output='list')
    The outlierDecider function helps identify columns in a DataFrame that either have low variance (where the Interquartile Range [IQR] is zero) or potential outliers (based on the IQR rule). The function supports two modes of output:

    list Mode: Returns and prints two separate lists:
    LowVar: Columns with low variance (IQR = 0).
    Repl: Columns where outliers may need to be addressed (IQR > 0).

    summary Mode: Prints a detailed summary for each column, indicating whether it has low variance or requires outlier replacement.

    Parameters:
    df: A pandas DataFrame containing the data to analyze.
    columns: A list of column names to evaluate for low variance or outliers.
    output: A string specifying the mode of operation ('list' or 'summary').
    'list': Generates two lists (LowVar and Repl) and prints them.
    'summary': Prints a simple summary for each column.
