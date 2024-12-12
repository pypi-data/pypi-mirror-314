import jax.numpy as jnp
from flax import nnx
from .bpnet import BPNet

class ChromBPNet(nnx.Module):
    def __init__(self, bias: BPNet, accessibility: BPNet):
        self.bias = nnx.clone(bias)
        self.accessibility = nnx.clone(accessibility)

    def __call__(self, x, x_ctl=None):
        acc_profile, acc_counts = self.accessibility(x, x_ctl)
        bias_profile, bias_counts = self.bias(x, x_ctl)

        y_profile = acc_profile + bias_profile
        y_counts = jnp.log(jnp.exp(acc_counts) + jnp.exp(bias_counts))

        return y_profile, y_counts
