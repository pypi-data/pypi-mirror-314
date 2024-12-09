from model.model import Model  # Assuming Model is defined as per the previous Jittor conversion
import jittor as jt

# Configuration
config = {
    'epoch': 100,
    'w': 224,
    'h': 224,
    'class_num': 5,
    'len': 100,
    'lr': 1e-2
}

# Create input tensor
x = jt.rand((config['len'], 3, config['w'], config['h']), requires_grad=True)

# Initialize the model
model = Model()

# Forward pass
y = model(x)

# Print the output
print(f'The running result of the current model is {y.numpy()}')
