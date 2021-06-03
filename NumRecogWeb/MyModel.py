import torch
import torch.nn as nn
from sklearn import datasets as ds
from sklearn.model_selection import train_test_split
import numpy as np

class MLP(nn.Module):
    def __init__(self,inp,hid,out):
        super(MLP,self).__init__()
        self.fc1 = nn.Linear(inp,hid)
        self.act_fun1 = nn.ReLU()
        self.fc2 = nn.Linear(hid,out)
    def forward(self,x):
        o = self.fc1(x)
        o = self.act_fun1(o)
        o = self.fc2(o)
        return o

def train(model,criterion,optimizer,dataloader):
    model.train()
    tot_loss = 0
    for data,label in dataloader:
        o = model(data)
        loss = criterion(o,label)
        tot_loss += loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return tot_loss/len(dataloader)

if __name__ == "__main__":
    # Training using MNIST
    learning_rate = 0.1
    batch_size = 1000
    num_epochs = 20

    X,y = ds.fetch_openml("mnist_784",version=1,return_X_y=True)
    X /= 255.0
    y = np.array(list(map(int,y)))
    
    x_train, x_test, y_train, y_test = train_test_split(X,y)

    x_train_tensor = torch.tensor(x_train).float()
    y_train_tensor = torch.tensor(y_train).long()
    
    x_test_tensor = torch.tensor(x_test).float()
    y_test_tensor = torch.tensor(y_test).long()
    
    train_dataset = torch.utils.data.TensorDataset(x_train_tensor,y_train_tensor)
    test_dataset = torch.utils.data.TensorDataset(x_test_tensor,y_test_tensor)   

    train_loader = torch.utils.data.DataLoader(train_dataset,batch_size=batch_size)
    test_loader = torch.utils.data.DataLoader(test_dataset,batch_size=batch_size)


    model = MLP(784,200,10)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(),lr=learning_rate)
    
    for epoch in range(num_epochs):
        loss = train(model,criterion,optimizer,train_loader)
        print(loss)
    torch.save(model.state_dict(),"model_data.pt")
    pred = model(x_test_tensor[:30])
    _,pred = pred.max(1)
    print(pred)
    print(y_test_tensor[:30])
