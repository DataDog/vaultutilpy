# Vaultutilpy

Python implementation of [vaultutil](https://github.com/DataDog/vaultutil)

## Usage

```python
import vaultutilpy
password = vaultutilpy.in_cluster_secret("path/to/secret", "key")
```

## Run Tests

```bash
python setup.py test
```
