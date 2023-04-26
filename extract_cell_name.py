import pandas as pd

def extract_cel_nam(df):
    col_name=df.columns[3]
    if (col_name=='Cell'):
        #print(col_name)
        df['a'] = df[str(col_name)].str.slice(start=21)
        df[['r','x', 'y','z']] = df['a'].str.split(',',3, expand=True)
        df[['b','Cell']] = df['y'].str.split('=',1, expand=True)
        col_x_name=df.columns[2]
        df.rename(columns={str(col_x_name): 'Site'}, inplace=True)
        df = df.drop(['r','b','a','x','y','z'], axis=1, errors='ignore')
        col_x_name=df.columns[2]
        print(df.head())
    else:
        df['a'] = df[str(col_name)].str.slice(start=6)
        df[['Cell','b','c']] = df['a'].str.split(',',2, expand=True)
        df[str(col_name)]=df['Cell']
        df[['Site','x']] = df[str(col_name)].str.split('_',1, expand=True)
        scol_name=df.columns[2]
        df[str(scol_name)]=df['Site']
        df = df.drop(['b','a','c','x','Site','Cell'], axis=1, errors='ignore')
        df.rename(columns={str(scol_name): 'Site'}, inplace=True)
        df.rename(columns={str(col_name): 'Cell'}, inplace=True)
    return df
