import os

import pandas as pd

filename = 'output.csv'


def get_leak_table():
    return pd.read_csv(filename, names=['size', 'address'])


def clean_tbl(tbl):
    tbl['address'] = (tbl['address']
                      .replace(regex=True, to_replace='allocated at', value=''))
    tbl['size'] = (tbl['size']
                   .replace(regex=True, to_replace='bytes at.*', value='')
                   .str.strip().astype(int))
    tbl['line'] = 0
    return tbl


def print_results(tbl):
    for ix in tbl.index:
        addr = tbl.loc[ix]['address']
        syscall = 'os161-addr2line -e ~/os161/root/kernel {}'.format(addr)
        response = os.popen(syscall).read()[40:]
        tbl['line'].loc[ix] = response
    print(tbl)


def main():
    tbl = get_leak_table().drop_duplicates(subset='address')
    tbl = clean_tbl(tbl).reset_index()[['size', 'address', 'line']]
    print_results(tbl)


if __name__ == '__main__':
    main()
