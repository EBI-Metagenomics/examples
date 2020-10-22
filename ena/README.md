# ENA API usage examples

A few examples on how to utilize MGnify API.

## Examples

The examples are stored in the `src` folder. They include jupyter notebooks, R and python scripts.

## Run with miniconda

Download miniconda from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

```bash
wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

chmod +x miniconda.sh

bash miniconda.sh -b -p /path/to/miniconda

export PATH=/path/to/miniconda/bin:$PATH

source /path/to/miniconda/bin/activate

pip install install xmltodict requests pandas
```

## Run in virtualenv

```bash
python3 -m venv /path/to/venv

source /path/to/venv/bin/activate

pip install xmltodict requests pandas
```
