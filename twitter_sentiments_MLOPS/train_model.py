from twitter_sentiments_MLOPS.models.model import SimpleNN

from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim
import torch.nn as nn
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoConfig, AutoModel
import torch
#from data.processed import embeddings
#from models import embedded_model

embedding_dim = 768  # Example for BERT-base model
hidden_dim = 128
output_dim = 4  


# Assuming embeddings_tensor and labels_tensor are your dataset tensors
# Split dataset into training and validation sets
train_embeddings, val_embeddings, train_labels, val_labels = train_test_split(
    embeddings_tensor, labels_tensor, test_size=0.2, random_state=42)

# Create training and validation datasets and dataloaders
train_dataset = TensorDataset(train_embeddings, train_labels)
val_dataset = TensorDataset(val_embeddings, val_labels)

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

# Your model, criterion, and optimizer remain the same
model = SimpleNN(embedding_dim, hidden_dim, output_dim)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training and Validation Loop
num_epochs = 5
for epoch in range(num_epochs):
    # Training
    model.train()
    train_loss = 0.0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

    # Print statistics
    print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss/len(train_loader)}, Validation Loss: {val_loss/len(val_loader)}")

print("Finished Training and Validation")

torch.save(model.state_dict(), 'models/first_model_state_dict.pth')

#torch.save(model, 'models/first_model.pth') # saves the full model