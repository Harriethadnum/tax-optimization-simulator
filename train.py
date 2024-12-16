import numpy as np
from tensor import Tensor
from layers import Dense
from activations import relu
from loss import mean_squared_error
from optimizer import Optimizer

# Dummy data
X = np.array([[1], [2], [3], [4]])  # Input
y = np.array([[2], [4], [6], [8]])  # Output (we want a model to learn to double the input)

# Build the model
model = [Dense(1, 1, activation=relu)]  # One dense layer with 1 input and 1 output

# Training setup
optimizer = Optimizer(learning_rate=0.1)
epochs = 100

# Training loop
for epoch in range(epochs):
    # Forward pass
    for x_batch, y_batch in zip(X, y):
        x_tensor = Tensor(x_batch)
        y_tensor = Tensor(y_batch)
        y_pred = model[0].forward(x_tensor)
        
        # Compute loss
        loss = mean_squared_error(y_tensor, y_pred)
        
        # Backward pass (simplified)
        # In real life, you’d calculate the gradient here
        
        # Print progress
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss}")

    # Update weights
    optimizer.update(model[0])

