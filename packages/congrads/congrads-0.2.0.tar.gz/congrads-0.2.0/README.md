# Congrads

**Congrads** is a Python toolbox that brings **constraint-guided gradient descent** capabilities to your machine learning projects. Built with seamless integration into PyTorch, Congrads empowers you to enhance the training and optimization process by incorporating constraints into your training pipeline.

Whether you're working with simple inequality constraints, combinations of input-output relations, or custom constraint formulations, Congrads provides the tools and flexibility needed to build more robust and generalized models.

> **Note:** The Congrads toolbox is **currently in alpha phase**. Expect significant changes, potential bugs, and incomplete features as we continue to develop and improve the functionality. Feedback is highly appreciated during this phase to help us refine the toolbox and ensure its reliability in later stages.

## Key Features

- **Constraint-Guided Training**: Add constraints to guide the optimization process, ensuring that your model generalizes better by trying to satisfy the constraints.
- **Flexible Constraint Definition**: Define constraints on inputs, outputs, or combinations thereof, using an intuitive and extendable interface. Make use of pre-programmed constraint classes or write your own.
- **Seamless PyTorch Integration**: Use Congrads within your existing PyTorch workflows with minimal setup.
- **Flexible and extendible**: Write your own custom networks, constraints and dataset classes to easily extend the functionality of the toolbox.

## Installation

Currently, the **Congrads** toolbox can only be installed using pip. We will later expand to other package managers such as conda. 

```bash
pip install congrads
```

## Getting Started

### 1. **Prerequisites**

Before you can use **Congrads**, make sure you have the following installed:

- Python 3.6+ (preffered version 3.11)
- **PyTorch** (install with CUDA support for GPU training, refer to [PyTorch's getting started guide](https://pytorch.org/get-started/locally/))
- **NumPy** (install with ```pip install numpy```, or refer to [NumPy's install guide](https://numpy.org/install/).)
- **Pandas** (install with ```pip install pandas```, or refer to [Panda's install guide](https://pandas.pydata.org/docs/getting_started/install.html).)

### 2. **Installation**

Please install **Congrads** via pip:

```bash
pip install congrads
```

### 3. **Basic Usage**

#### 1. Import necessary classes and functions from the toolbox

To start using the toolbox, import the required modules and functions. This includes classes for defining constraints, data processing, network setup, and training utilities.

```python
from congrads.constraints import BinaryConstraint, ScalarConstraint, Constraint
from congrads.core import CongradsCore
from congrads.datasets import BiasCorrection
from congrads.descriptor import Descriptor
from congrads.metrics import MetricManager
from congrads.networks import MLPNetwork
from congrads.utils import preprocess_BiasCorrection, splitDataLoaders

```

#### 2. Set up data and preprocessing

The toolbox works with various datasets, and for this example, we are using the **BiasCorrection** dataset. After loading the dataset, it is preprocessed using a utility function and split into train, validation, and test sets using DataLoader instances.

```python
# Load and preprocess data
data = BiasCorrection("./datasets", preprocess_BiasCorrection)
loaders = splitDataLoaders(
    data, loader_args={"batch_size": 100, "shuffle": True, "num_workers": 6}
)
```

#### 3. Configure the network

The model architecture used here is a Multi-Layer Perceptron (MLP) with 25 input features, 2 output features, and 3 hidden layers, each containing 35 neurons. The network outputs are later mapped to meaningful names using the descriptor.

```python
# Instantiate network and push to correct device
network = MLPNetwork(25, 2, n_hidden_layers=3, hidden_dim=35)
network = network.to(device)
```

#### 4. Instantiate loss and optimizer

Define the loss function and optimizer, which are critical for training the model. In this example, we use the Mean Squared Error (MSE) loss function and the Adam optimizer with a learning rate of 0.001.

```python
# Instantiate loss and optimizer
criterion = MSELoss()
optimizer = Adam(network.parameters(), lr=0.001)
```

#### 5. Set up the descriptor

The descriptor serves as a mapping between network layers and their semantic meanings. For this example, the network's two outputs are named ```Tmax``` (maximum temperature) and ```Tmin``` (minimum temperature), which correspond to specific columns in the dataset.

```python
# Descriptor setup
descriptor = Descriptor()
descriptor.add("output", 0, "Tmax", output=True)
descriptor.add("output", 1, "Tmin", output=True)
```

#### 6. Define constraints on your network

Constraints are rules applied to the network's behavior, ensuring its outputs meet specific criteria. Using the descriptor, constraints can be defined for named outputs. In this case, constraints enforce bounds (e.g., ```0 <= Tmin <= 1```) and relationships (```Tmax > Tmin```) on the outputs.

```python
# Constraints definition
Constraint.descriptor = descriptor
constraints = [
    ScalarConstraint("Tmin", ge, 0),   # Tmin >= 0
    ScalarConstraint("Tmin", le, 1),   # Tmin <= 1
    ScalarConstraint("Tmax", ge, 0),   # Tmax >= 0
    ScalarConstraint("Tmax", le, 1),   # Tmax <= 1
    BinaryConstraint("Tmax", gt, "Tmin"),  # Tmax > Tmin
]
```

#### 7. Set up trainer

Metrics are used to evaluate and track the model's performance during training. A ```MetricManager``` is instantiated with a TensorBoard writer to log metrics and visualize training progress.

```python
# Initialize metrics
writer = SummaryWriter()
metric_manager = MetricManager(writer, device)
```

#### 8. Initialize and configure the core learner

The core of the toolbox is the ```CongradsCore``` class, which integrates the descriptor, constraints, data loaders, network, loss function, optimizer, and metrics to manage the learning process.

```python
# Instantiate core
core = CongradsCore(
    descriptor,
    constraints,
    loaders,
    network,
    criterion,
    optimizer,
    metric_manager,
    device,
)
```

#### 9. Start training

The ```fit``` method of the core class starts the training loop for the specified number of epochs. At the end of training, the TensorBoard writer is closed to finalize the logs.

```python
# Start training
core.fit(max_epochs=150)

# Close writer
writer.close()
```

## Example Use Cases

- **Optimization with Domain Knowledge**: Ensure outputs meet real-world restrictions or safety standards.
- **Physics-Informed Neural Networks (PINNs)**: Enforce physical laws as constraints in your models.
- **Improve Training Process**: Inject domain knowledge in the training stage, increasing learning efficiency.

## Roadmap

- [ ] Documentation and Notebook examples
- [ ] Add support for constraint parser that can interpret equations
- [x] Add better handling of metric logging and visualization
- [x] Revise if Pytorch Lightning is preferable over plain Pytorch
- [ ] Determine if it is feasible to add unit and or functional tests

## Contributing

We welcome contributions to Congrads! Whether you want to report issues, suggest features, or contribute code via issues and pull requests.

## License

Congrads is licensed under the [The 3-Clause BSD License](LICENSE). We encourage companies that are interested in a collaboration for a specific topic to contact the authors for more information or to set up joint research projects.

---

Elevate your neural networks with Congrads! 🚀
