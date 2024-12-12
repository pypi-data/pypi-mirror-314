from jax import jit
import jax.numpy as jnp
from jax.scipy.special import gammaln

@jit
def mnll_loss(logps, true_counts):
    """A loss function based on the multinomial negative log-likelihood.

    This loss function takes in a tensor of normalized log probabilities such
    that the sum of each row is equal to 1 (e.g. from a log softmax) and
    an equal sized tensor of true counts and returns the probability of
    observing the true counts given the predicted probabilities under a
    multinomial distribution. Can accept tensors with 2 or more dimensions
    and averages over all except for the last axis, which is the number
    of categories.

    Parameters
    ----------
    logps: jnp.ndarray, shape=(n, ..., L)
        A tensor with `n` examples and `L` possible categories. 

    true_counts: jnp.ndarray, shape=(n, ..., L)
        A tensor with `n` examples and `L` possible categories.

    Returns
    -------
    loss: float
        The multinomial log likelihood loss of the true counts given the
        predicted probabilities, averaged over all examples and all other
        dimensions.
    """

    log_fact_sum = gammaln(jnp.sum(true_counts, axis=-1) + 1)
    log_prod_fact = jnp.sum(gammaln(true_counts + 1), axis=-1)
    log_prod_exp = jnp.sum(true_counts * logps, axis=-1)
    return -log_fact_sum + log_prod_fact - log_prod_exp

@jit
def log1p_mse_loss(log_predicted_counts, true_counts):
    """A MSE loss on the log(x+1) of the inputs.

    This loss will accept tensors of predicted counts and a vector of true
    counts and return the MSE on the log of the labels. The squared error
    is calculated for each position in the tensor and then averaged, regardless
    of the shape.

    Note: The predicted counts are in log space but the true counts are in the
    original count space.

    Parameters
    ----------
    log_predicted_counts: jnp.ndarray, shape=(n, ...)
        A tensor of log predicted counts where the first axis is the number of
        examples. Important: these values are already in log space.

    true_counts: jnp.ndarray, shape=(n, ...)
        A tensor of the true counts where the first axis is the number of
        examples.

    Returns
    -------
    loss: jnp.ndarray, shape=(n, 1)
        The MSE loss on the log of the two inputs, averaged over all examples
        and all other dimensions.
    """

    log_true = jnp.log(true_counts + 1)
    return jnp.mean(jnp.square(log_true - log_predicted_counts), axis=-1)

@jit
def bpnet_loss(y_pred_profile, y_pred_counts, y_true_profile, y_true_counts, alpha):
    """Compute the combined loss for BPNet."""
    profile_loss = mnll_loss(y_pred_profile, y_true_profile).mean()
    count_loss = log1p_mse_loss(y_pred_counts, y_true_counts).mean()
    total_loss = profile_loss + alpha * count_loss

    return total_loss, (profile_loss, count_loss)


__all__ = ["mnll_loss", "log1p_mse_loss", "bpnet_loss"]