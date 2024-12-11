class Descriptor:
    # TODO regenerate documentation

    def __init__(
        self,
    ):

        # Define dictionaries that will translate neuron names to layer and index
        self.neuron_to_layer: dict[str, str] = {}
        self.neuron_to_index: dict[str, int] = {}
        self.neuron_to_minmax: dict[str, tuple[float, float]] = {}

        # Define sets that will hold the layers based on which type
        self.output_layers: set[str] = set()
        self.constant_layers: set[str] = set()
        self.variable_layers: set[str] = set()

    def add(
        self,
        layer_name: str,
        index: int,
        neuron_name: str,
        min: float = 0,
        max: float = 1,
        output: bool = False,
        constant: bool = False,
    ):

        if output:
            self.output_layers.add(layer_name)

        if constant:
            self.constant_layers.add(layer_name)
        else:
            self.variable_layers.add(layer_name)

        self.neuron_to_layer[neuron_name] = layer_name
        self.neuron_to_index[neuron_name] = index

        if min != None and max == None:
            raise ValueError(
                f"The min parameter was set without setting the max parameter. Either set both or set none."
            )

        if max != None and min == None:
            raise ValueError(
                f"The max parameter was set without setting the min parameter. Either set both or set none."
            )

        self.neuron_to_minmax[neuron_name] = (min, max)
