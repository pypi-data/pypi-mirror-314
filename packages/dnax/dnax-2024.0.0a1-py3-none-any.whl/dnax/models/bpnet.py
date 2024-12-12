from typing import Optional

import jax.numpy as jnp
from flax import nnx

# from .losses import mnll_loss, log1p_mse_loss
# from .performance import calculate_performance_measures
# from .logging import Logger

class BPNet(nnx.Module):
    """
    BPNet (Base-resolution Prediction of Transcription factor binding Neural Network) model.

    This model predicts transcription factor binding profiles and counts from DNA sequences.
    It uses a series of dilated convolutions followed by profile and count prediction heads.

    Input shape: (N, L, C) where:
        N is the batch size
        L is the sequence length
        C is the number of input channels (typically 4 for one-hot encoded DNA sequences)

    Output shapes:
        Profile: (N, L - 2*trimming, n_outputs)
        Counts: (N, 1)

    Args:
        n_features (int): Number of convolutional filters in each layer.
        n_layers (int): Number of dilated convolutional layers.
        n_outputs (int): Number of output tracks for profile prediction.
        n_control_tracks (int): Number of control tracks (optional input).
        kernel_size (int): Kernel size for dilated convolutions.
        dilation_rate (int): Base dilation rate for dilated convolutions.
        alpha (float): Scaling factor for the output (not used in forward pass).
        trimming (int): Number of base pairs to trim from each end of the output.
        output_length (int): Length of the output sequence.
        use_profile_output_bias (bool): Whether to use bias in the profile output layer.
        use_count_output_bias (bool): Whether to use bias in the count output layer.
        use_initial_conv_bias (bool): Whether to use bias in the initial convolutional layer.
        use_dilated_conv_bias (bool): Whether to use bias in the dilated convolutional layers.
    """
    def __init__(self,     
                n_features: int = 64,
                n_layers: int = 8,
                *,
                input_features: int = 4,  # 4 nucleotides 
                n_outputs: int = 1,
                n_control_tracks: int = 0,
                initial_conv_kernel_size: int = 21,
                residual_block_kernel_size: int = 3,
                profile_conv_kernel_size: int = 75,
                dilation_rate: int = 2,
                alpha: float = 1.0,
                trimming: Optional[int] = None,
                output_length: Optional[int] = None,
                use_profile_output_bias: bool = True,
                use_count_output_bias: bool = True,
                use_initial_conv_bias: bool = True,
                use_dilated_conv_bias: bool = True,
                rngs: nnx.Rngs):
    
        # Parameters
        
        self.n_features = n_features
        self.n_layers = n_layers

        self.input_features = input_features
        self.n_outputs = n_outputs
        self.n_control_tracks = n_control_tracks
        
        self.initial_conv_kernel_size = initial_conv_kernel_size
        self.residual_block_kernel_size = residual_block_kernel_size
        self.profile_conv_kernel_size = profile_conv_kernel_size

        self.dilation_rate = dilation_rate
        self.alpha = alpha
        self.trimming = trimming
        self.output_length = output_length
        self.use_profile_output_bias = use_profile_output_bias
        self.use_count_output_bias = use_count_output_bias
        self.use_initial_conv_bias = use_initial_conv_bias
        self.use_dilated_conv_bias = use_dilated_conv_bias


        # Layers

        self.initial_conv = nnx.Conv(in_features=self.input_features, out_features=self.n_features, kernel_size=(self.initial_conv_kernel_size,), padding='SAME', use_bias=self.use_initial_conv_bias, rngs=rngs)

        self.residual_blocks = [
            nnx.Conv(
                in_features=self.n_features,
                out_features=self.n_features,
                kernel_size=(self.residual_block_kernel_size,),
                padding='SAME',
                kernel_dilation=(self.dilation_rate**i,),
                use_bias=self.use_dilated_conv_bias,
                rngs=rngs,
            )
            for i in range(1, self.n_layers + 1)
        ]

        self.profile_conv = nnx.Conv(in_features=self.n_features + self.n_control_tracks, out_features=self.n_outputs, kernel_size=(self.profile_conv_kernel_size,), padding='SAME', 
                                    use_bias=self.use_profile_output_bias,
                                    rngs=rngs)
        
        n_count_control = 1 if self.n_control_tracks > 0 else 0
        self.count_linear = nnx.Linear(in_features=self.n_features + n_count_control, out_features=1, use_bias=self.use_count_output_bias, rngs=rngs)

    def __call__(self, x, x_ctl=None):
        """
        Forward pass of the BPNet model.

        Args:
            x (jnp.ndarray): Input tensor of shape (N, L, C), where N is the batch size,
                             L is the sequence length, and C is the number of input channels (typically 4 for DNA).
            x_ctl (jnp.ndarray, optional): Control tracks tensor of shape (N, L, n_control_tracks).

        Returns:
            tuple: (y_profile, y_counts)
                y_profile (jnp.ndarray): Predicted binding profiles of shape (L - 2*trimming, n_outputs).
                y_counts (jnp.ndarray): Predicted binding counts of shape (1,).
        """

        start, end = self.trimming, x.shape[1] - self.trimming

        x = self.initial_conv(x)
        x = nnx.relu(x)
        for block in self.residual_blocks:
            res = x
            x = block(x)
            x = nnx.relu(x)
            x += res

        if x_ctl is None:
            x_w_ctl = x
        else:
            x_w_ctl = jnp.concatenate([x, x_ctl], axis=-1)

        y_profile = self.profile_conv(x_w_ctl)[:, start:end, :]

        # The 37 bp extension on each side (74 bp total) corresponds to the receptive field
        # of the profile head (75 bp convolution). This ensures that the count prediction
        # has access to the same genomic context as the profile prediction.
        x_mean = jnp.mean(x[:, start-37:end+37, :], axis=1)
        if x_ctl is not None:
            x_ctl_sum = jnp.sum(x_ctl[:, start-37:end+37, :], axis=(1, 2), keepdims=True)
            x_ctl_sum = jnp.squeeze(x_ctl_sum, axis=1)
            x_mean = jnp.concatenate([x_mean, jnp.log1p(x_ctl_sum)], axis=1)

        # y_counts = self.count_linear(x_mean).reshape(x.shape[0], 1)
        y_counts = self.count_linear(x_mean)

        return y_profile, y_counts
