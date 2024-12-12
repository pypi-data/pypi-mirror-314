import jax
import jax.numpy as jnp
from jax import random

def random_one_hot(key, shape, probs=None, dtype=jnp.int8):
    """Generate random one-hot encodings using JAX.

    TODO:
    1. Add support for nucleotide frequencies.
    Would allow to provide frequencies of C and G 
    to simulate GC-content.
    2. Add support for dinucleotide frequencies.
    That should support partial frequencies provided
    e.g. {"AA": 0.3}. 


    Parameters
    ----------
    key : jax.random.PRNGKey
        The random key to use for generation.
    shape : tuple
        The shape of the 3D tensor to generate.
    probs : tuple, list, jax.numpy.ndarray, or None, optional
        A 2D array of probabilities. If None, use a uniform distribution.
    dtype : jax.numpy.dtype, optional
        The datatype to return the matrix as. Default is jnp.int8.

    Returns
    -------
    ohe : jax.numpy.ndarray
        A JAX array with the specified shape that is one-hot encoded.
    """
    if len(shape) != 3:
        raise ValueError("Shape must be a tuple with 3 dimensions.")

    batch_size, seq_len, alphabet_size = shape
    ohe = jnp.zeros(shape, dtype=dtype)

    def process_batch(i, carry):
        ohe, key, probs = carry
        key, subkey = random.split(key)

        if probs is None:
            probs_ = None
        elif probs.shape[0] == 1:
            probs_ = probs[0]
        else:
            probs_ = probs[i]

        choices = random.choice(subkey, alphabet_size, shape=(seq_len,), p=probs_)
        ohe = ohe.at[i, jnp.arange(seq_len), choices].set(1)

        return (ohe, key, probs)

    if probs is not None:
        probs = jnp.asarray(probs)

    final_ohe, _, _ = jax.lax.fori_loop(0, batch_size, process_batch, (ohe, key, probs))

    return final_ohe