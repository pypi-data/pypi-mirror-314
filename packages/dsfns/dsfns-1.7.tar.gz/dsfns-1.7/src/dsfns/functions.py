import pandas as pd
import numpy as np
from feature_engine.outliers import Winsorizer
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler



def Outlier_IQR(df,columns):
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (1.5 * IQR)
        LL = df[i].quantile(0.25) - (1.5 * IQR)

        df[i] = np.where(df[i] > UL, UL, np.where(df[i] < LL , LL, df[i]))
    return df.head()



def Outlier_Winsorizer(df, column, capping_method='iqr'):
    winsor = Winsorizer(capping_method=capping_method,
                        tail='both',
                        fold=1.5,
                        variables=[column])
    
    df[column] = winsor.fit_transform(df[[column]])
    return df.head()



def Outlier_Clip(df,columns):
    for column in columns:
        df[column] = df[column].clip(lower=df[column].quantile(0.05), upper=df[column].quantile(0.95))
    return df.head()


def MissingVal_Repl(df, columns, type='mean'):
    for i in columns:
        if type == 'mean':
            value = df[i].mean()
        elif type == 'median':
            value = df[i].median()
        elif type == 'mode':
            value = df[i].mode()[0]  
        
        df[i] = df[i].replace(np.nan, value)
    return df.head()


def MissingVal_Imputer(df,columns,strategy='mean'):
    if strategy == 'mode':
        strategy = 'most_frequent'

    imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
    for i in columns:
        df[i] = pd.DataFrame(imputer.fit_transform(df[[i]]))
    return df.head()
    

def MissingVal_Fillna(df):
    num_cols = df.select_dtypes(include=['float', 'int']).columns
    for x in num_cols:
        df[x] = df[x].fillna(df[x].mean())

    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for y in cat_cols:
        df[y] = df[y].fillna(df[y].mode()[0])
    return df.head()


## VERSION 1.3

def outlierColumns(df):
    outl_cols = []
    for i in df.columns:
        if pd.api.types.is_numeric_dtype(df[i]):
            IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
            LLi = df[i].quantile(0.25) - (1.5 * IQR)
            ULi = df[i].quantile(0.75) + (1.5 * IQR)
            
            if ((df[i] < LLi) | (df[i] > ULi)).sum() > 0:
                outl_cols.append(i)
    return outl_cols



def outlierCount(df, columns):
    plt.ioff()
    for i in columns:
        oc = len(plt.boxplot(df[i])['fliers'][0].get_ydata())
        print(f"{i} = {oc}")



def highFrequency(df, perc=0.5):
    high_freq_columns = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            value_counts = df[col].value_counts()
            max_count = value_counts.max()
            total_count = len(df)
            
            if max_count / total_count > perc:
                high_freq_columns.append(col)
    return high_freq_columns


## VERSION 1.4

def Encoding(df,method='label'):
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if method == 'label':
        label = LabelEncoder()
        for col in cat_cols:
            df[col] = label.fit_transform(df[col])
    elif method == 'onehot':
        df = pd.get_dummies(df, columns=cat_cols)
    return df.head()


def Scaling(df, method='minmax'):
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'robust':
        scaler = RobustScaler()
        
    df = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)
    return df.head()
    

## VERSION 1.6

def outlierDecider(df,columns,output='list'):
    LowVar = []
    Repl = []
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (1.5 * IQR)
        LL = df[i].quantile(0.25) - (1.5 * IQR)

        if output == 'list':
            if IQR == 0:
                LowVar.append(i)
            else:
                Repl.append(i)    

        elif output == 'summary':
            if IQR == 0:
                print(f"{i} : Low Variance")
            else:
                print(f"{i} : Replace Outliers") 

    if output == 'list':
        print(f"LowVariance :{LowVar}")
        print(f"ReplaceOutliers : {Repl}")
