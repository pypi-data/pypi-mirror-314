from __future__ import annotations

import jax
import jax.numpy as jnp
from flax.training import train_state
import optax
from typing import Any, Callable, Tuple, Optional, Dict

from ..losses import bpnet_loss

def create_optimizer(name: str, **kwargs) -> optax.GradientTransformation:
    """Create an optimizer based on the given name and parameters."""
    if hasattr(optax, name):
        optimizer_fn = getattr(optax, name)
        return optimizer_fn(**kwargs)
    else:
        raise ValueError(f"Unsupported optimizer: {name}. Please ensure it's available in optax.")

def create_train_state(rng, model, input_shape, optimizer_name: str, optimizer_kwargs: Dict[str, Any]):
    """Create initial training state with customizable optimizer."""
    params = model.init(rng, jnp.ones(input_shape), jnp.ones(input_shape))['params']
    tx = create_optimizer(optimizer_name, **optimizer_kwargs)
    return train_state.TrainState.create(apply_fn=model.apply, params=params, tx=tx)

@jax.jit
def train_step(state: train_state.TrainState, 
               batch: Dict[str, jnp.ndarray],
               loss_fn: Callable) -> Tuple[train_state.TrainState, Dict[str, Any]]:
    """Perform a single training step."""
    def loss_fn_wrapper(params):
        y_profile, y_counts = state.apply_fn({'params': params}, batch['X'], batch.get('x_ctl'))
        y_profile = jax.nn.log_softmax(y_profile, axis=-1)
        y_counts = jax.nn.logsumexp(jnp.expand_dims(y_counts, axis=0), axis=0)
        loss, (profile_loss, count_loss) = loss_fn(y_profile, y_counts, 
                                                   batch['y_profile'], batch['y_counts'], 
                                                   state.params['alpha'])
        return loss, (profile_loss, count_loss)

    (loss, (profile_loss, count_loss)), grads = jax.value_and_grad(loss_fn_wrapper, has_aux=True)(state.params)
    state = state.apply_gradients(grads=grads)
    
    metrics = {
        'loss': loss,
        'profile_loss': profile_loss,
        'count_loss': count_loss
    }
    
    return state, metrics

@jax.jit
def eval_step(state: train_state.TrainState, 
              batch: Dict[str, jnp.ndarray],
              loss_fn: Callable) -> Dict[str, Any]:
    """Perform a single evaluation step."""
    y_profile, y_counts = state.apply_fn({'params': state.params}, batch['X'], batch.get('x_ctl'))
    y_profile = jax.nn.log_softmax(y_profile, axis=-1)
    y_counts = jax.nn.logsumexp(jnp.expand_dims(y_counts, axis=0), axis=0)
    loss, (profile_loss, count_loss) = loss_fn(y_profile, y_counts, 
                                               batch['y_profile'], batch['y_counts'], 
                                               state.params['alpha'])
    
    metrics = {
        'loss': loss,
        'profile_loss': profile_loss,
        'count_loss': count_loss
    }
    
    return metrics

def train_epoch(state: train_state.TrainState, 
                train_loader: Any, 
                loss_fn: Callable) -> Tuple[train_state.TrainState, Dict[str, float]]:
    """Train for a single epoch."""
    batch_metrics = []
    for batch in train_loader:
        state, metrics = train_step(state, batch, loss_fn)
        batch_metrics.append(metrics)
    
    # Compute mean of metrics across each batch in epoch.
    epoch_metrics = {
        k: jnp.mean([metrics[k] for metrics in batch_metrics])
        for k in batch_metrics[0]
    }
    return state, epoch_metrics

def eval_model(state: train_state.TrainState, 
               test_loader: Any, 
               loss_fn: Callable) -> Dict[str, float]:
    """Evaluate the model on the test set."""
    batch_metrics = []
    for batch in test_loader:
        metrics = eval_step(state, batch, loss_fn)
        batch_metrics.append(metrics)
    
    # Compute mean of metrics across each batch in epoch.
    epoch_metrics = {
        k: jnp.mean([metrics[k] for metrics in batch_metrics])
        for k in batch_metrics[0]
    }
    return epoch_metrics

def train_model(model, 
                train_loader: Any, 
                test_loader: Any, 
                num_epochs: int, 
                input_shape: Tuple[int, ...],
                optimizer_name: str = 'adam',
                optimizer_kwargs: Optional[Dict[str, Any]] = None,
                seed: int = 0) -> train_state.TrainState:
    """Train the model with customizable optimizer."""
    rng = jax.random.PRNGKey(seed)
    rng, init_rng = jax.random.split(rng)
    
    optimizer_kwargs = optimizer_kwargs or {'learning_rate': 1e-3}
    state = create_train_state(init_rng, model, input_shape, optimizer_name, optimizer_kwargs)
    
    for epoch in range(num_epochs):
        state, train_metrics = train_epoch(state, train_loader, bpnet_loss)
        test_metrics = eval_model(state, test_loader, bpnet_loss)
        
        print(f"Epoch {epoch+1}")
        print(f"Train metrics: {train_metrics}")
        print(f"Test metrics: {test_metrics}")
    
    return state
