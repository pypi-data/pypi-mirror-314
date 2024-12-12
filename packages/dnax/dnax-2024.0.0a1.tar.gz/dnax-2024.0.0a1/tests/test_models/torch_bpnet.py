import torch

class TorchBPNet(torch.nn.Module):
	"""
	This module follows the PyTorch BPNet implementation and borrows code from bpnet-lite:
	https://github.com/jmschrei/bpnet-lite.
	"""
	def __init__(self, n_filters=64, n_layers=8, n_outputs=2, 
		n_control_tracks=2, alpha=1, profile_output_bias=True, 
		count_output_bias=True, name=None, trimming=None):
		super().__init__()
		self.n_filters = n_filters
		self.n_layers = n_layers
		self.n_outputs = n_outputs
		self.n_control_tracks = n_control_tracks

		self.alpha = alpha
		self.name = name or "bpnet.{}.{}".format(n_filters, n_layers)
		self.trimming = trimming or 2 ** n_layers

		self.iconv = torch.nn.Conv1d(4, n_filters, kernel_size=21, padding=10)
		self.irelu = torch.nn.ReLU()

		self.rconvs = torch.nn.ModuleList([
			torch.nn.Conv1d(n_filters, n_filters, kernel_size=3, padding=2**i, 
				dilation=2**i) for i in range(1, self.n_layers+1)
		])
		self.rrelus = torch.nn.ModuleList([
			torch.nn.ReLU() for i in range(1, self.n_layers+1)
		])

		self.fconv = torch.nn.Conv1d(n_filters+n_control_tracks, n_outputs, 
			kernel_size=75, padding=37, bias=profile_output_bias)
		
		n_count_control = 1 if n_control_tracks > 0 else 0
		self.linear = torch.nn.Linear(n_filters+n_count_control, 1, 
			bias=count_output_bias)

	def forward(self, X, X_ctl=None):
		"""A forward pass of the model.

		This method takes in a nucleotide sequence X, a corresponding
		per-position value from a control track, and a per-locus value
		from the control track and makes predictions for the profile 
		and for the counts. This per-locus value is usually the
		log(sum(X_ctl_profile) + 1) when the control is an experimental
		read track but can also be the output from another model.

		Parameters
		----------
		X: torch.tensor, shape=(batch_size, 4, length)
			The one-hot encoded batch of sequences.

		X_ctl: torch.tensor or None, shape=(batch_size, n_strands, length)
			A value representing the signal of the control at each position in 
			the sequence. If no controls, pass in None. Default is None.

		Returns
		-------
		y_profile: torch.tensor, shape=(batch_size, n_strands, out_length)
			The output predictions for each strand trimmed to the output
			length.
		y_counts: torch.tensor, shape=(batch_size, 1)
			Total counts for the input sequence.
		"""

		start, end = self.trimming, X.shape[2] - self.trimming

		X = self.irelu(self.iconv(X))
		for i in range(self.n_layers):
			X_conv = self.rrelus[i](self.rconvs[i](X))
			X = torch.add(X, X_conv)

		if X_ctl is None:
			X_w_ctl = X
		else:
			X_w_ctl = torch.cat([X, X_ctl], dim=1)

		y_profile = self.fconv(X_w_ctl)[:, :, start:end]

		# counts prediction
		X = torch.mean(X[:, :, start-37:end+37], dim=2)

		if X_ctl is not None:
			X_ctl = torch.sum(X_ctl[:, :, start-37:end+37], dim=(1, 2))
			X_ctl = X_ctl.unsqueeze(-1)
			X = torch.cat([X, torch.log(X_ctl+1)], dim=-1)

		print(X.shape)
		y_counts = self.linear(X).reshape(X.shape[0], 1)
		return y_profile, y_counts
