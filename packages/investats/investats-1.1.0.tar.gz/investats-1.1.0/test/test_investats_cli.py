#!/usr/bin/env python3

import io
import textwrap

import pytest

from datetime import datetime as dt
from datetime import timezone as tz

from investats import load_data, save_data, complete_invest_entry, compute_stats


def test_load_data():
    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-12, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12, type: invest, inv_src: *inv, rate: 100.6558 }
        - { datetime: 2020-02-12 01:23:45, type: chkpt }
    ''')

    data = load_data(io.StringIO(yml))

    assert data == [
        {'datetime': dt(2020, 1, 12).astimezone(), 'type': 'invest',
         'inv_src': 500, 'rate': 100},
        {'datetime': dt(2020, 1, 12).astimezone(), 'type': 'chkpt',
         'cgt': 0.15},
        {'datetime': dt(2020, 2, 12).astimezone(), 'type': 'invest',
         'inv_src': 500, 'rate': 100.6558},
        {'datetime': dt(2020, 2, 12, 1, 23, 45).astimezone(), 'type': 'chkpt'},
    ]

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12, type: invest, inv_src: 500, rate: 100 }
        - { datetime: 2020-02-12 01:23:45, type: chkpt }
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(yml))
    assert exc_info.value.args == ('The first entry must be of type "invest"',)

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-12, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12, type: foo, inv_src: *inv, rate: 100.6558 }
        - { datetime: 2020-02-12 01:23:45, type: chkpt }
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(yml))
    assert exc_info.value.args == ('Invalid entry type: foo',)

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: foo, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12, type: invest, inv_src: *inv, rate: 100.6558 }
        - { datetime: 2020-02-12 01:23:45, type: chkpt }
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(yml))
    assert exc_info.value.args == ('Invalid datetime type: foo',)

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-12, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12, type: invest, inv_src: *inv, rate: 100.6558, inv_dst: 1234 }
        - { datetime: 2020-02-12 01:23:45, type: chkpt }
    ''')

    with pytest.raises(ValueError, match=r'Invalid entry {.+}: exactly two '
                       r'values among "inv_src", "inv_dst" and "rate" must be '
                       r'provided for each entry of type "invest"'):
        load_data(io.StringIO(yml))

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-12, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12, type: invest, inv_src: *inv }
        - { datetime: 2020-02-12 01:23:45, type: chkpt }
    ''')

    with pytest.raises(ValueError, match=r'Invalid entry {.+}: exactly two '
                       r'values among "inv_src", "inv_dst" and "rate" must be '
                       r'provided for each entry of type "invest"'):
        load_data(io.StringIO(yml))

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12 00:00:00+00:00, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-11 00:00:00+00:00, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-12 00:00:00+00:00, type: invest, inv_src: *inv, rate: 100.6558 }
        - { datetime: 2020-02-12 01:23:45+00:00, type: chkpt }
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(yml))
    assert exc_info.value.args == (
        'Invalid entry order: 2020-01-12 00:00:00+00:00 > '
        '2020-01-11 00:00:00+00:00',)

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-12 00:00:00+00:00, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-12 00:00:00+00:00, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-01-12 00:00:00+00:00, type: invest, inv_src: *inv, rate: 100.6558 }
        - { datetime: 2020-02-12 01:23:45+00:00, type: chkpt }
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(yml))
    assert exc_info.value.args == (
        'Invalid entry order: 2020-01-12 00:00:00+00:00 >= '
        '2020-01-12 00:00:00+00:00',)


def test_save_data():
    data = [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'diff_days': 0, 'tot_days': 0,
         'diff_src': 0, 'diff_dst': 0, 'latest_rate': 0,
         'tot_src': 0, 'tot_dst': 0, 'avg_rate': 0,
         'tot_dst_as_src': 0,
         'chkpt_yield': 0, 'chkpt_apy': 0,
         'global_yield': 0, 'global_apy': 0,
         'latest_cgt': 0,
         'chkpt_gain_src': 0, 'chkpt_gain_net_src': 0,
         'tot_gain_src': 0, 'tot_gain_net_src': 0},
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc),
         'diff_days': 11, 'tot_days': 11,
         'diff_src': 500, 'diff_dst': 5, 'latest_rate': 100,
         'tot_src': 500, 'tot_dst': 5, 'avg_rate': 100,
         'tot_dst_as_src': 500,
         'chkpt_yield': 0, 'chkpt_apy': 0,
         'global_yield': 0, 'global_apy': 0,
         'latest_cgt': 0.15,
         'chkpt_gain_src': 0, 'chkpt_gain_net_src': 0,
         'tot_gain_src': 0, 'tot_gain_net_src': 0},
        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc),
         'diff_days': 31, 'tot_days': 42,
         'diff_src': 700, 'diff_dst': 10, 'latest_rate': 70,
         'tot_src': 1200, 'tot_dst': 15, 'avg_rate': 80,
         'tot_dst_as_src': 1050,
         'chkpt_yield': -0.30000000000000004, 'chkpt_apy': -0.9849978210304741,
         'global_yield': -0.125, 'global_apy': -0.6866552911749941,
         'latest_cgt': 0.15,
         'chkpt_gain_src': -150, 'chkpt_gain_net_src': -127.5,
         'tot_gain_src': -150, 'tot_gain_net_src': -127.5},
        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc),
         'diff_days': 29, 'tot_days': 71,
         'diff_src': 250, 'diff_dst': 4.25, 'latest_rate': 200,
         'tot_src': 1450, 'tot_dst': 19.25, 'avg_rate': 75.32467532467533,
         'tot_dst_as_src': 3850,
         'chkpt_yield': 1.8571428571428572, 'chkpt_apy': 547587.0028295065,
         'global_yield': 1.6551724137931032, 'global_apy': 150.42410185614494,
         'latest_cgt': 0.15,
         'chkpt_gain_src': 2550, 'chkpt_gain_net_src': 2167.5,
         'tot_gain_src': 2400, 'tot_gain_net_src': 2040},
    ]

    headers_line = (
        'datetime,diff_days,tot_days,diff_src,diff_dst,latest_rate,tot_src,'
        'tot_dst,avg_rate,tot_dst_as_src,chkpt_yield,chkpt_apy,global_yield,'
        'global_apy,latest_cgt,chkpt_gain_src,chkpt_gain_net_src,tot_gain_src,'
        'tot_gain_net_src')

    csv = '\n'.join([
        headers_line,
        '2020-01-01 00:00:00+00:00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0',
        '2020-01-12 00:00:00+00:00,11,11,500,5,100,500,5,100,500,0,0,0,0,0.15,'
        '0,0,0,0',
        '2020-02-12 00:00:00+00:00,31,42,700,10,70,1200,15,80,1050,'
        '-0.30000000000000004,-0.9849978210304741,-0.125,-0.6866552911749941,'
        '0.15,-150,-127.5,-150,-127.5',
        '2020-03-12 00:00:00+00:00,29,71,250,4.25,200,1450,19.25,'
        '75.32467532467533,3850,1.8571428571428572,547587.0028295065,'
        '1.6551724137931032,150.42410185614494,0.15,2550,2167.5,2400,2040',
    ]) + '\n'

    buf = io.StringIO()
    save_data(data, buf)
    buf.seek(0)

    assert buf.read() == csv

    csv = '\n'.join([
        headers_line,
        '2020-01-01 00:00:00+00:00,0.00,0.00,0.000,0.0000,0.00000,0.000,'
        '0.0000,0.00000,0.000,0.000000,0.000000,0.000000,0.000000,0,0.000,'
        '0.000,0.000,0.000',
        '2020-01-12 00:00:00+00:00,11.00,11.00,500.000,5.0000,100.00000,'
        '500.000,5.0000,100.00000,500.000,0.000000,0.000000,0.000000,'
        '0.000000,0.15,0.000,0.000,0.000,0.000',
        '2020-02-12 00:00:00+00:00,31.00,42.00,700.000,10.0000,70.00000,'
        '1200.000,15.0000,80.00000,1050.000,-0.300000,-0.984998,-0.125000,'
        '-0.686655,0.15,-150.000,-127.500,-150.000,-127.500',
        '2020-03-12 00:00:00+00:00,29.00,71.00,250.000,4.2500,200.00000,'
        '1450.000,19.2500,75.32468,3850.000,1.857143,547587.002830,1.655172,'
        '150.424102,0.15,2550.000,2167.500,2400.000,2040.000',
    ]) + '\n'

    buf = io.StringIO()
    save_data(data, buf, '{:.2f}', '{:.3f}', '{:.4f}', '{:.5f}', '{:.6f}')
    buf.seek(0)

    assert buf.read() == csv


def test_complete_invest_entry():
    assert complete_invest_entry({'inv_dst': 100, 'rate': 3}) == \
        {'inv_src': 300, 'inv_dst': 100, 'rate': 3}
    assert complete_invest_entry({'inv_src': 100, 'rate': 8}) == \
        {'inv_src': 100, 'inv_dst': 12.5, 'rate': 8}
    assert complete_invest_entry({'inv_src': 100, 'inv_dst': 20}) == \
        {'inv_src': 100, 'inv_dst': 20, 'rate': 5}

    assert complete_invest_entry({'inv_dst': 0, 'rate': 3}) == \
        {'inv_src': 0, 'inv_dst': 0, 'rate': 3}
    assert complete_invest_entry({'inv_dst': 100, 'rate': 0}) == \
        {'inv_src': 0, 'inv_dst': 100, 'rate': 0}

    assert complete_invest_entry({'inv_src': 0, 'rate': 8}) == \
        {'inv_src': 0, 'inv_dst': 0, 'rate': 8}
    assert complete_invest_entry({'inv_src': 100, 'rate': 0}) == \
        {'inv_src': 100, 'inv_dst': 0, 'rate': 0}

    assert complete_invest_entry({'inv_src': 0, 'inv_dst': 20}) == \
        {'inv_src': 0, 'inv_dst': 20, 'rate': 0}
    assert complete_invest_entry({'inv_src': 100, 'inv_dst': 0}) == \
        {'inv_src': 100, 'inv_dst': 0, 'rate': 0}

    with pytest.raises(KeyError) as exc_info:
        complete_invest_entry({'inv_src': 0})
    assert exc_info.value.args == ('rate',)

    with pytest.raises(KeyError) as exc_info:
        complete_invest_entry({'inv_dst': 0})
    assert exc_info.value.args == ('rate',)

    with pytest.raises(KeyError) as exc_info:
        complete_invest_entry({'rate': 0})
    assert exc_info.value.args == ('inv_dst',)


def test_compute_stats():
    data_in_orig = [
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc), 'type': 'invest',
         'inv_src': 500, 'rate': 100},
        {'datetime': dt(2020, 1, 12, tzinfo=tz.utc), 'type': 'chkpt',
         'notes': 'First checkpoint'},

        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc), 'type': 'invest',
         'inv_src': 700, 'rate': 70},
        {'datetime': dt(2020, 2, 12, tzinfo=tz.utc), 'type': 'chkpt',
         'cgt': 0.15},

        {'datetime': dt(2020, 3, 10, tzinfo=tz.utc), 'type': 'invest',
         'inv_src': 200, 'rate': 50, 'notes': 'Some notes here'},
        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc), 'type': 'invest',
         'inv_src': 50, 'rate': 200},
        {'datetime': dt(2020, 3, 12, tzinfo=tz.utc), 'type': 'chkpt'},
    ]

    data_out_expected = [
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

    data_in = [x.copy() for x in data_in_orig]
    data_in_copy = [x.copy() for x in data_in]
    data_out = list(compute_stats(data_in))
    assert data_in == data_in_copy
    assert data_out == data_out_expected

    data_in = [x.copy() for x in data_in_orig]
    data_in[0]['datetime'] = dt(2020, 1, 1, tzinfo=tz.utc)
    data_in_copy = [x.copy() for x in data_in]
    data_out = list(compute_stats(data_in))
    assert data_in == data_in_copy
    assert data_out == data_out_expected
