import torch
import torch.nn as nn
import torch.optim as optim

class KalaTorch:
    """
    KalaTorch: A module for easy implementation of PyTorch models with support for different AI architectures.
    """

    def __init__(self, model_type="basic", input_size=None, output_size=None, hidden_layers=None):
        """
        Initialize a KalaTorch model.

        Args:
            model_type (str): Type of model to initialize ('basic', 'cnn', 'rnn', 'transformer', 'recinear', 'qlable').
            input_size (int): Size of the input layer.
            output_size (int): Size of the output layer.
            hidden_layers (list): List of hidden layer sizes (for basic MLP models).
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_type = model_type.lower()

        if self.model_type == "basic":
            self.model = self._build_basic_model(input_size, output_size, hidden_layers)
        elif self.model_type == "cnn":
            self.model = self._build_cnn_model()
        elif self.model_type == "rnn":
            self.model = self._build_rnn_model()
        elif self.model_type == "transformer":
            self.model = self._build_transformer_model()
        elif self.model_type == "recinear":
            self.model = self._build_recinear_model(input_size, output_size)
        elif self.model_type == "qlable":
            self.model = self._build_qlable_model()
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")

        self.model.to(self.device)

    def _build_basic_model(self, input_size, output_size, hidden_layers):
        """Build a basic fully connected neural network."""
        layers = []
        if not hidden_layers:
            hidden_layers = [128, 64]
        all_layers = [input_size] + hidden_layers + [output_size]
        for i in range(len(all_layers) - 1):
            layers.append(nn.Linear(all_layers[i], all_layers[i + 1]))
            if i < len(all_layers) - 2:
                layers.append(nn.ReLU())
        return nn.Sequential(*layers)

    def _build_cnn_model(self):
        """Build a simple convolutional neural network."""
        return nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def _build_rnn_model(self):
        """Build a simple recurrent neural network."""
        return nn.RNN(input_size=10, hidden_size=20, num_layers=2, batch_first=True)

    def _build_transformer_model(self):
        """Build a simple transformer model."""
        return nn.Transformer(d_model=512, nhead=8, num_encoder_layers=6, num_decoder_layers=6)

    def _build_recinear_model(self, input_size, output_size):
        """Build a simple recurrent-linear model."""
        return nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )

    def _build_qlable_model(self):
        """Build a simple Q-Learning-inspired model."""
        class QLableModel(nn.Module):
            def __init__(self):
                super(QLableModel, self).__init__()
                self.fc1 = nn.Linear(10, 128)
                self.relu = nn.ReLU()
                self.fc2 = nn.Linear(128, 10)

            def forward(self, x):
                x = self.relu(self.fc1(x))
                return self.fc2(x)

        return QLableModel()

    def compile(self, loss_fn, optimizer_fn, learning_rate=0.001):
        """
        Compile the model by setting the loss function and optimizer.

        Args:
            loss_fn: Loss function (e.g., nn.CrossEntropyLoss).
            optimizer_fn: Optimizer function (e.g., optim.Adam).
            learning_rate (float): Learning rate for the optimizer.
        """
        self.loss_fn = loss_fn
        self.optimizer = optimizer_fn(self.model.parameters(), lr=learning_rate)

    def train_step(self, x, y):
        """
        Perform a single training step.

        Args:
            x: Input tensor.
            y: Target tensor.
        """
        self.model.train()
        x, y = x.to(self.device), y.to(self.device)

        self.optimizer.zero_grad()
        predictions = self.model(x)
        loss = self.loss_fn(predictions, y)
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def evaluate(self, x, y):
        """
        Evaluate the model on a validation/test dataset.

        Args:
            x: Input tensor.
            y: Target tensor.
        """
        self.model.eval()
        x, y = x.to(self.device), y.to(self.device)
        with torch.no_grad():
            predictions = self.model(x)
            loss = self.loss_fn(predictions, y)
        return loss.item()

    def predict(self, x):
        """
        Perform inference.

        Args:
            x: Input tensor.
        """
        self.model.eval()
        x = x.to(self.device)
        with torch.no_grad():
            predictions = self.model(x)
        return predictions

print("kala_torch")