"""This is a sample Expectation for validating that a batch schema matches a provided dict."""

from typing import Any, Dict, Optional

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine.execution_engine import ExecutionEngine
from great_expectations.execution_engine.pandas_execution_engine import (
    PandasExecutionEngine,
)
from great_expectations.execution_engine.sparkdf_execution_engine import (
    SparkDFExecutionEngine,
)
from great_expectations.expectations.expectation import BatchExpectation
from great_expectations.expectations.metrics.metric_provider import (
    MetricConfiguration,
    MetricDomainTypes,
    metric_value,
)
from great_expectations.expectations.metrics.table_metric_provider import (
    TableMetricProvider,
)


# This class defines a Metric to support your Expectation.
# For most BatchExpectations, the main business logic for calculation will live in this class.
class BatchSchemaMatchesDict(TableMetricProvider):
    """MetricProvider Class for table.columns.schema"""

    # This is the id string that will be used to reference your Metric.
    metric_name = "table.columns.schema"

    # This method implements the core logic for the PandasExecutionEngine
    @metric_value(engine=PandasExecutionEngine)
    def _pandas(
        cls,
        execution_engine: PandasExecutionEngine,
        metric_domain_kwargs: Dict[str, Any],
        metric_value_kwargs: Dict[str, Any],
        metrics: Dict[str, Any],
        runtime_configuration: dict,
    ) -> Dict[str, str]:
        df, _, _ = execution_engine.get_compute_domain(
            metric_domain_kwargs, domain_type=MetricDomainTypes.TABLE
        )
        types_dict = {
            col_name: str(col_type) for col_name, col_type in dict(df.dtypes).items()
        }
        return types_dict

    # @metric_value(engine=SqlAlchemyExecutionEngine)
    # def _sqlalchemy(
    #         cls,
    #         execution_engine,
    #         metric_domain_kwargs,
    #         metric_value_kwargs,
    #         metrics,
    #         runtime_configuration,
    # ):
    #    raise NotImplementedError

    @metric_value(engine=SparkDFExecutionEngine)
    def _spark(
        cls,
        execution_engine: SparkDFExecutionEngine,
        metric_domain_kwargs: Dict[str, Any],
        metric_value_kwargs: Dict[str, Any],
        metrics: Dict[str, Any],
        runtime_configuration: dict,
    ) -> Dict[str, str]:
        df, _, _ = execution_engine.get_compute_domain(
            metric_domain_kwargs, domain_type=MetricDomainTypes.TABLE
        )
        types_dict = {
            col_name: str(col_type) for col_name, col_type in dict(df.dtypes).items()
        }
        return types_dict

    @classmethod
    def _get_evaluation_dependencies(
        cls,
        metric: MetricConfiguration,
        configuration: Optional[ExpectationConfiguration] = None,
        execution_engine: Optional[ExecutionEngine] = None,
        runtime_configuration: Optional[dict] = None,
    ) -> Dict[str, MetricConfiguration]:
        return {
            "table.columns": MetricConfiguration(
                "table.columns", metric.metric_domain_kwargs
            ),
        }


# This class defines the Expectation itself
# The main business logic for calculation lives here.
class ExpectBatchSchemaToMatchDict(BatchExpectation):
    """Expect the batch schema to match a provided dict."""

    # These examples will be shown in the public gallery.
    # They will also be executed as unit tests for your Expectation.
    examples = [
        {
            "dataset_name": "test_dataset",
            "data": {
                "a": [1, 2, 3],
                "b": [1.0, 2.0, 3.0],
                "c": ["aa", "bb", "cc"],
            },
            "only_for": ["pandas"],
            "tests": [
                {
                    "title": "positive_test",
                    "include_in_gallery": True,
                    "in": {"schema": {"a": "int64", "b": "float64", "c": "object"}},
                    "out": {"success": True},
                    "exact_match_out": False,
                },
                {
                    "title": "negative_test",
                    "include_in_gallery": True,
                    "in": {"schema": {"a": "object", "b": "int64", "c": "float64"}},
                    "out": {"success": False},
                    "exact_match_out": False,
                },
            ],
        },
        {
            "dataset_name": "test_dataset",
            "data": {
                "a": [1, 2, 3],
                "b": [1.0, 2.0, 3.0],
                "c": ["aa", "bb", "cc"],
            },
            "only_for": ["spark"],
            "tests": [
                {
                    "title": "positive_test",
                    "include_in_gallery": True,
                    "in": {"schema": {"a": "bigint", "b": "double", "c": "string"}},
                    "out": {"success": True},
                    "exact_match_out": False,
                },
                {
                    "title": "negative_test",
                    "include_in_gallery": True,
                    "in": {"schema": {"a": "string", "b": "bigint", "c": "double"}},
                    "out": {"success": False},
                    "exact_match_out": False,
                },
            ],
        },
    ]

    # This is a tuple consisting of all Metrics necessary to evaluate the Expectation.
    metric_dependencies = ("table.columns.schema", "table.columns")

    success_keys = ()

    # This dictionary contains default values for any parameters that should have default values.
    default_kwarg_values: Dict[str, Any] = {}

    def validate_configuration(
        self, configuration: Optional[ExpectationConfiguration]
    ) -> None:
        """
        Validate that a configuration has been set, and sets a configuration if it has to be set.

        Ensures that necessary configuration arguments have been provided
        for the validation of the expectation.

        Args:
            configuration (OPTIONAL[ExpectationConfiguration]): \
                An optional Expectation Configuration entry that will
                be used to configure the expectation
        Returns:
            None. Raises InvalidExpectationConfigurationError if the config
            is not validated successfully
        """
        super().validate_configuration(configuration)
        configuration = configuration or self.configuration

        # # Check other things in configuration.kwargs and raise Exceptions if needed
        # try:
        #     assert (
        #         ...
        #     ), "message"
        #     assert (
        #         ...
        #     ), "message"
        # except AssertionError as e:
        #     raise InvalidExpectationConfigurationError(str(e))

    def _validate(
        self,
        configuration: ExpectationConfiguration,
        metrics: Dict,
        runtime_configuration: Optional[dict] = None,
        execution_engine: Optional[ExecutionEngine] = None,
    ) -> Dict[str, Any]:
        table_schema = metrics["table.columns.schema"]
        expected_schema = configuration.kwargs.get("schema", {})
        success = table_schema == expected_schema
        return {
            "success": success,
            "result": {
                "observed_value": table_schema,
                "details": {
                    "expected_schema": expected_schema,
                },
            },
        }

    # This object contains metadata for display in the public Gallery
    library_metadata = {
        "tags": [],  # Tags for this Expectation in the Gallery
        "contributors": [  # Github handles for all contributors to this Expectation.
            "ivan-acmetric",  # Don't forget to add your github handle here!
        ],
    }
