#!/usr/bin/env python3

import io
import textwrap

import pytest

from copy import deepcopy
from datetime import datetime as dt
from datetime import timezone as tz

from investats_aggr import pair_items_to_dict, load_data, save_data, \
    aggregate_series


def test_pair_items_to_dict():
    assert pair_items_to_dict(['A', 'aaa', 'B', 'bbb']) == \
        {'A': 'aaa', 'B': 'bbb'}
    assert pair_items_to_dict(['A', 'aaa', 'B', 'bbb', 'C', 'ccc']) == \
        {'A': 'aaa', 'B': 'bbb', 'C': 'ccc'}

    with pytest.raises(ValueError) as exc_info:
        pair_items_to_dict(['A', 'aaa', 'B'])
    assert exc_info.value.args == (
        'The length of pair items must be an even number',)

    with pytest.raises(ValueError) as exc_info:
        pair_items_to_dict(['A', 'aaa'])
    assert exc_info.value.args == ('The number of pairs must be >= 2',)


def test_load_data():
    csv = textwrap.dedent('''\
        datetime,field01,field02,field03
        2020-01-01 00:00:00+00:00,0,0,0
        2020-01-12 00:00:00+00:00,11,11,500
        2020-02-12 00:00:00+00:00,31,42,700.123
        2020-03-12 00:00:00+00:00,29,71,250.001
    ''')

    data = list(load_data(io.StringIO(csv)))

    assert data == [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'field01': 0, 'field02': 0, 'field03': 0},
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc),
         'field01': 11, 'field02': 11, 'field03': 500},
        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc),
         'field01': 31, 'field02': 42, 'field03': 700.123},
        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc),
         'field01': 29, 'field02': 71, 'field03': 250.001},
    ]


def test_save_data():
    data = [
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc),
         'diff_days': 0, 'tot_days': 0,

         'diff_src': 1000, 'tot_src': 1000, 'tot_dst_as_src': 1000,
         'chkpt_gain_src': 0, 'chkpt_gain_net_src': 0,
         'tot_gain_src': 0, 'tot_gain_net_src': 0,

         'AAA:diff_src': 500, 'AAA:diff_dst': 5, 'AAA:latest_rate': 100,
         'AAA:tot_src': 500, 'AAA:tot_dst': 5, 'AAA:avg_rate': 100,
         'AAA:tot_dst_as_src': 500,
         'AAA:chkpt_yield': 0, 'AAA:chkpt_apy': 0,
         'AAA:global_yield': 0, 'AAA:global_apy': 0,
         'AAA:latest_cgt': 0,
         'AAA:chkpt_gain_src': 0, 'AAA:chkpt_gain_net_src': 0,
         'AAA:tot_gain_src': 0, 'AAA:tot_gain_net_src': 0,

         'BBB:diff_src': 500, 'BBB:diff_dst': 10, 'BBB:latest_rate': 50,
         'BBB:tot_src': 500, 'BBB:tot_dst': 10, 'BBB:avg_rate': 50,
         'BBB:tot_dst_as_src': 500,
         'BBB:chkpt_yield': 0, 'BBB:chkpt_apy': 0,
         'BBB:global_yield': 0, 'BBB:global_apy': 0,
         'BBB:latest_cgt': 0,
         'BBB:chkpt_gain_src': 0, 'BBB:chkpt_gain_net_src': 0,
         'BBB:tot_gain_src': 0, 'BBB:tot_gain_net_src': 0,

         'chkpt_yield': 0, 'chkpt_apy': 0,
         'global_yield': 0, 'global_apy': 0},

        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc),
         'diff_days': 31, 'tot_days': 31,

         'diff_src': 2100, 'tot_src': 3100, 'tot_dst_as_src': 3150,
         'chkpt_gain_src': 50, 'chkpt_gain_net_src': 32.5,
         'tot_gain_src': 50, 'tot_gain_net_src': 32.5,

         'AAA:diff_src': 700, 'AAA:diff_dst': 10, 'AAA:latest_rate': 70,
         'AAA:tot_src': 1200, 'AAA:tot_dst': 15, 'AAA:avg_rate': 80,
         'AAA:tot_dst_as_src': 1050,
         'AAA:chkpt_yield': -0.30000000000000004, 'AAA:chkpt_apy': -0.9849978210304741,
         'AAA:global_yield': -0.125, 'AAA:global_apy': -0.7924170918049609,
         'AAA:latest_cgt': 0.15,
         'AAA:chkpt_gain_src': -150, 'AAA:chkpt_gain_net_src': -127.5,
         'AAA:tot_gain_src': -150, 'AAA:tot_gain_net_src': -127.5,

         'BBB:diff_src': 1400, 'BBB:diff_dst': 20, 'BBB:latest_rate': 70,
         'BBB:tot_src': 1900, 'BBB:tot_dst': 30, 'BBB:avg_rate': 63.333333333333336,
         'BBB:tot_dst_as_src': 2100,
         'BBB:chkpt_yield': 0.3999999999999999, 'BBB:chkpt_apy': 51.546013724696195,
         'BBB:global_yield': 0.10526315789473673, 'BBB:global_apy': 2.249177905018738,
         'BBB:latest_cgt': 0.20,
         'BBB:chkpt_gain_src': 200, 'BBB:chkpt_gain_net_src': 160,
         'BBB:tot_gain_src': 200, 'BBB:tot_gain_net_src': 160,

         'chkpt_yield': 0.05, 'chkpt_apy': 0.7761797254076475,
         'global_yield': 0.05, 'global_apy': 0.7761797254076475},

        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc),
         'diff_days': 29, 'tot_days': 60,

         'diff_src': 500, 'tot_src': 3600, 'tot_dst_as_src': 10_700,
         'chkpt_gain_src': 7050, 'chkpt_gain_net_src': 5767.5,
         'tot_gain_src': 7100, 'tot_gain_net_src': 5800,

         'AAA:diff_src': 250, 'AAA:diff_dst': 4.25, 'AAA:latest_rate': 200,
         'AAA:tot_src': 1450, 'AAA:tot_dst': 19.25, 'AAA:avg_rate': 75.32467532467533,
         'AAA:tot_dst_as_src': 3850,
         'AAA:chkpt_yield': 1.8571428571428572, 'AAA:chkpt_apy': 547587.0028295065,
         'AAA:global_yield': 1.6551724137931032, 'AAA:global_apy': 379.0996102191754,
         'AAA:latest_cgt': 0.15,
         'AAA:chkpt_gain_src': 2550, 'AAA:chkpt_gain_net_src': 2167.5,
         'AAA:tot_gain_src': 2400, 'AAA:tot_gain_net_src': 2040,

         'BBB:diff_src': 250, 'BBB:diff_dst': 4.25, 'BBB:latest_rate': 200,
         'BBB:tot_src': 2150, 'BBB:tot_dst': 34.25, 'BBB:avg_rate': 62.77372262773723,
         'BBB:tot_dst_as_src': 6850,
         'BBB:chkpt_yield': 1.8571428571428572, 'BBB:chkpt_apy': 547587.0028295065,
         'BBB:global_yield': 2.186046511627907, 'BBB:global_apy': 1150.9943403101925,
         'BBB:latest_cgt': 0.20,
         'BBB:chkpt_gain_src': 4500, 'BBB:chkpt_gain_net_src': 3600,
         'BBB:tot_gain_src': 4700, 'BBB:tot_gain_net_src': 3760,

         'chkpt_yield': 2.238095238095238, 'chkpt_apy': 2646126.1510352483,
         'global_yield': 7.1, 'global_apy': 336214.0873987736},
    ]

    headers_line = (
        'datetime,diff_days,tot_days,'
        'diff_src,tot_src,tot_dst_as_src,'
        'chkpt_gain_src,chkpt_gain_net_src,tot_gain_src,tot_gain_net_src,'
        'AAA:diff_src,AAA:diff_dst,AAA:latest_rate,'
        'AAA:tot_src,AAA:tot_dst,AAA:avg_rate,'
        'AAA:tot_dst_as_src,'
        'AAA:chkpt_yield,AAA:chkpt_apy,AAA:global_yield,AAA:global_apy,'
        'AAA:latest_cgt,'
        'AAA:chkpt_gain_src,AAA:chkpt_gain_net_src,'
        'AAA:tot_gain_src,AAA:tot_gain_net_src,'
        'BBB:diff_src,BBB:diff_dst,BBB:latest_rate,'
        'BBB:tot_src,BBB:tot_dst,BBB:avg_rate,'
        'BBB:tot_dst_as_src,'
        'BBB:chkpt_yield,BBB:chkpt_apy,BBB:global_yield,BBB:global_apy,'
        'BBB:latest_cgt,'
        'BBB:chkpt_gain_src,BBB:chkpt_gain_net_src,'
        'BBB:tot_gain_src,BBB:tot_gain_net_src,'
        'chkpt_yield,chkpt_apy,global_yield,global_apy')

    csv = '\n'.join([
        headers_line,
        '2020-01-12 00:00:00+00:00,0,0,1000,1000,1000,0,0,0,0,500,5,100,500,5,'
        '100,500,0,0,0,0,0,0,0,0,0,500,10,50,500,10,50,500,0,0,0,0,0,0,0,0,0,'
        '0,0,0,0',
        '2020-02-12 00:00:00+00:00,31,31,2100,3100,3150,50,32.5,50,32.5,700,'
        '10,70,1200,15,80,1050,-0.30000000000000004,-0.9849978210304741,'
        '-0.125,-0.7924170918049609,0.15,-150,-127.5,-150,-127.5,1400,20,70,'
        '1900,30,63.333333333333336,2100,0.3999999999999999,'
        '51.546013724696195,0.10526315789473673,2.249177905018738,0.2,200,160,'
        '200,160,0.05,0.7761797254076475,0.05,0.7761797254076475',
        '2020-03-12 00:00:00+00:00,29,60,500,3600,10700,7050,5767.5,7100,5800,'
        '250,4.25,200,1450,19.25,75.32467532467533,3850,1.8571428571428572,'
        '547587.0028295065,1.6551724137931032,379.0996102191754,0.15,2550,'
        '2167.5,2400,2040,250,4.25,200,2150,34.25,62.77372262773723,6850,'
        '1.8571428571428572,547587.0028295065,2.186046511627907,'
        '1150.9943403101925,0.2,4500,3600,4700,3760,2.238095238095238,'
        '2646126.1510352483,7.1,336214.0873987736',
    ]) + '\n'

    buf = io.StringIO()
    save_data(data, buf)
    buf.seek(0)

    assert buf.read() == csv

    csv = '\n'.join([
        headers_line,
        '2020-01-12 00:00:00+00:00,0.00,0.00,1000.000,1000.000,1000.000,0.000,'
        '0.000,0.000,0.000,500.000,5.0000,100.00000,500.000,5.0000,100.00000,'
        '500.000,0.000000,0.000000,0.000000,0.000000,0,0.000,0.000,0.000,'
        '0.000,500.000,10.0000,50.00000,500.000,10.0000,50.00000,500.000,'
        '0.000000,0.000000,0.000000,0.000000,0,0.000,0.000,0.000,0.000,'
        '0.000000,0.000000,0.000000,0.000000',
        '2020-02-12 00:00:00+00:00,31.00,31.00,2100.000,3100.000,3150.000,'
        '50.000,32.500,50.000,32.500,700.000,10.0000,70.00000,1200.000,'
        '15.0000,80.00000,1050.000,-0.300000,-0.984998,-0.125000,-0.792417,'
        '0.15,-150.000,-127.500,-150.000,-127.500,1400.000,20.0000,70.00000,'
        '1900.000,30.0000,63.33333,2100.000,0.400000,51.546014,0.105263,'
        '2.249178,0.2,200.000,160.000,200.000,160.000,0.050000,0.776180,'
        '0.050000,0.776180',
        '2020-03-12 00:00:00+00:00,29.00,60.00,500.000,3600.000,10700.000,'
        '7050.000,5767.500,7100.000,5800.000,250.000,4.2500,200.00000,'
        '1450.000,19.2500,75.32468,3850.000,1.857143,547587.002830,1.655172,'
        '379.099610,0.15,2550.000,2167.500,2400.000,2040.000,250.000,4.2500,'
        '200.00000,2150.000,34.2500,62.77372,6850.000,1.857143,547587.002830,'
        '2.186047,1150.994340,0.2,4500.000,3600.000,4700.000,3760.000,'
        '2.238095,2646126.151035,7.100000,336214.087399',
    ]) + '\n'

    buf = io.StringIO()
    save_data(data, buf, '{:.2f}', '{:.3f}', '{:.4f}', '{:.5f}', '{:.6f}')
    buf.seek(0)

    assert buf.read() == csv

    data_bad = [{'datetime': 12345, 'asdfghjkl': 67890},
                {'datetime': 11223, 'asdfghjkl': 34455},
                {'datetime': 66778, 'asdfghjkl': 89900}]

    buf = io.StringIO()
    with pytest.raises(ValueError) as exc_info:
        save_data(data_bad, buf)
    assert exc_info.value.args == ('Unsupported key: asdfghjkl',)


def test_aggregate_series():
    data_aaa = [
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc),
         'diff_days': 0, 'tot_days': 0,
         'diff_src': 500, 'diff_dst': 5, 'latest_rate': 100,
         'tot_src': 500, 'tot_dst': 5, 'avg_rate': 100,
         'tot_dst_as_src': 500,
         'chkpt_yield': 0, 'chkpt_apy': 0,
         'global_yield': 0, 'global_apy': 0,
         'latest_cgt': 0,
         'chkpt_gain_src': 0, 'chkpt_gain_net_src': 0,
         'tot_gain_src': 0, 'tot_gain_net_src': 0},
        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc),
         'diff_days': 31, 'tot_days': 31,
         'diff_src': 700, 'diff_dst': 10, 'latest_rate': 70,
         'tot_src': 1200, 'tot_dst': 15, 'avg_rate': 80,
         'tot_dst_as_src': 1050,
         'chkpt_yield': -0.30000000000000004, 'chkpt_apy': -0.9849978210304741,
         'global_yield': -0.125, 'global_apy': -0.7924170918049609,
         'latest_cgt': 0.15,
         'chkpt_gain_src': -150, 'chkpt_gain_net_src': -127.5,
         'tot_gain_src': -150, 'tot_gain_net_src': -127.5},
        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc),
         'diff_days': 29, 'tot_days': 60,
         'diff_src': 250, 'diff_dst': 4.25, 'latest_rate': 200,
         'tot_src': 1450, 'tot_dst': 19.25, 'avg_rate': 75.32467532467533,
         'tot_dst_as_src': 3850,
         'chkpt_yield': 1.8571428571428572, 'chkpt_apy': 547587.0028295065,
         'global_yield': 1.6551724137931032, 'global_apy': 379.0996102191754,
         'latest_cgt': 0.15,
         'chkpt_gain_src': 2550, 'chkpt_gain_net_src': 2167.5,
         'tot_gain_src': 2400, 'tot_gain_net_src': 2040},
    ]
    data_bbb = [
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc),
         'diff_days': 0, 'tot_days': 0,
         'diff_src': 500, 'diff_dst': 10, 'latest_rate': 50,
         'tot_src': 500, 'tot_dst': 10, 'avg_rate': 50,
         'tot_dst_as_src': 500,
         'chkpt_yield': 0, 'chkpt_apy': 0,
         'global_yield': 0, 'global_apy': 0,
         'latest_cgt': 0,
         'chkpt_gain_src': 0, 'chkpt_gain_net_src': 0,
         'tot_gain_src': 0, 'tot_gain_net_src': 0},
        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc),
         'diff_days': 31, 'tot_days': 31,
         'diff_src': 1400, 'diff_dst': 20, 'latest_rate': 70,
         'tot_src': 1900, 'tot_dst': 30, 'avg_rate': 63.333333333333336,
         'tot_dst_as_src': 2100,
         'chkpt_yield': 0.3999999999999999, 'chkpt_apy': 51.546013724696195,
         'global_yield': 0.10526315789473673, 'global_apy': 2.249177905018738,
         'latest_cgt': 0.20,
         'chkpt_gain_src': 200, 'chkpt_gain_net_src': 160,
         'tot_gain_src': 200, 'tot_gain_net_src': 160},
        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc),
         'diff_days': 29, 'tot_days': 60,
         'diff_src': 250, 'diff_dst': 4.25, 'latest_rate': 200,
         'tot_src': 2150, 'tot_dst': 34.25, 'avg_rate': 62.77372262773723,
         'tot_dst_as_src': 6850,
         'chkpt_yield': 1.8571428571428572, 'chkpt_apy': 547587.0028295065,
         'global_yield': 2.186046511627907, 'global_apy': 1150.9943403101925,
         'latest_cgt': 0.20,
         'chkpt_gain_src': 4500, 'chkpt_gain_net_src': 3600,
         'tot_gain_src': 4700, 'tot_gain_net_src': 3760},
    ]

    named_series_orig = {'AAA': data_aaa, 'BBB': data_bbb}

    named_series = deepcopy(named_series_orig)
    named_series_copy = deepcopy(named_series)
    data_out = list(aggregate_series(named_series))
    assert named_series == named_series_copy
    assert data_out == [
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc),
         'diff_days': 0, 'tot_days': 0,

         'diff_src': 1000, 'tot_src': 1000, 'tot_dst_as_src': 1000,
         'chkpt_gain_src': 0, 'chkpt_gain_net_src': 0,
         'tot_gain_src': 0, 'tot_gain_net_src': 0,

         'AAA:diff_src': 500, 'AAA:diff_dst': 5, 'AAA:latest_rate': 100,
         'AAA:tot_src': 500, 'AAA:tot_dst': 5, 'AAA:avg_rate': 100,
         'AAA:tot_dst_as_src': 500,
         'AAA:chkpt_yield': 0, 'AAA:chkpt_apy': 0,
         'AAA:global_yield': 0, 'AAA:global_apy': 0,
         'AAA:latest_cgt': 0,
         'AAA:chkpt_gain_src': 0, 'AAA:chkpt_gain_net_src': 0,
         'AAA:tot_gain_src': 0, 'AAA:tot_gain_net_src': 0,

         'BBB:diff_src': 500, 'BBB:diff_dst': 10, 'BBB:latest_rate': 50,
         'BBB:tot_src': 500, 'BBB:tot_dst': 10, 'BBB:avg_rate': 50,
         'BBB:tot_dst_as_src': 500,
         'BBB:chkpt_yield': 0, 'BBB:chkpt_apy': 0,
         'BBB:global_yield': 0, 'BBB:global_apy': 0,
         'BBB:latest_cgt': 0,
         'BBB:chkpt_gain_src': 0, 'BBB:chkpt_gain_net_src': 0,
         'BBB:tot_gain_src': 0, 'BBB:tot_gain_net_src': 0,

         'chkpt_yield': 0, 'chkpt_apy': 0,
         'global_yield': 0, 'global_apy': 0},

        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc),
         'diff_days': 31, 'tot_days': 31,

         'diff_src': 2100, 'tot_src': 3100, 'tot_dst_as_src': 3150,
         'chkpt_gain_src': 50, 'chkpt_gain_net_src': 32.5,
         'tot_gain_src': 50, 'tot_gain_net_src': 32.5,

         'AAA:diff_src': 700, 'AAA:diff_dst': 10, 'AAA:latest_rate': 70,
         'AAA:tot_src': 1200, 'AAA:tot_dst': 15, 'AAA:avg_rate': 80,
         'AAA:tot_dst_as_src': 1050,
         'AAA:chkpt_yield': -0.30000000000000004, 'AAA:chkpt_apy': -0.9849978210304741,
         'AAA:global_yield': -0.125, 'AAA:global_apy': -0.7924170918049609,
         'AAA:latest_cgt': 0.15,
         'AAA:chkpt_gain_src': -150, 'AAA:chkpt_gain_net_src': -127.5,
         'AAA:tot_gain_src': -150, 'AAA:tot_gain_net_src': -127.5,

         'BBB:diff_src': 1400, 'BBB:diff_dst': 20, 'BBB:latest_rate': 70,
         'BBB:tot_src': 1900, 'BBB:tot_dst': 30, 'BBB:avg_rate': 63.333333333333336,
         'BBB:tot_dst_as_src': 2100,
         'BBB:chkpt_yield': 0.3999999999999999, 'BBB:chkpt_apy': 51.546013724696195,
         'BBB:global_yield': 0.10526315789473673, 'BBB:global_apy': 2.249177905018738,
         'BBB:latest_cgt': 0.20,
         'BBB:chkpt_gain_src': 200, 'BBB:chkpt_gain_net_src': 160,
         'BBB:tot_gain_src': 200, 'BBB:tot_gain_net_src': 160,

         'chkpt_yield': 0.05, 'chkpt_apy': 0.7761797254076475,
         'global_yield': 0.016129032258064516, 'global_apy': 0.20730561938737058},

        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc),
         'diff_days': 29, 'tot_days': 60,

         'diff_src': 500, 'tot_src': 3600, 'tot_dst_as_src': 10_700,
         'chkpt_gain_src': 7050, 'chkpt_gain_net_src': 5767.5,
         'tot_gain_src': 7100, 'tot_gain_net_src': 5800,

         'AAA:diff_src': 250, 'AAA:diff_dst': 4.25, 'AAA:latest_rate': 200,
         'AAA:tot_src': 1450, 'AAA:tot_dst': 19.25, 'AAA:avg_rate': 75.32467532467533,
         'AAA:tot_dst_as_src': 3850,
         'AAA:chkpt_yield': 1.8571428571428572, 'AAA:chkpt_apy': 547587.0028295065,
         'AAA:global_yield': 1.6551724137931032, 'AAA:global_apy': 379.0996102191754,
         'AAA:latest_cgt': 0.15,
         'AAA:chkpt_gain_src': 2550, 'AAA:chkpt_gain_net_src': 2167.5,
         'AAA:tot_gain_src': 2400, 'AAA:tot_gain_net_src': 2040,

         'BBB:diff_src': 250, 'BBB:diff_dst': 4.25, 'BBB:latest_rate': 200,
         'BBB:tot_src': 2150, 'BBB:tot_dst': 34.25, 'BBB:avg_rate': 62.77372262773723,
         'BBB:tot_dst_as_src': 6850,
         'BBB:chkpt_yield': 1.8571428571428572, 'BBB:chkpt_apy': 547587.0028295065,
         'BBB:global_yield': 2.186046511627907, 'BBB:global_apy': 1150.9943403101925,
         'BBB:latest_cgt': 0.20,
         'BBB:chkpt_gain_src': 4500, 'BBB:chkpt_gain_net_src': 3600,
         'BBB:tot_gain_src': 4700, 'BBB:tot_gain_net_src': 3760,

         'chkpt_yield': 2.238095238095238, 'chkpt_apy': 2646126.1510352483,
         'global_yield': 1.9722222222222223, 'global_apy': 753.9376784192543},
    ]

    with pytest.raises(ValueError) as exc_info:
        list(aggregate_series({}))
    assert exc_info.value.args == ('The number of series must be >= 2',)

    named_series = deepcopy(named_series_orig)
    del named_series['BBB'][2]
    named_series_copy = deepcopy(named_series)
    with pytest.raises(ValueError) as exc_info:
        list(aggregate_series(named_series))
    assert exc_info.value.args == (
        'Series are not all the same length: 2 != 3',)
    assert named_series == named_series_copy

    named_series = deepcopy(named_series_orig)
    named_series['AAA'][0]['datetime'] = dt(2020, 2, 13, tzinfo=tz.utc)
    named_series_copy = deepcopy(named_series)
    with pytest.raises(ValueError) as exc_info:
        list(aggregate_series(named_series))
    assert exc_info.value.args == (
        'Mismatching checkpoint datetime: '
        '2020-01-12 00:00:00+00:00 != 2020-02-13 00:00:00+00:00',)
    assert named_series == named_series_copy
