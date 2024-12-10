
# Airflow TDengine Provider

The Airflow Provider for [TDengine](https://github.com/taosdata/TDengine).

## Usage

Build the package locally, and install it on your Airflow environment.

```shell
pip install dist/apache_airflow_providers_tdengine-0.0.1-py3-none-any.whl
```

Or via PyPI:

```shell
pip install apache-airflow-providers-tdengine
```

Add a connection to Airflow via CLI:

```shell
airflow connections add 'tdengine_default' \
  --conn-uri 'YOUR_CONN_URI_HERE'
```

NOTICE: The client driver `taosc` must be installed since only native connector i.e. `tdengine` is supported now.

### Sample Operator

```python
from sciaiot.airflow.providers.tdengine.operators.tdengine import BaseTDengineOperator
import taos


class CustomTDengineOperator(BaseOperator):
  def __init__(self, *, **kwargs) -> None:
    super().__init__(conn_id=conn_id, database=database, **kwargs)

  def execute(self, context: Context) -> None:
    statement = "SELECT server_status()"
    hook = self.get_hook()
    hook.run(statement=statement)
  
```

## Development

### IDE

Use [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) with VS Code.

### Database

Run the `tests/DDL.sql` in `taos` CLI to setup a test database.

### Code Style

In the root folder of project, run:

```shell
# add -v for verbose output
# add --fix for auto fixing
ruff check 
```

Or with [the Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) installed, run commands for any opening python file.

## Test

In the root folder of project, run:

```shell
pytest
```

## Build

In the root folder of project, run:

```shell
python -m build
```
