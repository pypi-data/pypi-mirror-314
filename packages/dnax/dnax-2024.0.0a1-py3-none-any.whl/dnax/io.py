import h5py
import jax
import jax.numpy as jnp
from flax import nnx
from typing import Dict, Any

from .models.bpnet import BPNet
from .models.chrombpnet import ChromBPNet


def load_chrombpnet_weights(filename: str) -> Dict[str, Any]:
    """
    Load weights from the ChromBPNet TensorFlow h5 file format.

    This code is based on the I/O code from the bpnet-lite repository.
    
    Args:
        filename: Path to the h5 file containing model weights
        
    Returns:
        Dictionary containing the model parameters
    """
    h5 = h5py.File(filename, "r")
    w = h5['model_weights']

    if 'bpnet_1conv' in w.keys():
        prefix = ""
    else:
        prefix = "wo_bias_"

    def namer(prefix, suffix):
        return '{0}{1}/{0}{1}'.format(prefix, suffix)

    k, b = 'kernel:0', 'bias:0'

    # Get number of layers
    n_layers = 0
    for layer_name in w.keys():
        try:
            idx = int(layer_name.split("_")[-1].replace("conv", ""))
            n_layers = max(n_layers, idx)
        except ValueError:
            pass

    name = namer(prefix, "bpnet_1conv")
    # n_filters = w[name][k].shape[2]

    params = {
        'initial_conv': {
            'kernel': jnp.transpose(w[namer(prefix, 'bpnet_1st_conv')][k][:], (2, 1, 0)),
            'bias': jnp.array(w[namer(prefix, 'bpnet_1st_conv')][b][:])
        },
        'residual_blocks': {}
    }

    # Load dilated conv layers
    for i in range(1, n_layers+1):
        lname = namer(prefix, f'bpnet_{i}conv')
        params['residual_blocks'][i-1] = {
            'kernel': jnp.transpose(w[lname][k][:], (2, 1, 0)),
            'bias': jnp.array(w[lname][b][:])
        }

    # Load profile head
    prefix = prefix + "bpnet_" if prefix != "" else ""
    fname = namer(prefix, 'prof_out_precrop')
    params['profile_conv'] = {
        'kernel': jnp.transpose(w[fname][k][:], (2, 1, 0)),
        'bias': jnp.array(w[fname][b][:])
    }

    # Load count head
    name = namer(prefix, "logcount_predictions")
    params['count_linear'] = {
        'kernel': jnp.transpose(w[name][k][:], (1, 0)),
        'bias': jnp.array(w[name][b][:])
    }

    return params

def load_chrombpnet_model(bias_model_path: str, 
                          accessibility_model_path: str) -> ChromBPNet:
    """Load a complete ChromBPNet model from saved weights.
    
    Args:
        bias_model_path: Path to bias model weights
        accessibility_model_path: Path to accessibility model weights
        **model_kwargs: Additional arguments to pass to ChromBPNet constructor
        
    Returns:
        Initialized ChromBPNet model with loaded weights
    """
    load_fn = load_chrombpnet_weights
    
    # Load weights
    bias_weights = load_fn(bias_model_path)
    acc_weights = load_fn(accessibility_model_path)

    # Model kwargs
    bias_model_kwargs = {
        'n_features': bias_weights['initial_conv']['bias'].shape[0],
        'n_layers': len(bias_weights['residual_blocks']),
    }
    accessibility_model_kwargs = {
        'n_features': acc_weights['initial_conv']['bias'].shape[0],
        'n_layers': len(acc_weights['residual_blocks']),
    }
    
    # Create models
    bias_model = BPNet(**bias_model_kwargs, rngs=nnx.Rngs(0))
    acc_model = BPNet(**accessibility_model_kwargs, rngs=nnx.Rngs(0))
    
    # Initialize with loaded weights
    bias_state = nnx.State(jax.tree.map(
        lambda x: nnx.VariableState(type=nnx.Param, value=x),
        bias_weights,
    ))
    assert len(bias_state['residual_blocks']) == len(bias_model.residual_blocks)
    nnx.update(bias_model, bias_state)

    acc_state = nnx.State(jax.tree.map(
        lambda x: nnx.VariableState(type=nnx.Param, value=x),
        acc_weights,
    ))
    assert len(acc_state['residual_blocks']) == len(acc_model.residual_blocks)
    nnx.update(acc_model, acc_state)
    
    model = ChromBPNet(bias=bias_model, accessibility=acc_model)
    
    return model
