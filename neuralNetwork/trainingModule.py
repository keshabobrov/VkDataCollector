import torch
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader

import tensorInit

device = torch.device('mps') # For Apple Silicon GPU support

class NeurualNetwork(nn.Module):
    # HACK: Class methods could and should be optimized, but it's redundant for purpose of our research.
    def __init__(self):
        super(NeurualNetwork, self).__init__()
        self.data = tensorInit.VkDataset(0)
        self.layer0 = nn.Linear(188, 188)
        self.layer1 = nn.Linear(188, 188)
        self.layer2 = nn.Linear(188, 188)
        self.layer3 = nn.Linear(188, 128)
        self.layer4 = nn.Linear(128, 128)
        self.layer5 = nn.Linear(128, 128)
        self.layer6 = nn.Linear(128, 128)
        self.layer7 = nn.Linear(128, 128)
        self.layer8 = nn.Linear(128, 64)
        self.layer9 = nn.Linear(64, 64)
        self.layer10 = nn.Linear(64, 64)
        self.layer11 = nn.Linear(64, 64)
        self.layer12 = nn.Linear(64, 32)
        self.layer13 = nn.Linear(32, 32)
        self.layer14 = nn.Linear(32, 32)
        self.layer15 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.relu(self.layer0(x))
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.relu(self.layer3(x))
        x = self.relu(self.layer4(x))
        x = self.relu(self.layer5(x))
        x = self.relu(self.layer6(x))
        x = self.relu(self.layer7(x))
        x = self.relu(self.layer8(x))
        x = self.relu(self.layer9(x))
        x = self.relu(self.layer10(x))
        x = self.relu(self.layer11(x))
        x = self.relu(self.layer12(x))
        x = self.relu(self.layer13(x)) 
        x = self.relu(self.layer14(x))
        x = self.sigmoid(self.layer15(x))
        return x


def train_model():
    model = NeurualNetwork()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    num_epochs = 400
    # I have tried different factor and patience values. Mode and scheduler type I have kept as is
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10)

    train_loader = DataLoader(dataset=model.data, batch_size=32, shuffle=True, num_workers=0)
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for X_batch, Y_batch in train_loader:
            optimizer.zero_grad()
            X_batch.to(device)
            Y_batch.to(device) 
            y_pred = model(X_batch)
            loss = criterion(y_pred, Y_batch)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        avg_loss = running_loss / len(train_loader)
        scheduler.step(avg_loss)
        print(f'Epoch {epoch}/{num_epochs}, Loss: {avg_loss}, LR: {scheduler.get_last_lr()}')
    torch.save(model.state_dict(), 'model.pth')
    check_model(model)

def check_model(model):
    model.eval()
    test_tensor = tensorInit.VkDataset(1)
    average_loss = 0
    def get_status(value):
        """
            Here's we are defining criteries for gov/opposition support classifications.
            We are not using this values for testing.
            We are usining it for model evaluation.
                - <0.4 — government support
                - 0.4-0.6 — unknown support
                - >0.6 — opposition support
            Here's we are comparing test dataset (another 10K values) with predicted value
        """
        if value.item() > 0.6:
            return 1
        elif value.item() <= 0.6 and value.item() >= 0.4:
            return 0.5
        elif value.item() < 0.4:
            return 0
    for x, y in test_tensor: 
        with torch.no_grad():
            prediction = get_status(model(x))
            y_status = get_status(y)
            if prediction != y_status:
                average_loss += 1
    print(average_loss)

if __name__ == "__main__":
    """
        Saved model files can be found in folder _models_
        Description of arguments can be found in file algorithm_arguments.
    """
    train_model()
    