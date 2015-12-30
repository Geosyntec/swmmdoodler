import os
import pandas as pd

def swmm_format(df, col, path, qfoul):
    '''
    Takes a pandas.DataFrame and a column in that dataframe
    and saves a formated df in the standard user-prepared format.
    '''

    if qfoul:
        header = ['{0} Flow, cfs (converted from MGD)'
            .format(col)
            .replace('U.1','_qfoul')]

        path = os.path.join(path, '{0}.txt'.format(col)
            .replace('U.1','_qfoul'))
    if not qfoul:
        header = ['{0} Flow, cfs (converted from MGD)'
            .format(col)
            .replace('R.1','r_ts.1')]
        path = os.path.join(path, '{0}.txt'.format(col)
            .replace('R.1','r.1'))

    if not os.path.exists(path.rpartition('\\')[0]):
        os.makedirs(path.rpartition('\\')[0])

    df[[col]].to_csv(
        path,
        sep='\t',
        date_format='%m/%d/%Y %H:%M:%S',
        header=header,
        index_label=[';Date Time']
    )

def read_InfoWorks_files(path, drop_cols=['Seconds'], drop_rows=['[Hr:Min:s]']):
    all_ts = pd.read_csv(path, index_col=[0], parse_dates=[0])
    if drop_cols is not None:
        all_ts = all_ts.drop(drop_cols, axis=1)
    if drop_rows is not None:
        all_ts = all_ts.drop(drop_rows)
    return all_ts
