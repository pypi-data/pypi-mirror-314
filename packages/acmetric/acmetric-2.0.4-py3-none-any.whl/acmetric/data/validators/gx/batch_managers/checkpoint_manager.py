"""This module contains the `CheckpointManager` class."""

from great_expectations.checkpoint import Checkpoint
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult

from acmetric.data.validators.gx.batch_managers.batch_manager import BatchManager
from acmetric.utils.exceptions import ValidationError


class CheckpointManager:
    """Checkpoint manager for the data."""

    def __init__(self, batch_manager: BatchManager) -> None:
        """
        Initialize the checkpoint manager.

        This method initializes the checkpoint manager.

        Parameters
        ----------
        batch_manager: BatchManager
            Batch manager.
        """
        self.batch_manager = batch_manager
        self.checkpoint = self.create_checkpoint()

    def create_checkpoint(self) -> Checkpoint:
        """
        Create a checkpoint.

        This method creates a checkpoint (or updates it if it already exists).
        """
        checkpoint = self.batch_manager.data_context.add_or_update_checkpoint(
            name=f"{self.batch_manager.name}_checkpoint",
            validations=[
                {
                    "batch_request": self.batch_manager.batch_request,
                    "expectation_suite_name": f"{self.batch_manager.name}_suite",
                },
            ],
        )
        return checkpoint

    def run_checkpoint(self) -> CheckpointResult:
        """
        Run a checkpoint.

        This method runs a checkpoint.
        """
        checkpoint_result = self.checkpoint.run()
        return checkpoint_result

    @staticmethod
    def evaluate_checkpoint_result(checkpoint_result: CheckpointResult) -> None:
        """
        Evaluate checkpoint result.

        This method evaluates the result of a checkpoint.
        If the checkpoint fails, it raises a `ValidationError`.

        Parameters
        ----------
        checkpoint_result: CheckpointResult
            Result of the checkpoint.
        """
        if not checkpoint_result["success"]:
            raise ValidationError(checkpoint_result)

    def run_checkpoint_and_evaluate(self) -> None:
        """Run a checkpoint and evaluate its result."""
        checkpoint_result = self.run_checkpoint()
        self.evaluate_checkpoint_result(checkpoint_result)
