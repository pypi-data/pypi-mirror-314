import jax
from flax import nnx
import numpy as np
import torch
import pytest

from dnax.models.bpnet import BPNet

# Import the TorchBPNet class from wherever it's defined
from .torch_bpnet import TorchBPNet
from .tf_bpnet import TFBPNet

@pytest.fixture
def model_params():
    return {
        'n_features': 64,
        'n_layers': 8,
        'n_outputs': 1,
        'n_control_tracks': 2,
        'alpha': 1.0,
        'trimming': (2114 - 1000) // 2,
        'use_profile_output_bias': True,
        'use_count_output_bias': True,  # Changed from count_output_bias
        'use_initial_conv_bias': True,
        'use_dilated_conv_bias': True
    }

@pytest.fixture
def input_data():
    batch_size, n_channels, sequence_length = 6, 4, 2_114
    n_control_tracks = 2
    key = jax.random.PRNGKey(0)
    X = jax.random.normal(key, (batch_size, sequence_length, n_channels))  # Note the shape change vs PyTorch

    if n_control_tracks == 0:
        return X, None
    
    X_ctl = jax.random.normal(key, (batch_size, sequence_length, n_control_tracks))  # Note the shape change vs PyTorch
    return X, X_ctl

def test_bpnet_jax_vs_torch(model_params, input_data):
    X, X_ctl = input_data
    
    # Initialize JAX model
    jax_model = BPNet(**model_params, rngs=nnx.Rngs(0))
    # rng = jax.random.PRNGKey(0)
    # state = create_train_state(rng, jax_model, X.shape, 'adam', {'learning_rate': 1e-3})
    # variables = jax_model.init(state.params, X, X_ctl)
    # print(jax.tree_util.tree_map(lambda x: x.shape, variables['params']))
    # tabulate_fn = tabulate(jax_model, jax.random.PRNGKey(0))
    
    # Initialize PyTorch model
    torch_params = {k: v for k, v in model_params.items() if k in TorchBPNet.__init__.__code__.co_varnames}
    torch_params['n_filters'] = model_params['n_features']  # Change 'n_features' to 'n_filters'
    torch_params['count_output_bias'] = model_params['use_count_output_bias']
    torch_params['profile_output_bias'] = model_params['use_profile_output_bias']
    torch_model = TorchBPNet(**torch_params)

    # Apply JAX initialization to PyTorch model
    with torch.no_grad():
        # torch_model.linear.weight = torch.nn.Parameter(torch.from_numpy(np.array(variables['params']['count_linear']['kernel'])).T)
        # torch_model.linear.bias = torch.nn.Parameter(torch.from_numpy(np.array(variables['params']['count_linear']['bias'])))
        # conv_mapping = {'fconv': 'profile_conv', 'iconv': 'initial_conv'}
        # for torch_name, jax_name in conv_mapping.items():
        #     getattr(torch_model, torch_name).weight = torch.nn.Parameter(
        #         torch.from_numpy(np.array(variables['params'][jax_name]['kernel'])).permute(2, 1, 0)
        #     )
        #     getattr(torch_model, torch_name).bias = torch.nn.Parameter(
        #         torch.from_numpy(np.array(variables['params'][jax_name]['bias']))
        #     )
        # for residual_i in range(model_params['n_layers']):
        #     torch_model.rconvs[residual_i].weight = torch.nn.Parameter(
        #         torch.from_numpy(np.array(variables['params'][f'residual_blocks_{residual_i}']['layers_0']['kernel'])).permute(2, 1, 0)
        #     )
        #     torch_model.rconvs[residual_i].bias = torch.nn.Parameter(
        #         torch.from_numpy(np.array(variables['params'][f'residual_blocks_{residual_i}']['layers_0']['bias']))
        #     )
        torch_model.linear.weight = torch.nn.Parameter(torch.from_numpy(np.array(jax_model.count_linear.kernel)).T)
        torch_model.linear.bias = torch.nn.Parameter(torch.from_numpy(np.array(jax_model.count_linear.bias)))
        conv_mapping = {'fconv': 'profile_conv', 'iconv': 'initial_conv'}
        for torch_name, jax_name in conv_mapping.items():
            getattr(torch_model, torch_name).weight = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_model, jax_name).kernel)).permute(2, 1, 0)
            )
            getattr(torch_model, torch_name).bias = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_model, jax_name).bias))
            )
        for residual_i in range(model_params['n_layers']):
            torch_model.rconvs[residual_i].weight = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_model.residual_blocks[residual_i].kernel)).permute(2, 1, 0)
            )
            torch_model.rconvs[residual_i].bias = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_model.residual_blocks[residual_i].bias))
            )
    
    # Convert inputs to appropriate types
    jax_X, jax_X_ctl = X, X_ctl
    torch_X = torch.from_numpy(np.array(X).transpose(0, 2, 1))  # Transpose for PyTorch
    if X_ctl is not None:
        torch_X_ctl = torch.from_numpy(np.array(X_ctl).transpose(0, 2, 1))  # Transpose for PyTorch
    else:
        torch_X_ctl = None
    
    # Get outputs from both models
    # jax_y_profile, jax_y_counts = jax.vmap(jax_model.apply, in_axes=(None, 0, 0))({'params': state.params}, jax_X, jax_X_ctl)
    # jax_y_profile, jax_y_counts = jax_model.apply(variables, jax_X, jax_X_ctl)
    jax_y_profile, jax_y_counts = jax_model(jax_X, jax_X_ctl)
    torch_y_profile, torch_y_counts = torch_model(torch_X, torch_X_ctl)
    
    # Convert outputs to numpy for comparison
    jax_y_profile = np.array(jax_y_profile)
    jax_y_counts = np.array(jax_y_counts)
    torch_y_profile = torch_y_profile.detach().numpy()
    torch_y_counts = torch_y_counts.detach().numpy()
    
    # Compare output
    rtol, atol = 1e-3, 1e-4
    np.testing.assert_allclose(jax_y_profile, torch_y_profile.transpose(0, 2, 1), rtol=rtol, atol=atol)
    np.testing.assert_allclose(jax_y_counts, torch_y_counts, rtol=rtol, atol=atol)

    # Compare number of parameters
    params = nnx.state(jax_model, nnx.Param)
    jax_num_params = sum(p.size for p in jax.tree.leaves(params))
    torch_num_params = sum(p.numel() for p in torch_model.parameters())
    assert jax_num_params == torch_num_params, "Number of parameters does not match"


def test_bpnet_jax_vs_torch_vs_tf(model_params, input_data):
    X, _ = input_data
    X_ctl = None
    
    # Initialize JAX model
    params_no_ctl = model_params.copy()
    params_no_ctl['n_control_tracks'] = 0
    jax_model = BPNet(**params_no_ctl, rngs=nnx.Rngs(0))
    
    # Initialize PyTorch model
    torch_params = {k: v for k, v in model_params.items() if k in TorchBPNet.__init__.__code__.co_varnames}
    torch_params['n_filters'] = model_params['n_features']
    torch_params['count_output_bias'] = model_params['use_count_output_bias']
    torch_params['profile_output_bias'] = model_params['use_profile_output_bias']
    torch_model = TorchBPNet(**torch_params)

    # Initialize TensorFlow model
    tf_model_params = {
        'filters': model_params['n_features'],
        'n_dil_layers': model_params['n_layers'],
        'counts_loss_weight': 1.0,  # Adjust as needed
        'inputlen': X.shape[1],
        'outputlen': X.shape[1] - 2 * model_params['trimming'],
        'num_tasks': model_params['n_outputs'],
    }
    tf_args = type('Args', (object,), {'learning_rate': 1e-3})()
    tf_model = TFBPNet(tf_args, tf_model_params)

    # Apply JAX initialization to PyTorch model
    with torch.no_grad():
        torch_model.linear.weight = torch.nn.Parameter(torch.from_numpy(np.array(jax_model.count_linear.kernel)).T)
        torch_model.linear.bias = torch.nn.Parameter(torch.from_numpy(np.array(jax_model.count_linear.bias)))
        conv_mapping = {'fconv': 'profile_conv', 'iconv': 'initial_conv'}
        for torch_name, jax_name in conv_mapping.items():
            getattr(torch_model, torch_name).weight = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_model, jax_name).kernel)).permute(2, 1, 0)
            )
            getattr(torch_model, torch_name).bias = torch.nn.Parameter(
                torch.from_numpy(np.array(getattr(jax_model, jax_name).bias))
            )
        for residual_i in range(model_params['n_layers']):
            torch_model.rconvs[residual_i].weight = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_model.residual_blocks[residual_i].kernel)).permute(2, 1, 0)
            )
            torch_model.rconvs[residual_i].bias = torch.nn.Parameter(
                torch.from_numpy(np.array(jax_model.residual_blocks[residual_i].bias))
            )

    # Apply JAX initialization to TensorFlow model
    tf_model.model.get_layer('bpnet_1st_conv').set_weights([
        np.array(jax_model.initial_conv.kernel),
        np.array(jax_model.initial_conv.bias)
    ])
    for i in range(1, model_params['n_layers'] + 1):
        tf_model.model.get_layer(f'bpnet_{i}conv').set_weights([
            np.array(jax_model.residual_blocks[i-1].kernel),
            np.array(jax_model.residual_blocks[i-1].bias)
        ])
    tf_model.model.get_layer('prof_out_precrop').set_weights([
        np.array(jax_model.profile_conv.kernel),
        np.array(jax_model.profile_conv.bias)
    ])
    tf_model.model.get_layer('logcount_predictions').set_weights([
        np.array(jax_model.count_linear.kernel),
        np.array(jax_model.count_linear.bias)
    ])
    
    # Convert inputs to appropriate types
    jax_X, X_ctl = X, None
    torch_X = torch.from_numpy(np.array(X).transpose(0, 2, 1))
    tf_X = np.array(X)

    # Get outputs from all models
    jax_y_profile, jax_y_counts = jax_model(jax_X, X_ctl)
    torch_y_profile, torch_y_counts = torch_model(torch_X, X_ctl)
    tf_y_profile, tf_y_counts = tf_model.model.predict([tf_X])

    # Convert outputs to numpy for comparison
    jax_y_profile = np.array(jax_y_profile)
    jax_y_counts = np.array(jax_y_counts)
    torch_y_profile = torch_y_profile.detach().numpy()
    torch_y_counts = torch_y_counts.detach().numpy()
    
    # Compare outputs
    rtol, atol = 1e-3, 1e-4
    np.testing.assert_allclose(jax_y_profile, torch_y_profile.transpose(0, 2, 1), rtol=rtol, atol=atol)
    np.testing.assert_allclose(jax_y_counts, torch_y_counts, rtol=rtol, atol=atol)
    np.testing.assert_allclose(jax_y_profile, tf_y_profile[..., None], rtol=rtol, atol=atol)
    np.testing.assert_allclose(jax_y_counts, tf_y_counts, rtol=rtol, atol=atol)

    # Compare number of parameters
    params = nnx.state(jax_model, nnx.Param)
    jax_num_params = sum(p.size for p in jax.tree.leaves(params))
    torch_num_params = sum(p.numel() for p in torch_model.parameters())
    tf_num_params = np.sum([np.prod(v.shape) for v in tf_model.model.trainable_variables])
    assert jax_num_params == torch_num_params == tf_num_params, "Number of parameters does not match"
