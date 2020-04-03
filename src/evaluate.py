import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import preprocessing

# discard paths from game name
def gamename(gamepath):
    name = os.path.basename(gamepath)
    name, _ = os.path.splitext(name)
    return name

# read csv file
def readlog(logfile):
    df = pd.read_csv(logfile,)
    return df

# merge all log files into one table
def fullreport(data_dir):
    cols = ['name', 'game', 'win', 'score', 'time']
    table = pd.DataFrame(columns = cols)
    
    for file in Path(data_dir).glob('*.csv'):
        file = str(file)
        name = "_".join(file.split('_')[:-1])
        df = readlog(file)
        df['name'] = name
        df['game'] = df['game'].apply(gamename)
        table = pd.concat([table, df], sort = False)

    tables = []
    tables.append(table.pivot(index = 'name', columns = 'game', values = 'win'))
    tables.append(table.pivot(index = 'name', columns = 'game', values = 'score'))

    configs = getconfigs(tables[0])
    getconfigs(tables[1], with_configs = False)
    # print(table.loc['name'])
    # table = table.sort_values(by = ['game', 'win', 'score'], ascending = [True, False, False])
    # table = table[cols]
    return tables, configs

# save report to disk
def savereport(df, out_dir, out_name = 'report'):
    timestamp = datetime.now()
    out_name = f'{out_name}_{timestamp.month}.{timestamp.day}.{timestamp.hour}.{timestamp.minute}.{timestamp.second}.csv'
    out_path = os.path.join(out_dir, out_name)
    df.to_csv(out_path)

# get stats for each algorithm aggregated for all games
def agg(df):
    # df = df.groupby('name').agg({
    #     'win' : ['median', 'mean', 'std' ],
    #     'score' : ['median', 'mean', 'std', 'max', 'min'],
    #     })
    df = df.groupby('name').mean()
    df = df.sort_values(by = ['win', 'score', 'time'], ascending = [False, False, True])
    return df

def getparams(name):
    name = os.path.basename(name)
    params = name.split('-')
    d = {}
    for param in params:
        key, value = param.split("=")
        value = float(value)
        key = key.lower()
        d[key] = value

    return d

def nextchar(char):
    return chr(ord(char) + 1)

# get hyperparams (k, d, etc.)
def getconfigs(df, with_configs = True):
    configs = pd.DataFrame(columns = ['id', 'bootstrap' , 'depth', 'k', 'high_depth', 'low_k', 'high_k', 'window', 'sparse_depth', 'sparse_k', ])
    names = df.index.values.tolist()
    id = 'A'
    for i, name in enumerate(names):
        names[i] = id
        if with_configs:
            params = getparams(name)
            row = [id]
            for col in configs.columns[1:]:
                row.append(params.get(col))
            configs.loc[i] = row
        id = nextchar(id)

    df.index = names
    if with_configs:
       return configs

def heatmap(df, scale = False):
    x = df.iloc[:, 1:].values
    if scale:
        min_max_scaler = preprocessing.StandardScaler()
        x = min_max_scaler.fit_transform(x)
    sns.heatmap(x)
    plt.show()

def main(data_dir, out_dir):
    tables, configs = fullreport(data_dir)
    savereport(tables[0], out_dir, 'wins')
    savereport(tables[0], out_dir, 'scores')
    savereport(configs, out_dir, 'configs')
    print(tables[0])
    print('Sort on Wins')
    print(tables[0].mean(axis = 1).sort_values(ascending = False))
    print()
    print('Sort on Score')
    print(tables[1].mean(axis = 1).sort_values(ascending = False))
    # table = agg(table)
    print()
    heatmap(tables[0])
    heatmap(tables[1], scale = True)

import fire
if __name__ == '__main__' :
    fire.Fire(main)
