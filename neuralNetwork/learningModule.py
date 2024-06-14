import torch
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader
import tensorInit


class NeurualNetwork(nn.Module):
    def __init__(self):
        super(NeurualNetwork, self).__init__()
        self.data = tensorInit.VkDataset()
        self.layer1 = nn.Linear(188, 128)
        self.layer2 = nn.Linear(128, 64)
        self.layer3 = nn.Linear(64, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.sigmoid(self.layer3(x))
        return x

def main():
    model = NeurualNetwork()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    num_epochs = 1000

    train_loader = DataLoader(dataset=model.data, batch_size=4, shuffle=True, num_workers=8)

    for epoch in range(num_epochs):
        model.train()
        for X_batch, Y_batch in train_loader:
            optimizer.zero_grad()
            y_pred = model(X_batch)
            loss = criterion(y_pred, Y_batch)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')

if __name__ == "__main__":
    main()