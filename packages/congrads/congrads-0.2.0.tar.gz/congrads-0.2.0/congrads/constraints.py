from abc import ABC, abstractmethod
from numbers import Number
import random
import string
from typing import Callable, Dict
from torch import (
    Tensor,
    ge,
    gt,
    lt,
    le,
    reshape,
    stack,
    ones,
    tensor,
    zeros_like,
)
import logging
from torch.nn.functional import normalize

from .descriptor import Descriptor


class Constraint(ABC):

    descriptor: Descriptor = None
    device = None

    def __init__(
        self,
        neurons: set[str],
        name: str = None,
        rescale_factor: float = 1.5,
    ) -> None:

        # Init parent class
        super().__init__()

        # Init object variables
        self.neurons = neurons
        self.rescale_factor = rescale_factor

        # Perform checks
        if rescale_factor <= 1:
            logging.warning(
                f"Rescale factor for constraint {name} is <= 1. The network will favor general loss over the constraint-adjusted loss. Is this intended behaviour? Normally, the loss should always be larger than 1."
            )

        # If no constraint_name is set, generate one based on the class name and a random suffix
        if name:
            self.name = name
        else:
            random_suffix = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
            self.name = f"{self.__class__.__name__}_{random_suffix}"
            logging.warning(f"Name for constraint is not set. Using {self.name}.")

        # If rescale factor is not larger than 1, warn user and adjust
        if not rescale_factor > 1:
            self.rescale_factor = abs(rescale_factor) + 1.5
            logging.warning(
                f"Rescale factor for constraint {name} is < 1, adjusted value {rescale_factor} to {self.rescale_factor}."
            )
        else:
            self.rescale_factor = rescale_factor

        # Infer layers from descriptor and neurons
        self.layers = set()
        for neuron in self.neurons:
            if neuron not in self.descriptor.neuron_to_layer.keys():
                raise ValueError(
                    f'The neuron name {neuron} used with constraint {self.name} is not defined in the descriptor. Please add it to the correct layer using descriptor.add("layer", ...).'
                )

            self.layers.add(self.descriptor.neuron_to_layer[neuron])

    # TODO only denormalize if required for efficiency
    def _denormalize(self, input: Tensor, neuron_names: list[str]):
        # Extract min and max for each neuron
        min_values = tensor(
            [self.descriptor.neuron_to_minmax[name][0] for name in neuron_names],
            device=input.device,
        )
        max_values = tensor(
            [self.descriptor.neuron_to_minmax[name][1] for name in neuron_names],
            device=input.device,
        )

        # Apply vectorized denormalization
        return input * (max_values - min_values) + min_values

    @abstractmethod
    def check_constraint(self, prediction: dict[str, Tensor]) -> Tensor:
        raise NotImplementedError

    @abstractmethod
    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        raise NotImplementedError


class ScalarConstraint(Constraint):

    def __init__(
        self,
        neuron_name: str,
        comparator: Callable[[Tensor, Number], Tensor],
        scalar: Number,
        name: str = None,
        rescale_factor: float = 1.5,
    ) -> None:

        # Compose constraint name
        name = f"{neuron_name}_{comparator.__name__}_{str(scalar)}"

        # Init parent class
        super().__init__({neuron_name}, name, rescale_factor)

        # Init variables
        self.comparator = comparator
        self.scalar = scalar

        # Get layer name and feature index from neuron_name
        self.layer = self.descriptor.neuron_to_layer[neuron_name]
        self.index = self.descriptor.neuron_to_index[neuron_name]

        # If comparator function is not supported, raise error
        if comparator not in [ge, le, gt, lt]:
            raise ValueError(
                f"Comparator {str(comparator)} used for constraint {name} is not supported. Only ge, le, gt, lt are allowed."
            )

        # Calculate directions based on constraint operator
        if self.comparator in [lt, le]:
            self.direction = -1
        elif self.comparator in [gt, ge]:
            self.direction = 1

    def check_constraint(self, prediction: dict[str, Tensor]) -> Tensor:

        return ~self.comparator(prediction[self.layer][:, self.index], self.scalar)

    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        # NOTE currently only works for dense layers due to neuron to index translation

        output = {}

        for layer in self.layers:
            output[layer] = zeros_like(prediction[layer][0])

        output[self.layer][self.index] = self.direction

        for layer in self.layers:
            output[layer] = normalize(reshape(output[layer], [1, -1]), dim=1)

        return output


class BinaryConstraint(Constraint):

    def __init__(
        self,
        neuron_name_left: str,
        comparator: Callable[[Tensor, Number], Tensor],
        neuron_name_right: str,
        name: str = None,
        rescale_factor: float = 1.5,
    ) -> None:

        # Compose constraint name
        name = f"{neuron_name_left}_{comparator.__name__}_{neuron_name_right}"

        # Init parent class
        super().__init__(
            {neuron_name_left, neuron_name_right},
            name,
            rescale_factor,
        )

        # Init variables
        self.comparator = comparator

        # Get layer name and feature index from neuron_name
        self.layer_left = self.descriptor.neuron_to_layer[neuron_name_left]
        self.layer_right = self.descriptor.neuron_to_layer[neuron_name_right]
        self.index_left = self.descriptor.neuron_to_index[neuron_name_left]
        self.index_right = self.descriptor.neuron_to_index[neuron_name_right]

        # If comparator function is not supported, raise error
        if comparator not in [ge, le, gt, lt]:
            raise RuntimeError(
                f"Comparator {str(comparator)} used for constraint {name} is not supported. Only ge, le, gt, lt are allowed."
            )

        # Calculate directions based on constraint operator
        if self.comparator in [lt, le]:
            self.direction_left = -1
            self.direction_right = 1
        else:
            self.direction_left = 1
            self.direction_right = -1

    def check_constraint(self, prediction: dict[str, Tensor]) -> Tensor:

        return ~self.comparator(
            prediction[self.layer_left][:, self.index_left],
            prediction[self.layer_right][:, self.index_right],
        )

    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        # NOTE currently only works for dense layers due to neuron to index translation

        output = {}

        for layer in self.layers:
            output[layer] = zeros_like(prediction[layer][0])

        output[self.layer_left][self.index_left] = self.direction_left
        output[self.layer_right][self.index_right] = self.direction_right

        for layer in self.layers:
            output[layer] = normalize(reshape(output[layer], [1, -1]), dim=1)

        return output


class SumConstraint(Constraint):
    def __init__(
        self,
        neuron_names_left: list[str],
        comparator: Callable[[Tensor, Number], Tensor],
        neuron_names_right: list[str],
        weights_left: list[float] = None,
        weights_right: list[float] = None,
        name: str = None,
        rescale_factor: float = 1.5,
    ) -> None:

        # Init parent class
        neuron_names = set(neuron_names_left) | set(neuron_names_right)
        super().__init__(neuron_names, name, rescale_factor)

        # Init variables
        self.comparator = comparator
        self.neuron_names_left = neuron_names_left
        self.neuron_names_right = neuron_names_right

        # If comparator function is not supported, raise error
        if comparator not in [ge, le, gt, lt]:
            raise ValueError(
                f"Comparator {str(comparator)} used for constraint {name} is not supported. Only ge, le, gt, lt are allowed."
            )

        # If feature list dimensions don't match weight list dimensions, raise error
        if weights_left and (len(neuron_names_left) != len(weights_left)):
            raise ValueError(
                "The dimensions of neuron_names_left don't match with the dimensions of weights_left."
            )
        if weights_right and (len(neuron_names_right) != len(weights_right)):
            raise ValueError(
                "The dimensions of neuron_names_right don't match with the dimensions of weights_right."
            )

        # If weights are provided for summation, transform them to Tensors
        if weights_left:
            self.weights_left = tensor(weights_left, device=self.device)
        else:
            self.weights_left = ones(len(neuron_names_left), device=self.device)
        if weights_right:
            self.weights_right = tensor(weights_right, device=self.device)
        else:
            self.weights_right = ones(len(neuron_names_right), device=self.device)

        # Calculate directions based on constraint operator
        if self.comparator in [lt, le]:
            self.direction_left = -1
            self.direction_right = 1
        else:
            self.direction_left = 1
            self.direction_right = -1

    def check_constraint(self, prediction: dict[str, Tensor]) -> Tensor:

        def compute_weighted_sum(neuron_names: list[str], weights: tensor) -> tensor:
            layers = [
                self.descriptor.neuron_to_layer[neuron_name]
                for neuron_name in neuron_names
            ]
            indices = [
                self.descriptor.neuron_to_index[neuron_name]
                for neuron_name in neuron_names
            ]

            # Extract predictions for all neurons and apply weights in bulk
            predictions = stack(
                [prediction[layer][:, index] for layer, index in zip(layers, indices)],
                dim=1,
            )

            # Denormalize if required
            predictions_denorm = self._denormalize(predictions, neuron_names)

            # Calculate weighted sum
            weighted_sum = (predictions_denorm * weights.unsqueeze(0)).sum(dim=1)

            return weighted_sum

        weighted_sum_left = compute_weighted_sum(
            self.neuron_names_left, self.weights_left
        )
        weighted_sum_right = compute_weighted_sum(
            self.neuron_names_right, self.weights_right
        )

        # Apply the comparator and calculate the result
        return ~self.comparator(weighted_sum_left, weighted_sum_right)

    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        # NOTE currently only works for dense layers due to neuron to index translation

        output = {}

        for layer in self.layers:
            output[layer] = zeros_like(prediction[layer][0])

        for neuron_name_left in self.neuron_names_left:
            layer = self.descriptor.neuron_to_layer[neuron_name_left]
            index = self.descriptor.neuron_to_index[neuron_name_left]
            output[layer][index] = self.direction_left

        for neuron_name_right in self.neuron_names_right:
            layer = self.descriptor.neuron_to_layer[neuron_name_right]
            index = self.descriptor.neuron_to_index[neuron_name_right]
            output[layer][index] = self.direction_right

        for layer in self.layers:
            output[layer] = normalize(reshape(output[layer], [1, -1]), dim=1)

        return output


# class MonotonicityConstraint(Constraint):
#     # TODO docstring

#     def __init__(
#         self,
#         neuron_name: str,
#         name: str = None,
#         descriptor: Descriptor = None,
#         rescale_factor: float = 1.5,
#     ) -> None:

#         # Compose constraint name
#         name = f"Monotonicity_{neuron_name}"

#         # Init parent class
#         super().__init__({neuron_name}, name, rescale_factor)

#         # Init variables
#         if descriptor != None:
#             self.descriptor = descriptor
#             self.run_init_descriptor()

#         # Get layer name and feature index from neuron_name
#         self.layer = self.descriptor.neuron_to_layer[neuron_name]
#         self.index = self.descriptor.neuron_to_index[neuron_name]

#     def check_constraint(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
#         # Check if values for column in batch are only increasing
#         result = ~ge(
#             diff(
#                 prediction[self.layer][:, self.index],
#                 prepend=zeros_like(
#                     prediction[self.layer][:, self.index][:1],
#                     device=prediction[self.layer].device,
#                 ),
#             ),
#             0,
#         )

#         return {self.layer: result}

#     def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
#         # TODO implement

#         output = {self.layer: zeros_like(prediction[self.layer][0])}
#         output[self.layer][self.index] = 1

#         return output
