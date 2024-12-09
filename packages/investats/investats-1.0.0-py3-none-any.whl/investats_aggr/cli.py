#!/usr/bin/env python3

import argparse
import csv
import sys

from dateutil import parser as dup
from typing import TextIO


def pair_items_to_dict(items: list[str]) -> dict[str, str]:
    '''
    Converts a list of (asset name, input file) pairs, specified as a simple
    array of items, to a Python dictionary
    '''
    len_items = len(items)

    if len_items % 2 != 0:
        raise ValueError('The length of pair items must be an even number')
    if len_items < 4:
        raise ValueError('The number of pairs must be >= 2')

    return {items[i]: items[i + 1] for i in range(0, len_items, 2)}


def load_data(file: TextIO):
    '''
    Loads data from a CSV file
    '''
    data = list(csv.DictReader(file))

    float_keys = [k for k in data[0].keys() if k != 'datetime']

    for x in data:
        yield {'datetime': dup.parse(x['datetime'])} | \
            {k: float(x[k]) for k in float_keys}


def save_data(data: list[dict], file: TextIO, fmt_days: str = '',
              fmt_src: str = '', fmt_dst: str = '', fmt_rate: str = '',
              fmt_yield: str = ''):
    '''
    Saves data into a CSV file
    '''
    func_days = str if fmt_days == '' else lambda x: fmt_days.format(x)
    func_src = str if fmt_src == '' else lambda x: fmt_src.format(x)
    func_dst = str if fmt_dst == '' else lambda x: fmt_dst.format(x)
    func_rate = str if fmt_rate == '' else lambda x: fmt_rate.format(x)
    func_yield = str if fmt_yield == '' else lambda x: fmt_yield.format(x)

    def get_fmt(key: str):
        '''
        Determines the format function for a specific field key
        '''
        if key == 'datetime' or key.endswith(':latest_cgt'):
            return str

        if key in ['diff_days', 'tot_days']:
            return func_days

        if key in ['diff_src', 'tot_src', 'tot_dst_as_src',
                   'chkpt_gain_src', 'chkpt_gain_net_src',
                   'tot_gain_src', 'tot_gain_net_src'] \
            or key.endswith((':diff_src', ':tot_src', ':tot_dst_as_src',
                             ':chkpt_gain_src', ':chkpt_gain_net_src',
                             ':tot_gain_src', ':tot_gain_net_src')):
            return func_src

        if key.endswith((':diff_dst', ':tot_dst')):
            return func_dst

        if key.endswith((':latest_rate', ':avg_rate')):
            return func_rate

        if key in ['chkpt_yield', 'chkpt_apy',
                   'global_yield', 'global_apy'] \
            or key.endswith((':chkpt_yield', ':chkpt_apy',
                            ':global_yield', ':global_apy')):
            return func_yield

        raise ValueError(f'Unsupported key: {key}')

    fields = {k: get_fmt(k) for k in data[0].keys()}

    print(','.join(fields.keys()), file=file)
    for x in data:
        print(','.join(f(x[k]) for k, f in fields.items()), file=file)


def aggregate_series(named_series: dict[str, list[dict]]):
    '''
    Aggregates multiple investats data series into a single one
    '''
    if len(named_series) < 2:
        raise ValueError('The number of series must be >= 2')

    names = list(named_series.keys())
    series = list(named_series.values())

    length = len(series[0])
    for s in series[1:]:
        len_s = len(s)
        if len_s != length:
            raise ValueError('Series are not all the same length: '
                             f'{len_s} != {length}')

    for i in range(length):
        d = series[0][i]['datetime']
        for s in series[1:]:
            d_s = s[i]['datetime']
            if d_s != d:
                raise ValueError('Mismatching checkpoint datetime: '
                                 f'{d_s} != {d}')

    KEYS_COMMON = ['datetime', 'diff_days', 'tot_days']
    KEYS_SUM = ['diff_src', 'tot_src', 'tot_dst_as_src',
                'chkpt_gain_src', 'chkpt_gain_net_src',
                'tot_gain_src', 'tot_gain_net_src']

    keys_specific = [k for k in series[0][0].keys() if k not in KEYS_COMMON]

    result = []

    for i in range(length):
        named_entries = {name: named_series[name][i] for name in names}
        entries = list(named_entries.values())

        result.append({k: entries[0][k] for k in KEYS_COMMON} |
                      {k: sum(e[k] for e in entries) for k in KEYS_SUM} |
                      {f'{name}:{k}': named_entries[name][k]
                       for name in names for k in keys_specific})

    prev_aggr = None

    for aggr in result:
        # We calculate the "aggregate yields" using the following alternative
        # (but equivalent) formulas

        aggr['chkpt_yield'] = 0 if prev_aggr is None \
            or prev_aggr['tot_dst_as_src'] == 0 \
            else aggr['chkpt_gain_src'] / prev_aggr['tot_dst_as_src']

        aggr['chkpt_apy'] = 0 if aggr['chkpt_yield'] == 0 \
            or aggr['diff_days'] == 0 \
            else (1 + aggr['chkpt_yield']) ** (365 / aggr['diff_days']) - 1

        aggr['global_yield'] = 0 if aggr['tot_src'] == 0 \
            else aggr['tot_gain_src'] / aggr['tot_src']

        aggr['global_apy'] = 0 if aggr['global_yield'] == 0 \
            or aggr['tot_days'] == 0 \
            else (1 + aggr['global_yield']) ** (365 / aggr['tot_days']) - 1

        prev_aggr = aggr

        yield aggr


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Aggregate multiple investats data series into a single one'
    )

    parser.add_argument('pairs', metavar='PAIRS', type=str, nargs='+',
                        help='List of (asset name, input file) pairs, as '
                        'array of items (e.g. AAA stats-aaa.csv '
                        'BBB stats-bbb.csv)')

    parser.add_argument('--fmt-days', type=str, default='',
                        help='If specified, formats the days values with this '
                        'format string (e.g. "{:.2f}")')
    parser.add_argument('--fmt-src', type=str, default='',
                        help='If specified, formats the SRC values with this '
                        'format string (e.g. "{:.2f}")')
    parser.add_argument('--fmt-dst', type=str, default='',
                        help='If specified, formats the DST values with this '
                        'format string (e.g. "{:.4f}")')
    parser.add_argument('--fmt-rate', type=str, default='',
                        help='If specified, formats the rate values with this '
                        'format string (e.g. "{:.6f}")')
    parser.add_argument('--fmt-yield', type=str, default='',
                        help='If specified, formats the yield values with this '
                        'format string (e.g. "{:.4f}")')

    args = parser.parse_args(argv[1:])

    ############################################################################

    named_series = {}

    for name, file in pair_items_to_dict(args.pairs).items():
        with open(file, 'r') as f:
            named_series[name] = list(load_data(f))

    save_data(list(aggregate_series(named_series)), sys.stdout, args.fmt_days,
              args.fmt_src, args.fmt_dst, args.fmt_rate, args.fmt_yield)

    return 0
