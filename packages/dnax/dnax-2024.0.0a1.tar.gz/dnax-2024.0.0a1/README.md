<img src="./docs/img/logo.png" width=150/>

# dnax — DNA models in JAX

>[!WARNING]
>This is an experimental implementation.

`dnax` provides JAX-based implementation of models like [BPNet](https://github.com/kundajelab/bpnet), [ChromBPNet](https://github.com/kundajelab/chrombpnet), [DragoNNFruit](https://github.com/jmschrei/dragonnfruit).
The code is heavily based on original implementations ([chrombpnet](https://github.com/kundajelab/chrombpnet), [bpnet-lite](https://github.com/jmschrei/bpnet-lite))
however attempts to be more readable, accessible, and maintainable.

## Installation

```bash
pip install dnax

# or 

pip install git+https://github.com/gtca/dnax.git
```

## Usage

Vanilla ChromBPNet:

```python
from dnax.models.chrombpnet import ChromBPNet

bias = BPNet(n_filters=512, n_layers=8)
accessibility = BPNet(n_filters=512, n_layers=8)

model = ChromBPNet(bias, accessibility)

x = ...  # (batch, 2114, 4) tensor (1-hot)
profile, counts = model(x)
```

For inference, you can load existing ChromBPNet models:

```python
from dnax.io import load_chrombpnet_model

model = load_chrombpnet_model(bias_file, accessibility_file)

profile, counts = model(x)
```

## Implementation

`dnax` currently uses `flax` and its [NNX API](https://flax.readthedocs.io/en/latest/guides/linen_to_nnx.html).

