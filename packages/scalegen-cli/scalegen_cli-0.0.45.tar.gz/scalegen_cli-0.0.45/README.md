# cli


## Install
```shell
export PRODUCT_TYPE="scalegen"
python make_toml.py
pip3 install -e .
```

## Usage
```shell
scalegen login -ki <key-id> -ks <key-secret>
scalegen --help
```

## Developer Notes
- Set the `ST_PLATFORM_API` environment variable before using/test the cli.
- Run `black .` before submitting commits
