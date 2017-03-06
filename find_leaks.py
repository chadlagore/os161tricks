import os

import pandas as pd

filename = 'output.csv'
os161_folder = '~/os161/root/kernel'


def get_leak_table():
    '''
    Return the leak table (in filename)
    '''
    return pd.read_csv(filename, names=['size', 'address'])


def clean_tbl(tbl):
    '''
    Return a cleaned up table. Remove excess strings etc.
    '''
    tbl['address'] = (tbl['address']
                      .replace(regex=True, to_replace='allocated at', value=''))
    tbl['size'] = (tbl['size']
                   .replace(regex=True, to_replace='bytes at.*', value='')
                   .str.strip().astype(int))
    tbl['line'] = 0
    return tbl


def call_addr2line(tbl):
    '''
    Call os161 addr2line function.
    '''
    for ix in tbl.index:
        addr = tbl.loc[ix]['address']
        syscall = 'os161-addr2line -e {} {}'.format(os161_folder, addr)
        response = os.popen(syscall).read()[40:]
        tbl['line'].loc[ix] = response
    return tbl


def main():
    tbl = get_leak_table().drop_duplicates(subset='address')
    tbl = clean_tbl(tbl).reset_index()[['size', 'address', 'line']]
    tbl = call_addr2line(tbl)
    print(tbl)


if __name__ == '__main__':
    main()
