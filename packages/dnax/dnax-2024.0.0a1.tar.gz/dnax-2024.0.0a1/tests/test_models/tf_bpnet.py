from tensorflow.keras.backend import int_shape
from tensorflow.keras.layers import Input, Cropping1D, add, Conv1D, GlobalAvgPool1D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
import tensorflow as tf
import tensorflow_probability as tfp
import os

# Set random seed for reproducibility
os.environ['PYTHONHASHSEED'] = '0'


# from chrombpnet/trianing/utils/losses.py
# originally from https://github.com/kundajelab/basepair/blob/cda0875571066343cdf90aed031f7c51714d991a/basepair/losses.py#L87
def multinomial_nll(true_counts, logits):
    """Compute the multinomial negative log-likelihood
    Args:
      true_counts: observed count values
      logits: predicted logit values
    """
    counts_per_example = tf.reduce_sum(true_counts, axis=-1)
    dist = tfp.distributions.Multinomial(total_count=counts_per_example,
                                         logits=logits)
    return (-tf.reduce_sum(dist.log_prob(true_counts)) /
            tf.cast(tf.shape(true_counts)[0], dtype=tf.float32))


class TFBPNet:
    """
    NOTE: This TensorFlow implementation is based on the ChromBPNet repo, and
          it does not currently support a control track (X_ctl) as part of input.
    """
    def __init__(self, args, model_params):
        """Initialize and build the model in one step."""
        self.learning_rate = args.learning_rate
        self.filters = int(model_params['filters'])
        self.n_dil_layers = int(model_params['n_dil_layers'])
        self.counts_loss_weight = float(model_params['counts_loss_weight'])
        self.sequence_len = int(model_params["inputlen"])
        self.out_pred_len = int(model_params["outputlen"])
        self.num_tasks = int(model_params["num_tasks"])
        
        # Fixed parameters
        self.conv1_kernel_size = 21
        self.profile_kernel_size = 75

        # Build the model as part of the initialization
        inp = Input(shape=(self.sequence_len, 4), name='sequence')

        # First convolution without dilation
        x = Conv1D(self.filters,
                   kernel_size=self.conv1_kernel_size,
                   padding='valid', 
                   activation='relu',
                   name='bpnet_1st_conv')(inp)

        # Add dilated convolutions
        layer_names = [str(i) for i in range(1, self.n_dil_layers + 1)]
        
        for i in range(1, self.n_dil_layers + 1):
            conv_layer_name = f'bpnet_{layer_names[i-1]}conv'
            conv_x = Conv1D(self.filters, 
                            kernel_size=3, 
                            padding='valid',
                            activation='relu', 
                            dilation_rate=2**i,
                            name=conv_layer_name)(x)

            # Ensure symmetric cropping
            x_len = int_shape(x)[1]
            conv_x_len = int_shape(conv_x)[1]
            assert (x_len - conv_x_len) % 2 == 0, "Cropping mismatch"

            x = Cropping1D((x_len - conv_x_len) // 2, 
                           name=f'bpnet_{layer_names[i-1]}crop')(x)
            x = add([conv_x, x])

        # Branch 1: Profile prediction
        prof_out_precrop = Conv1D(filters=self.num_tasks,
                                  kernel_size=self.profile_kernel_size,
                                  padding='valid',
                                  name='prof_out_precrop')(x)

        cropsize = int(int_shape(prof_out_precrop)[1] / 2) - int(self.out_pred_len / 2)
        assert cropsize >= 0, "Invalid crop size"
        assert int_shape(prof_out_precrop)[1] % 2 == 0, "Symmetric cropping required"
        
        prof = Cropping1D(cropsize, 
                          name='logits_profile_predictions_preflatten')(prof_out_precrop)

        profile_out = Flatten(name="logits_profile_predictions")(prof)

        # Branch 2: Counts prediction
        gap_combined_conv = GlobalAvgPool1D(name='gap')(x)
        count_out = Dense(self.num_tasks, name="logcount_predictions")(gap_combined_conv)

        # Compile the model
        self.model = Model(inputs=[inp], outputs=[profile_out, count_out])
        self.model.compile(optimizer=Adam(learning_rate=self.learning_rate),
                           loss=[multinomial_nll, 'mse'],
                           loss_weights=[1, self.counts_loss_weight])
