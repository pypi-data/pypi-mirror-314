import os

version = os.environ.get("MLFLOW_OIDC_AUTH_VERSION", "3.0.0.dev0")

__version__ = version
