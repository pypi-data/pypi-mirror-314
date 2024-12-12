"""Spark session fixture."""

from pyspark.sql import SparkSession
from pytest import fixture


@fixture(scope="session")
def spark() -> SparkSession:
    """Spark session fixture."""
    return SparkSession.builder.getOrCreate()
