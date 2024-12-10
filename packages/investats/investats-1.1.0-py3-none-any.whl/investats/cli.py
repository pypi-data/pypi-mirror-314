#!/usr/bin/env python3

import argparse
import sys

from contextlib import ExitStack
from datetime import datetime as dt
from datetime import date
from typing import TextIO

import yaml


def is_aware(d: dt):
    '''
    Returns true if the datetime object `d` is timezone-aware, false otherwise.
    See https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    '''
    return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None


def load_data(file: TextIO) -> list[dict]:
    '''
    Loads data from a YAML file
    '''
    data = yaml.safe_load(file)

    if data[0]['type'] != 'invest':
        raise ValueError('The first entry must be of type "invest"')

    # YAML supports parsing dates out of the box if they are in the correct
    # format (ISO-8601). See
    # https://symfony.com/doc/current/components/yaml/yaml_format.html#dates

    for entry in data:
        if not entry['type'] in ['invest', 'chkpt']:
            raise ValueError('Invalid entry type: ' + str(entry['type']))

        if not isinstance(entry['datetime'], dt):
            if not isinstance(entry['datetime'], date):
                raise ValueError('Invalid datetime type: ' +
                                 str(entry['datetime']))

            entry['datetime'] = dt.combine(entry['datetime'], dt.min.time())

        if not is_aware(entry['datetime']):
            entry['datetime'] = entry['datetime'].astimezone()

        if entry['type'] == 'invest' and not any([
            'inv_src' not in entry and 'inv_dst' in entry and 'rate' in entry,
            'inv_src' in entry and 'inv_dst' not in entry and 'rate' in entry,
            'inv_src' in entry and 'inv_dst' in entry and 'rate' not in entry,
        ]):
            raise ValueError('Invalid entry ' + str(entry) + ': exactly two '
                             'values among "inv_src", "inv_dst" and "rate" '
                             'must be provided for each entry of '
                             'type "invest"')

    for i in range(1, len(data)):
        prev, curr = data[i - 1], data[i]

        if prev['type'] == 'invest':
            if prev['datetime'] > curr['datetime']:
                raise ValueError('Invalid entry order: ' +
                                 str(prev['datetime']) + ' > ' +
                                 str(curr['datetime']))
        else:
            if prev['datetime'] >= curr['datetime']:
                raise ValueError('Invalid entry order: ' +
                                 str(prev['datetime']) + ' >= ' +
                                 str(curr['datetime']))

    return data


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

    fields = {
        'datetime': str,

        'diff_days': func_days,
        'tot_days': func_days,

        'diff_src': func_src,
        'diff_dst': func_dst,
        'latest_rate': func_rate,

        'tot_src': func_src,
        'tot_dst': func_dst,
        'avg_rate': func_rate,

        'tot_dst_as_src': func_src,

        'chkpt_yield': func_yield,
        'chkpt_apy': func_yield,
        'global_yield': func_yield,
        'global_apy': func_yield,

        'latest_cgt': str,

        'chkpt_gain_src': func_src,
        'chkpt_gain_net_src': func_src,
        'tot_gain_src': func_src,
        'tot_gain_net_src': func_src,
    }

    print(','.join(fields.keys()), file=file)
    for x in data:
        print(','.join(f(x[k]) for k, f in fields.items()), file=file)


def complete_invest_entry(entry_in: dict) -> dict:
    '''
    Complete an entry of type "invest" with the missing fields that can be
    calculated from the others
    '''
    entry_out = entry_in.copy()

    if 'inv_src' not in entry_out:
        entry_out['inv_src'] = entry_out['inv_dst'] * entry_out['rate']
    elif 'inv_dst' not in entry_out:
        entry_out['inv_dst'] = 0 if entry_out['rate'] == 0 else \
            entry_out['inv_src'] / entry_out['rate']
    elif 'rate' not in entry_out:
        entry_out['rate'] = 0 if entry_out['inv_dst'] == 0 else \
            entry_out['inv_src'] / entry_out['inv_dst']

    return entry_out


def compute_stats(data: list[dict]):
    '''
    Computes the statistics
    '''
    prev_out = None

    diff_src, diff_dst, latest_rate = 0, 0, 0

    for entry_in in data:
        # - entry_in['datetime']: date and time of the entry (timezone-aware)
        # - entry_in['type']: can be "invest" or "chkpt" (checkpoint)
        # - entry_in['notes']: notes (optional)

        if entry_in['type'] == 'invest':
            entry_in = complete_invest_entry(entry_in)

            # - entry_in['inv_src']: invested SRC
            # - entry_in['inv_dst']: invested DST
            # - entry_in['rate']: current SRC/DST rate

            diff_src += entry_in['inv_src']
            diff_dst += entry_in['inv_dst']
            latest_rate = entry_in['rate']
        elif entry_in['type'] == 'chkpt':
            entry_out = {}

            # - entry_out['datetime']: same date and time of the checkpoint

            entry_out['datetime'] = entry_in['datetime']

            # - entry_out['diff_days']: days passed since the last checkpoint
            # - entry_out['tot_days']: days passed since the first checkpoint

            if prev_out is None:
                entry_out['diff_days'] = 0
                entry_out['tot_days'] = 0
            else:
                entry_out['diff_days'] = (
                    entry_out['datetime'] - prev_out['datetime']
                ).total_seconds() / 60 / 60 / 24
                entry_out['tot_days'] = prev_out['tot_days'] + \
                    entry_out['diff_days']

            # - entry_out['diff_src']: invested SRC since the last checkpoint
            # - entry_out['diff_dst']: invested DST since the last checkpoint
            # - entry_out['latest_rate']: latest SRC/DST rate (at the latest
            #   operation)

            entry_out['diff_src'], entry_out['diff_dst'] = diff_src, diff_dst
            entry_out['latest_rate'] = latest_rate

            # - entry_out['tot_src']: total invested SRC
            # - entry_out['tot_dst']: total invested DST
            # - entry_out['avg_rate']: ratio between tot_src and tot_dst

            if prev_out is None:
                entry_out['tot_src'] = diff_src
                entry_out['tot_dst'] = diff_dst
            else:
                entry_out['tot_src'] = prev_out['tot_src'] + diff_src
                entry_out['tot_dst'] = prev_out['tot_dst'] + diff_dst

            entry_out['avg_rate'] = 0 if entry_out['tot_dst'] == 0 \
                else entry_out['tot_src'] / entry_out['tot_dst']

            # - entry_out['tot_dst_as_src']: how many SRC would be obtained by
            #   converting tot_dst using latest_rate

            entry_out['tot_dst_as_src'] = entry_out['tot_dst'] * latest_rate

            # - entry_out['chkpt_yield']: yield w.r.t. the last checkpoint
            # - entry_out['chkpt_apy']: APY w.r.t. the last checkpoint

            entry_out['chkpt_yield'] = 0 if prev_out is None \
                or prev_out['latest_rate'] == 0 \
                else latest_rate / prev_out['latest_rate'] - 1

            entry_out['chkpt_apy'] = 0 if entry_out['chkpt_yield'] == 0 \
                or entry_out['diff_days'] == 0 \
                else (1 + entry_out['chkpt_yield']) ** \
                (365 / entry_out['diff_days']) - 1

            # - entry_out['global_yield']: yield w.r.t. avg_rate
            # - entry_out['global_apy']: APY w.r.t. avg_rate

            entry_out['global_yield'] = 0 if entry_out['avg_rate'] == 0 \
                else latest_rate / entry_out['avg_rate'] - 1

            entry_out['global_apy'] = 0 if entry_out['global_yield'] == 0 \
                or entry_out['tot_days'] == 0 \
                else (1 + entry_out['global_yield']) ** \
                (365 / entry_out['tot_days']) - 1

            # - entry_in['cgt']: Capital Gains Tax
            # - entry_out['latest_cgt']: latest CGT (Capital Gains Tax)

            entry_out['latest_cgt'] = entry_in['cgt'] if 'cgt' in entry_in \
                else prev_out['latest_cgt'] if prev_out is not None \
                else 0

            # - entry_out['chkpt_gain_src']: gain w.r.t. the last chkpt
            # - entry_out['chkpt_gain_net_src']: net gain w.r.t. the last chkpt

            if prev_out is None:
                entry_out['chkpt_gain_src'] = 0
                entry_out['chkpt_gain_net_src'] = 0
            else:
                entry_out['chkpt_gain_src'] = entry_out['tot_dst_as_src'] - \
                    (prev_out['tot_dst_as_src'] + entry_out['diff_src'])
                entry_out['chkpt_gain_net_src'] = \
                    entry_out['chkpt_gain_src'] * (1 - entry_out['latest_cgt'])

            # - entry_out['tot_gain_src']: gain w.r.t. tot_src
            # - entry_out['tot_gain_net_src']: net gain w.r.t. tot_src

            entry_out['tot_gain_src'] = \
                entry_out['tot_dst_as_src'] - entry_out['tot_src']
            entry_out['tot_gain_net_src'] = \
                entry_out['tot_gain_src'] * (1 - entry_out['latest_cgt'])

            diff_src, diff_dst = 0, 0

            prev_out = entry_out

            yield entry_out
        else:
            raise ValueError('Invalid entry type: ' + str(entry_in['type']))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Investment statistics calculator'
    )

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: -)')
    parser.add_argument('file_out', metavar='FILE_OUT', type=str,
                        nargs='?', default='-',
                        help='Output file. If set to "-" then stdout is used '
                        '(default: -)')

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

    with ExitStack() as stack:
        file_in = (sys.stdin if args.file_in == '-'
                   else stack.enter_context(open(args.file_in, 'r')))
        file_out = (sys.stdout if args.file_out == '-'
                    else stack.enter_context(open(args.file_out, 'w')))

        data_in = load_data(file_in)
        data_out = compute_stats(data_in)
        save_data(data_out, file_out, args.fmt_days, args.fmt_src, args.fmt_dst,
                  args.fmt_rate, args.fmt_yield)

    return 0
