"""Module providing a function printing provider version."""
__version__ = "0.0.1"


def get_provider_info():
    """Function to get provider information."""
    return {
        "package-name": "airflow-providers-tdengine",
        "name": "Airflow TDengine Provider",
        "description": "A provider of Apache Airflow for TDengine.",
        "versions": [__version__],
        "connection-types": [
            {
                "connection-type": "tdengine",
                "hook-class-name": "sciaiot.airflow.providers.tdengine.hooks.tdengine.TDengineHook"
            }
        ],
    }
