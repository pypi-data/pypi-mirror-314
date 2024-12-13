# KalaTorch
# Author : N V R K SAI KAMESH SHARMA

KalaTorch is a Python module designed for easy implementation of PyTorch models. It supports various AI architectures, such as basic feedforward neural networks, CNNs, RNNs, transformers, and more. This module simplifies the process of creating, training, and evaluating AI models.

---

## Features
- **Basic Neural Networks (MLP)**: Fully connected layers with customizable hidden layers.
- **CNN**: Convolutional Neural Networks for image processing.
- **RNN**: Recurrent Neural Networks for sequence data.
- **Transformer**: Attention-based models for advanced sequence tasks.
- **Recinear**: Simplified recurrent-linear networks.
- **QLable**: Q-Learning-inspired networks for reinforcement learning tasks.
- Automatic GPU/CPU support.

---

## Installation
To use KalaTorch, copy the `KalaTorch` class implementation into your Python project. Ensure PyTorch is installed:

```bash
pip install torch torchvision
```

---

## Example Usage

### Importing and Initializing
```python
from KalaTorch import KalaTorch
import torch
import torch.nn as nn
import torch.optim as optim
```

### Preparing Data
```python
# Example data for training
x_train = torch.randn(32, 784)  # 32 samples, each with 784 features
y_train = torch.randint(0, 10, (32,))  # 32 labels for 10 classes (0-9)

# Example data for evaluation
x_val = torch.randn(16, 784)  # 16 samples for validation
y_val = torch.randint(0, 10, (16,))  # 16 labels
```

### Full Code Examples for Supported Models

#### 1. **Basic MLP (Multi-Layer Perceptron)**
```python
# Create a basic MLP model
kala = KalaTorch(model_type="basic", input_size=784, output_size=10, hidden_layers=[128, 64])

# Compile the model
kala.compile(loss_fn=nn.CrossEntropyLoss(), optimizer_fn=optim.Adam, learning_rate=0.001)

# Training
for epoch in range(5):
    loss = kala.train_step(x_train, y_train)
    print(f"Epoch {epoch+1}, Training loss: {loss}")

# Evaluation
val_loss = kala.evaluate(x_val, y_val)
print(f"Validation loss: {val_loss}")

# Prediction
predictions = kala.predict(x_val)
print(predictions)
```

#### 2. **CNN (Convolutional Neural Network)**
```python
# Create a CNN model
kala = KalaTorch(model_type="cnn")

# Compile the model
kala.compile(loss_fn=nn.CrossEntropyLoss(), optimizer_fn=optim.SGD, learning_rate=0.01)

# Training
for epoch in range(5):
    loss = kala.train_step(x_train.view(-1, 1, 28, 28), y_train)  # Reshape data for CNN
    print(f"Epoch {epoch+1}, Training loss: {loss}")

# Evaluation
val_loss = kala.evaluate(x_val.view(-1, 1, 28, 28), y_val)  # Reshape data for CNN
print(f"Validation loss: {val_loss}")
```

#### 3. **RNN (Recurrent Neural Network)**
```python
# Create an RNN model
kala = KalaTorch(model_type="rnn")

# Compile the model
kala.compile(loss_fn=nn.MSELoss(), optimizer_fn=optim.Adam, learning_rate=0.001)

# Example sequential data (10 timesteps, 20 features)
x_seq_train = torch.randn(32, 10, 20)
y_seq_train = torch.randn(32, 10, 20)

# Training
for epoch in range(5):
    loss = kala.train_step(x_seq_train, y_seq_train)
    print(f"Epoch {epoch+1}, Training loss: {loss}")

# Evaluation
x_seq_val = torch.randn(16, 10, 20)
y_seq_val = torch.randn(16, 10, 20)
val_loss = kala.evaluate(x_seq_val, y_seq_val)
print(f"Validation loss: {val_loss}")
```

#### 4. **Transformer**
```python
# Create a Transformer model
kala = KalaTorch(model_type="transformer")

# Compile the model
kala.compile(loss_fn=nn.CrossEntropyLoss(), optimizer_fn=optim.Adam, learning_rate=0.001)

# Example transformer data (seq_len=10, d_model=512)
x_transformer_train = torch.randn(32, 10, 512)
y_transformer_train = torch.randint(0, 10, (32, 10))

# Training
for epoch in range(5):
    loss = kala.train_step(x_transformer_train, y_transformer_train)
    print(f"Epoch {epoch+1}, Training loss: {loss}")

# Evaluation
x_transformer_val = torch.randn(16, 10, 512)
y_transformer_val = torch.randint(0, 10, (16, 10))
val_loss = kala.evaluate(x_transformer_val, y_transformer_val)
print(f"Validation loss: {val_loss}")
```

#### 5. **Recinear**
```python
# Create a Recinear model
kala = KalaTorch(model_type="recinear", input_size=784, output_size=10)

# Compile the model
kala.compile(loss_fn=nn.CrossEntropyLoss(), optimizer_fn=optim.Adam, learning_rate=0.001)

# Training
for epoch in range(5):
    loss = kala.train_step(x_train, y_train)
    print(f"Epoch {epoch+1}, Training loss: {loss}")

# Evaluation
val_loss = kala.evaluate(x_val, y_val)
print(f"Validation loss: {val_loss}")
```

#### 6. **QLable**
```python
# Create a QLable model
kala = KalaTorch(model_type="qlable")

# Compile the model
kala.compile(loss_fn=nn.MSELoss(), optimizer_fn=optim.SGD, learning_rate=0.01)

# Example Q-Learning-like data (10 features)
x_qlable_train = torch.randn(32, 10)
y_qlable_train = torch.randn(32, 10)

# Training
for epoch in range(5):
    loss = kala.train_step(x_qlable_train, y_qlable_train)
    print(f"Epoch {epoch+1}, Training loss: {loss}")

# Evaluation
x_qlable_val = torch.randn(16, 10)
y_qlable_val = torch.randn(16, 10)
val_loss = kala.evaluate(x_qlable_val, y_qlable_val)
print(f"Validation loss: {val_loss}")
```

---

## API Reference

### `KalaTorch`
#### Initialization
```python
KalaTorch(model_type="basic", input_size=None, output_size=None, hidden_layers=None)
```
- `model_type` (str): Model architecture (`"basic"`, `"cnn"`, `"rnn"`, `"transformer"`, `"recinear"`, `"qlable"`).
- `input_size` (int): Input feature size (required for `"basic"` and `"recinear"`).
- `output_size` (int): Output size (required for `"basic"` and `"recinear"`).
- `hidden_layers` (list): List of hidden layer sizes (only for `"basic"`).

#### Methods
- `compile(loss_fn, optimizer_fn, learning_rate=0.001)`:
  - `loss_fn`: Loss function (e.g., `nn.CrossEntropyLoss`).
  - `optimizer_fn`: Optimizer function (e.g., `optim.Adam`).
  - `learning_rate`: Learning rate.

- `train_step(x, y)`:
  - `x`: Input tensor.
  - `y`: Target tensor.
  - Returns: Training loss.

- `evaluate(x, y)`:
  - `x`: Input tensor.
  - `y`: Target tensor.
  - Returns: Evaluation loss.

- `predict(x)`:
  - `x`: Input tensor.
  - Returns: Model predictions.

---

## Contributions
Feel free to contribute to KalaTorch! Fork the repository, make your changes, and submit a pull request.

---

## License

MIT License

Copyright (c) 2024 N V R K Sai Kamesh Sharma

This project is open-sourced under the MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE..

MIT License

Copyright (c) 2024 N V R K Sai Kamesh Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy

