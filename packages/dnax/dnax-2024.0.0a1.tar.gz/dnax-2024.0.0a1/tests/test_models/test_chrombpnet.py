import jax
from flax import nnx
import numpy as np
import torch
import pytest

from dnax.models.bpnet import BPNet
from dnax.models.chrombpnet import ChromBPNet
from .torch_bpnet import TorchBPNet
from .torch_chrombpnet import TorchChromBPNet


@pytest.fixture
def model_params():
    return {
        'n_features': 64,
        'n_layers': 8,
        'n_outputs': 1,
        'n_control_tracks': 0,  # No control tracks
        'alpha': 1.0,
        'trimming': (2114 - 1000) // 2,
        'use_profile_output_bias': True,
        'use_count_output_bias': True,
        'use_initial_conv_bias': True,
        'use_dilated_conv_bias': True
    }

@pytest.fixture
def input_data():
    batch_size, n_channels, sequence_length = 6, 4, 2_114
    key = jax.random.PRNGKey(0)
    X = jax.random.normal(key, (batch_size, sequence_length, n_channels))
    return X, None  # No control tracks for ChromBPNet

def test_chrombpnet_jax_vs_torch(model_params, input_data):
    X, X_ctl = input_data
    
    # Initialize JAX models (bias and accessibility)
    jax_bias = BPNet(**model_params, rngs=nnx.Rngs(0))
    jax_acc = BPNet(**model_params, rngs=nnx.Rngs(1))
    
    # Create JAX ChromBPNet model
    jax_model = ChromBPNet(bias=jax_bias, accessibility=jax_acc)
    
    # Initialize PyTorch models (bias and accessibility)
    torch_params = {k: v for k, v in model_params.items() if k in TorchBPNet.__init__.__code__.co_varnames}
    torch_params['n_filters'] = model_params['n_features']
    torch_params['count_output_bias'] = model_params['use_count_output_bias']
    torch_params['profile_output_bias'] = model_params['use_profile_output_bias']
    
    torch_bias = TorchBPNet(**torch_params)
    torch_acc = TorchBPNet(**torch_params)
    
    # Create PyTorch ChromBPNet model
    torch_model = TorchChromBPNet(bias=torch_bias, accessibility=torch_acc, name="test")

    # Apply JAX initialization to PyTorch bias model
    with torch.no_grad():
        torch_bias.linear.weight = torch.nn.Parameter(torch.from_numpy(np.array(jax_bias.count_linear.kernel)).T)
        torch_bias.linear.bias = torch.nn.Parameter(torch.from_numpy(np.array(jax_bias.count_linear.bias)))
        
        conv_mapping = {'fconv': 'profile_conv', 'iconv': 'initial_conv'}
        for torch_name, jax_name in conv_mapping.items():
            getattr(torch_bias, torch_name).weight = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_bias, jax_name).kernel)).permute(2, 1, 0)
            )
            getattr(torch_bias, torch_name).bias = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_bias, jax_name).bias))
            )
        for residual_i in range(model_params['n_layers']):
            torch_bias.rconvs[residual_i].weight = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_bias.residual_blocks[residual_i].kernel)).permute(2, 1, 0)
            )
            torch_bias.rconvs[residual_i].bias = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_bias.residual_blocks[residual_i].bias))
            )

    # Apply JAX initialization to PyTorch accessibility model
    with torch.no_grad():
        torch_acc.linear.weight = torch.nn.Parameter(torch.from_numpy(np.array(jax_acc.count_linear.kernel)).T)
        torch_acc.linear.bias = torch.nn.Parameter(torch.from_numpy(np.array(jax_acc.count_linear.bias)))
        
        for torch_name, jax_name in conv_mapping.items():
            getattr(torch_acc, torch_name).weight = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_acc, jax_name).kernel)).permute(2, 1, 0)
            )
            getattr(torch_acc, torch_name).bias = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_acc, jax_name).bias))
            )
        for residual_i in range(model_params['n_layers']):
            torch_acc.rconvs[residual_i].weight = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_acc.residual_blocks[residual_i].kernel)).permute(2, 1, 0)
            )
            torch_acc.rconvs[residual_i].bias = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_acc.residual_blocks[residual_i].bias))
            )
    
    # Convert inputs to appropriate types
    jax_X = X
    torch_X = torch.from_numpy(np.array(X).transpose(0, 2, 1))  # Transpose for PyTorch
    
    # Get outputs from both models
    jax_y_profile, jax_y_counts = jax_model(jax_X, X_ctl)
    torch_y_profile, torch_y_counts = torch_model(torch_X, X_ctl)
    
    # Convert outputs to numpy for comparison
    jax_y_profile = np.array(jax_y_profile)
    jax_y_counts = np.array(jax_y_counts)
    torch_y_profile = torch_y_profile.detach().numpy()
    torch_y_counts = torch_y_counts.detach().numpy()
    
    # Compare outputs
    rtol, atol = 1e-3, 1e-4
    np.testing.assert_allclose(jax_y_profile, torch_y_profile.transpose(0, 2, 1), rtol=rtol, atol=atol)
    np.testing.assert_allclose(jax_y_counts, torch_y_counts, rtol=rtol, atol=atol)

    # Compare number of parameters
    params = nnx.state(jax_model, nnx.Param)
    jax_num_params = sum(p.size for p in jax.tree.leaves(params))
    torch_num_params = sum(p.numel() for p in torch_model.parameters())
    assert jax_num_params == torch_num_params, "Number of parameters does not match" 
