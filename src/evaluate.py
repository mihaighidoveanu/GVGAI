import pandas as pd
from pathlib import Path
import os
from datetime import datetime

def gamename(gamepath):
    name = os.path.basename(gamepath)
    name, _ = os.path.splitext(name)
    return name

def readlog(logfile):
    df = pd.read_csv(logfile,)
    return df

def fullreport(data_dir):
    cols = ['name', 'game', 'win', 'score', 'time']
    table = pd.DataFrame(columns = cols)
    
    for file in os.listdir(data_dir):
        name = file.split('_')[0]
        file = os.path.join(data_dir, file)
        df = readlog(file)
        df['name'] = name
        # df['game'] = df['game'].apply(gamename)
        table = pd.concat([table, df], sort = False)

    print(table['win'].dtype)
    table = table.sort_values(by = ['game', 'win', 'score'], ascending = [True, False, False])
    table = table[cols]
    return table

def savereport(df, out_dir):
    timestamp = datetime.now()
    out_name = f'report_{timestamp.month}.{timestamp.day}.{timestamp.hour}.{timestamp.minute}.{timestamp.second}.csv'
    out_path = os.path.join(out_dir, out_name)
    df.to_csv(out_path, index = None)

def main(data_dir, out_dir):
    table = fullreport(data_dir)
    savereport(table, out_dir)
    print(table)
    table = table.groupby('name').agg({
        'win' : ['median', 'mean', 'std' ],
        'score' : ['median', 'mean', 'std', 'max', 'min'],
        })
    table = table.sort_values(by = [('win', 'mean')], ascending = [False])
    print()
    print(table)

import fire
if __name__ == '__main__' :
    fire.Fire(main)
