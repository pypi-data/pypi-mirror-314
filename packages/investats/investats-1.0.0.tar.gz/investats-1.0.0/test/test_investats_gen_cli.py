#!/usr/bin/env python3

import io
import textwrap

import pytest

from datetime import date

from investats_gen import Freq, generate_entries


def test_freq():
    assert Freq('weekly') == Freq.WEEKLY

    with pytest.raises(ValueError) as exc_info:
        Freq('foo')
    assert exc_info.value.args == ('\'foo\' is not a valid Freq',)

    d = date(2020, 1, 1)

    assert Freq.DAILY.prev(d) == date(2019, 12, 31)
    assert Freq.WEEKLY.prev(d) == date(2019, 12, 25)
    assert Freq.MONTHLY.prev(d) == date(2019, 12, 1)
    assert Freq.YEARLY.prev(d) == date(2019, 1, 1)

    assert Freq.DAILY.next(d) == date(2020, 1, 2)
    assert Freq.WEEKLY.next(d) == date(2020, 1, 8)
    assert Freq.MONTHLY.next(d) == date(2020, 2, 1)
    assert Freq.YEARLY.next(d) == date(2021, 1, 1)

    d = date(2020, 12, 7)

    assert Freq.DAILY.prev(d) == date(2020, 12, 6)
    assert Freq.WEEKLY.prev(d) == date(2020, 11, 30)
    assert Freq.MONTHLY.prev(d) == date(2020, 11, 7)
    assert Freq.YEARLY.prev(d) == date(2019, 12, 7)

    assert Freq.DAILY.next(d) == date(2020, 12, 8)
    assert Freq.WEEKLY.next(d) == date(2020, 12, 14)
    assert Freq.MONTHLY.next(d) == date(2021, 1, 7)
    assert Freq.YEARLY.next(d) == date(2021, 12, 7)


def test_generate_entries():
    with pytest.raises(ValueError) as exc_info:
        generate_entries(io.StringIO(), date(2020, 1, 1), '500', 100, 0.08,
                         Freq.MONTHLY, 1, '0.15', '{:.4f}')
    assert exc_info.value.args == ('Count must be >= 2',)

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2020-01-01, type: invest, inv_src: &inv 500, rate: 100.0000 }
        - { datetime: 2020-01-01, type: chkpt, cgt: 0.15 }
        - { datetime: 2020-02-01, type: invest, inv_src: *inv, rate: 100.6558 }
        - { datetime: 2020-02-01, type: chkpt }
        - { datetime: 2020-03-01, type: invest, inv_src: *inv, rate: 101.2731 }
        - { datetime: 2020-03-01, type: chkpt }
        - { datetime: 2020-04-01, type: invest, inv_src: *inv, rate: 101.9373 }
        - { datetime: 2020-04-01, type: chkpt }
        - { datetime: 2020-05-01, type: invest, inv_src: *inv, rate: 102.5841 }
        - { datetime: 2020-05-01, type: chkpt }
    ''')

    buf = io.StringIO()
    generate_entries(buf, date(2020, 1, 1), '500', 100, 0.08, Freq.MONTHLY, 5,
                     '0.15', '{:.4f}')
    buf.seek(0)

    assert buf.read() == yml

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2021-01-01, type: invest, inv_src: &inv 500, rate: 100 }
        - { datetime: 2021-01-01, type: chkpt }
        - { datetime: 2022-01-01, type: invest, inv_src: *inv, rate: 108.0 }
        - { datetime: 2022-01-01, type: chkpt }
    ''')

    buf = io.StringIO()
    generate_entries(buf, date(2021, 1, 1), '500', 100, 0.08, Freq.YEARLY, 2)
    buf.seek(0)

    assert buf.read() == yml

    yml = textwrap.dedent('''\
        ---
        - { datetime: 2021-01-01, type: invest, inv_src: &inv 500, rate: 100 }
        - { datetime: 2021-01-01, type: chkpt }
        - { datetime: 2022-01-01, type: invest, inv_src: *inv, rate: 108.0 }
        - { datetime: 2022-01-01, type: chkpt }
    ''')

    for cgt in ['', '0', '000', '0.0', '0.00', '0.0000', '0000.0000', '-0',
                '-0.0', '-00.00']:
        buf = io.StringIO()
        generate_entries(buf, date(2021, 1, 1), '500', 100, 0.08,
                         Freq.YEARLY, 2, cgt)
        buf.seek(0)

        assert buf.read() == yml
