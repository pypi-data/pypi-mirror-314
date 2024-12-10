#!/usr/bin/env python3

import argparse
import sys

from contextlib import ExitStack
from datetime import datetime as dt
from datetime import timedelta
from dateutil import parser as dup
from typing import TextIO


def is_txn_valid(txn: dict) -> bool:
    '''
    Checks whether a transaction is valid or not
    '''
    return all(k in txn for k in ['datetime', 'asset', 'rate']) \
        and ('inv_src' in txn) != ('inv_dst' in txn)


def load_data(file: TextIO, pfix_reset: str, pfix_datetime: str,
              pfix_asset: str, pfix_inv_src: str, pfix_inv_dst: str,
              pfix_rate: str):
    '''
    Scrapes transactions from a raw text file
    '''
    txn = {}

    for line in file:
        line = line.strip()

        if line.startswith(pfix_reset):
            if txn == {}:
                continue
            if not is_txn_valid(txn):
                raise ValueError('Invalid transaction: ' + str(txn))
            yield txn
            txn = {}
        elif line.startswith(pfix_datetime):
            txn['datetime'] = dup.parse(line.removeprefix(pfix_datetime))
        elif line.startswith(pfix_asset):
            txn['asset'] = line.removeprefix(pfix_asset).strip()
        elif line.startswith(pfix_inv_src):
            txn['inv_src'] = line.removeprefix(pfix_inv_src).strip()
        elif line.startswith(pfix_inv_dst):
            txn['inv_dst'] = line.removeprefix(pfix_inv_dst).strip()
        elif line.startswith(pfix_rate):
            txn['rate'] = line.removeprefix(pfix_rate).strip()

    if txn == {}:
        return
    if not is_txn_valid(txn):
        raise ValueError('Invalid transaction: ' + str(txn))
    yield txn


def save_data(data: list[dict], file: TextIO):
    '''
    Saves data into a YAML file
    '''
    print('---', file=file)

    for entry in data:
        print('- { ' + ', '.join([
            f'{k}: {str(v)}' for k, v in entry.items()
        ]) + ' }', file=file)


def txns_to_entries(txns: list[dict], asset: str, cgt: str = ''):
    '''
    Filters transactions related to a specific asset, and converts them to
    investats-compatible entries
    '''
    txns = [txn for txn in txns if txn['asset'] == asset]
    len_txns = len(txns)

    is_first_chkpt = True

    for i, txn in enumerate(txns):
        yield {'datetime': txn['datetime'], 'type': 'invest'} | \
            {k: txn[k] for k in ['inv_src', 'inv_dst', 'rate'] if k in txn}

        next_txn = txns[i + 1] if i < len_txns - 1 else None

        if next_txn is None \
                or txn['datetime'].date() != next_txn['datetime'].date():
            chkpt = {
                'datetime': dt.combine(
                    (txn['datetime']).date() + timedelta(days=1),
                    dt.min.time(), txn['datetime'].tzinfo,
                ),
                'type': 'chkpt',
            }

            if is_first_chkpt:
                if cgt != '':
                    chkpt['cgt'] = cgt
                is_first_chkpt = False

            yield chkpt


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Scrape input data for investats from raw text'
    )

    parser.add_argument('asset', metavar='ASSET', type=str,
                        help='Asset name')

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: -)')
    parser.add_argument('file_out', metavar='FILE_OUT', type=str,
                        nargs='?', default='-',
                        help='Output file. If set to "-" then stdout is used '
                        '(default: -)')

    parser.add_argument('--pfix-reset', type=str, default='#####',
                        help='Prefix of the lines that separate one '
                        'transaction from another (default "#####")')
    parser.add_argument('--pfix-datetime', type=str, default='Datetime:',
                        help='Prefix of the lines that contain a datetime '
                        '(default "Datetime:")')
    parser.add_argument('--pfix-asset', type=str, default='Asset:',
                        help='Prefix of the lines that contain the name of an '
                        'asset (default "Asset:")')
    parser.add_argument('--pfix-inv-src', type=str, default='InvSrc:',
                        help='Prefix of the lines that contain an inv_src '
                        'value (default "InvSrc:")')
    parser.add_argument('--pfix-inv-dst', type=str, default='InvDst:',
                        help='Prefix of the lines that contain an inv_dst '
                        'value (default "InvDst:")')
    parser.add_argument('--pfix-rate', type=str, default='Rate:',
                        help='Prefix of the lines that contain a rate value '
                        '(default "Rate:")')

    parser.add_argument('-t', '--cgt', type=str, default='',
                        help='Capital Gains Tax (default: empty)')

    args = parser.parse_args(argv[1:])

    ############################################################################

    with ExitStack() as stack:
        file_in = (sys.stdin if args.file_in == '-'
                   else stack.enter_context(open(args.file_in, 'r')))
        file_out = (sys.stdout if args.file_out == '-'
                    else stack.enter_context(open(args.file_out, 'w')))

        txns = load_data(file_in, args.pfix_reset, args.pfix_datetime,
                         args.pfix_asset, args.pfix_inv_src, args.pfix_inv_dst,
                         args.pfix_rate)
        entries = txns_to_entries(txns, args.asset, args.cgt)
        save_data(entries, file_out)

    return 0
