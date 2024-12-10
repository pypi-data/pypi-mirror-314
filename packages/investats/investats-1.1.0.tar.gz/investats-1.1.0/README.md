# investats

[![GitHub main workflow](https://img.shields.io/github/actions/workflow/status/dmotte/investats/main.yml?branch=main&logo=github&label=main&style=flat-square)](https://github.com/dmotte/investats/actions)
[![PyPI](https://img.shields.io/pypi/v/investats?logo=python&style=flat-square)](https://pypi.org/project/investats/)

:snake: **Inve**stment **stat**istic**s** calculator.

## Installation

This utility is available as a Python package on **PyPI**:

```bash
pip3 install investats
```

## Usage

There are some files in the [`example`](example) directory of this repo that can be useful to demonstrate how this tool works, so let's change directory first:

```bash
cd example/
```

We need a Python **virtual environment** ("venv") with some packages to do the demonstration:

```bash
python3 -mvenv venv
venv/bin/python3 -mpip install -r requirements.txt
```

> **Note**: we refer to the **source asset** of the investment with the **generic ticker symbol** `SRC`, and to the **destination asset** with `DST`.

Now we need some **input data** about some investments. You can **generate** dummy data using the `investats_gen` CLI entrypoint. Example commands:

```bash
python3 -minvestats_gen -d2021-01-01 -a.20 -c24 --fmt-rate='{:.4f}' data-AAA.yml
python3 -minvestats_gen -d2021-01-01 -a.30 -c24 --fmt-rate='{:.4f}' data-BBB.yml
```

Or you can **scrape** data from raw text files using the `investats_scrape` CLI entrypoint:

```bash
python3 -minvestats_scrape AAA transactions.txt --pfix-{inv-src=Amount,inv-dst=Shares,rate=Price}: -t0.15
```

Now that we have the data, we can **compute the statistics** about the investments:

```bash
for i in AAA BBB; do
    python3 -minvestats --fmt-{days,src}='{:.2f}' --fmt-{dst,yield}='{:.4f}' \
        --fmt-rate='{:.6f}' "data-$i.yml" "stats-$i.csv"
done
```

> **Note**: each supported **input and output entry field** is described with a comment in the `compute_stats` function code. You can search for the string `# - entry_` in the [`investats/cli.py`](investats/cli.py) file to get an overview.

Then, we can **aggregate** the resulting data (related to multiple investments) into a single CSV file:

```bash
python3 -minvestats_aggr AAA stats-AAA.csv BBB stats-BBB.csv \
    --fmt-{days,src}='{:.2f}' --fmt-{dst,yield}='{:.4f}' --fmt-rate='{:.6f}' \
    > stats.csv
```

And finally display some nice **plots** using the [`plots.py`](example/plots.py) script (which uses the [_Plotly_](https://github.com/plotly/plotly.py) Python library):

```bash
venv/bin/python3 plots.py -srga stats.csv
```

For more details on how to use these commands, you can also refer to their help message (`--help`).

## Development

If you want to contribute to this project, you can install the package in **editable** mode:

```bash
pip3 install -e . --user
```

This will just link the package to the original location, basically meaning any changes to the original package would reflect directly in your environment ([source](https://stackoverflow.com/a/35064498)).

If you want to run the tests, you'll have to install the `pytest` package and then run:

```bash
pytest test
```
