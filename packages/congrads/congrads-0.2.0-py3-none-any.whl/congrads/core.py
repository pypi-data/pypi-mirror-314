import logging
from torch import Tensor, float32, no_grad, norm, tensor
from torch.optim import Optimizer
from torch.nn import Module
from torch.utils.data import DataLoader
from time import time

from .metrics import MetricManager
from .constraints import Constraint
from .descriptor import Descriptor


class CongradsCore:

    def __init__(
        self,
        descriptor: Descriptor,
        constraints: list[Constraint],
        loaders: tuple[DataLoader, DataLoader, DataLoader],
        network: Module,
        criterion: callable,
        optimizer: Optimizer,
        metric_manager: MetricManager,
        device,
    ):

        # Init parent class
        super().__init__()

        # Init object variables
        self.descriptor = descriptor
        self.constraints = constraints
        self.train_loader = loaders[0]
        self.valid_loader = loaders[1]
        self.test_loader = loaders[2]
        self.network = network
        self.criterion = criterion
        self.optimizer = optimizer
        self.metric_manager = metric_manager
        self.device = device

        # Perform checks
        if len(self.descriptor.variable_layers) == 0:
            logging.warning(
                "The descriptor object has no variable layers. The constraint guided loss adjustment is therefore not used. Is this the intended behaviour?"
            )

        # Initialize constraint metrics
        metric_manager.register("Loss/train")
        metric_manager.register("Loss/valid")
        metric_manager.register("CSR/train")
        metric_manager.register("CSR/valid")

        for constraint in self.constraints:
            metric_manager.register(f"{constraint.name}/train")
            metric_manager.register(f"{constraint.name}/valid")

    def fit(self, max_epochs: int = 100):
        # Loop over epochs
        for epoch in range(max_epochs):

            # Log start time
            start_time = time()

            # Training
            for batch in self.train_loader:

                # Set model in training mode
                self.network.train()

                # Get input-output pairs from batch
                inputs, outputs = batch

                # Transfer to GPU
                inputs, outputs = inputs.to(self.device), outputs.to(self.device)

                # Log preparation time
                prepare_time = start_time - time()

                # Model computations
                prediction = self.network(inputs)

                # Calculate loss
                loss = self.criterion(prediction["output"], outputs)
                self.metric_manager.accumulate("Loss/train", loss.unsqueeze(0))

                # Adjust loss based on constraints
                combined_loss = self.train_step(prediction, loss)

                # Backpropx
                self.optimizer.zero_grad()
                combined_loss.backward(
                    retain_graph=False, inputs=list(self.network.parameters())
                )
                self.optimizer.step()

            # Validation
            with no_grad():
                for batch in self.valid_loader:

                    # Set model in evaluation mode
                    self.network.eval()

                    # Get input-output pairs from batch
                    inputs, outputs = batch

                    # Transfer to GPU
                    inputs, outputs = inputs.to(self.device), outputs.to(self.device)

                    # Model computations
                    prediction = self.network(inputs)

                    # Calculate loss
                    loss = self.criterion(prediction["output"], outputs)
                    self.metric_manager.accumulate("Loss/valid", loss.unsqueeze(0))

                    # Validate constraints
                    self.valid_step(prediction, loss)

            # TODO with valid loader, checkpoint model with best performance

            # Save metrics
            self.metric_manager.record(epoch)
            self.metric_manager.reset()

            # Log compute and preparation time
            process_time = start_time - time() - prepare_time
            print(
                "Compute efficiency: {:.2f}, epoch: {}/{}:".format(
                    process_time / (process_time + prepare_time), epoch, max_epochs
                )
            )
            start_time = time()

    def train_step(
        self,
        prediction: dict[str, Tensor],
        loss: Tensor,
    ):

        # Init scalar tensor for loss
        total_rescale_loss = tensor(0, dtype=float32, device=self.device)
        loss_grads = {}

        # Precalculate loss gradients for each variable layer
        with no_grad():
            for layer in self.descriptor.variable_layers:
                self.optimizer.zero_grad()
                loss.backward(retain_graph=True, inputs=prediction[layer])
                loss_grads[layer] = prediction[layer].grad

        # For each constraint, TODO split into real and validation only constraints
        for constraint in self.constraints:

            # Check if constraints are satisfied and calculate directions
            with no_grad():
                constraint_checks = constraint.check_constraint(prediction)
                constraint_directions = constraint.calculate_direction(prediction)

            # Only do direction calculations for variable layers affecting constraint
            for layer in constraint.layers & self.descriptor.variable_layers:

                with no_grad():
                    # Multiply direction modifiers with constraint result
                    constraint_result = (
                        constraint_checks.unsqueeze(1).type(float32)
                        * constraint_directions[layer]
                    )

                    # Multiply result with rescale factor of constraint
                    constraint_result *= constraint.rescale_factor

                    # Calculate loss gradient norm
                    norm_loss_grad = norm(loss_grads[layer], dim=1, p=2, keepdim=True)

                # Calculate rescale loss
                rescale_loss = (
                    prediction[layer]
                    * constraint_result
                    * norm_loss_grad.detach().clone()
                ).mean()

                # Store rescale loss for this reference space
                total_rescale_loss += rescale_loss

            # Log constraint satisfaction ratio
            self.metric_manager.accumulate(
                f"{constraint.name}/train",
                (~constraint_checks).type(float32),
            )
            self.metric_manager.accumulate(
                "CSR/train",
                (~constraint_checks).type(float32),
            )

        # Return combined loss
        return loss + total_rescale_loss

    def valid_step(
        self,
        prediction: dict[str, Tensor],
        loss: Tensor,
    ):

        # Compute rescale loss without tracking gradients
        with no_grad():

            # For each constraint in this reference space, calculate directions
            for constraint in self.constraints:

                # Check if constraints are satisfied for
                constraint_checks = constraint.check_constraint(prediction)

                # Log constraint satisfaction ratio
                self.metric_manager.accumulate(
                    f"{constraint.name}/valid",
                    (~constraint_checks).type(float32),
                )
                self.metric_manager.accumulate(
                    "CSR/valid",
                    (~constraint_checks).type(float32),
                )

        # Return loss
        return loss
