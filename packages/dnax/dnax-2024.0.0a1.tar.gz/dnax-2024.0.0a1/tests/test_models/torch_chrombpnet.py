import torch


class TorchChromBPNet(torch.nn.Module):
    """PyTorch implementation of ChromBPNet for testing purposes."""
    
    def __init__(self, bias, accessibility, name):
        super().__init__()
        # Freeze the bias model parameters
        for parameter in bias.parameters():
            parameter.requires_grad = False

        self.bias = bias
        self.accessibility = accessibility
        self.name = name
        self.n_control_tracks = accessibility.n_control_tracks
        self.n_outputs = 1

    def forward(self, X, X_ctl=None):
        acc_profile, acc_counts = self.accessibility(X, X_ctl)
        bias_profile, bias_counts = self.bias(X, X_ctl)

        y_profile = acc_profile + bias_profile
        y_counts = torch.log(torch.exp(acc_counts) + torch.exp(bias_counts))
        
        return y_profile, y_counts