#!/usr/bin/env python3

import argparse
import sys

from contextlib import ExitStack
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
from enum import Enum
from typing import TextIO


class Freq(str, Enum):
    '''
    Represents how often an investment is made
    '''
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    def prev(self, d: date) -> date:
        '''
        Calculates the date of the previous investment
        '''
        match self:
            case Freq.DAILY:
                return d - timedelta(days=1)
            case Freq.WEEKLY:
                return d - timedelta(weeks=1)
            case Freq.MONTHLY:
                return d.replace(year=d.year - 1, month=12) if d.month == 1 \
                    else d.replace(month=d.month - 1)
            case Freq.YEARLY:
                return d.replace(year=d.year - 1)

    def next(self, d: date) -> date:
        '''
        Calculates the date of the next investment
        '''
        match self:
            case Freq.DAILY:
                return d + timedelta(days=1)
            case Freq.WEEKLY:
                return d + timedelta(weeks=1)
            case Freq.MONTHLY:
                return d.replace(year=d.year + 1, month=1) if d.month == 12 \
                    else d.replace(month=d.month + 1)
            case Freq.YEARLY:
                return d.replace(year=d.year + 1)


def generate_entries(file: TextIO, date_start: date, inv_src: str,
                     init_rate: float, apy: float, freq: Freq, count: int,
                     cgt: str = '', fmt_rate: str = ''):
    '''
    Generates entries based on some parameters
    '''
    if count < 2:
        raise ValueError('Count must be >= 2')

    zero_cgt = cgt == '' or float(cgt) == 0

    d = date_start
    rate = init_rate
    str_rate = str(rate) if fmt_rate == '' else fmt_rate.format(rate)

    print('---', file=file)
    print('- { datetime: %s, type: invest, inv_src: &inv %s, rate: %s }' %
          (d.strftime('%Y-%m-%d'), inv_src, str_rate), file=file)
    print('- { datetime: %s, type: chkpt%s }' %
          (d.strftime('%Y-%m-%d'), '' if zero_cgt else f', cgt: {cgt}'),
          file=file)

    for _ in range(1, count):
        d = freq.next(d)
        days = (d - date_start).total_seconds() / 60 / 60 / 24
        rate = init_rate * (1 + apy) ** (days / 365)
        str_rate = str(rate) if fmt_rate == '' else fmt_rate.format(rate)

        print('- { datetime: %s, type: invest, inv_src: *inv, rate: %s }' %
              (d.strftime('%Y-%m-%d'), str_rate), file=file)
        print('- { datetime: %s, type: chkpt }' % d.strftime('%Y-%m-%d'),
              file=file)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Generate sample entries based on some parameters'
    )

    parser.add_argument('file_out', metavar='FILE_OUT', type=str,
                        nargs='?', default='-',
                        help='Output file. If set to "-" then stdout is used '
                        '(default: -)')

    parser.add_argument('-d', '--date-start',
                        type=lambda x: dt.strptime(x, '%Y-%m-%d').date(),
                        default=dt.now().date() - timedelta(days=365),
                        help='Start date, in YYYY-MM-DD format '
                        '(default: 365 days ago)')
    parser.add_argument('-s', '--inv-src', type=str, default='1000',
                        help='How much SRC to invest each time '
                        '(default: 1000)')
    parser.add_argument('-r', '--init-rate', type=float, default=100,
                        help='Initial DST/SRC rate value (default: 100)')

    parser.add_argument('-a', '--apy', type=float, default=0,
                        help='APY (over 365 days) of the DST/SRC rate '
                        '(default: 0)')
    parser.add_argument('-f', '--freq', type=lambda x: Freq(x),
                        default=Freq.MONTHLY,
                        help='How often the investment is made '
                        '(default: monthly)')
    parser.add_argument('-c', '--count', type=int, default=12,
                        help='Number of periods (default: 12)')

    parser.add_argument('-t', '--cgt', type=str, default='',
                        help='Capital Gains Tax (default: empty)')

    parser.add_argument('--fmt-rate', type=str, default='',
                        help='If specified, formats the rate values with this '
                        'format string (e.g. "{:.6f}")')

    args = parser.parse_args(argv[1:])

    ############################################################################

    with ExitStack() as stack:
        file_out = (sys.stdout if args.file_out == '-'
                    else stack.enter_context(open(args.file_out, 'w')))

        generate_entries(file_out, args.date_start, args.inv_src,
                         args.init_rate, args.apy, args.freq, args.count,
                         args.cgt, args.fmt_rate)

    return 0
