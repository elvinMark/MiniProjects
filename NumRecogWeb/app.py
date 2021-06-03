from flask import Flask,render_template,request
import torch
import torch.nn as nn
from MyModel import MLP,train
import numpy as np
import matplotlib.pyplot as plt 
import os

app = Flask(__name__)
model = MLP(784,200,10)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(),lr=0.1)

if os.path.exists("model_data.pt"):
    model.load_state_dict(torch.load("model_data.pt"))

@app.route("/",methods=["POST","GET"])
def home():
    return render_template("index.html");

@app.route("/guess",methods=["POST"])
def guess():
    data = request.form["mydata"]
    x = np.array(list(map(int,data)))
    data = torch.tensor(x).float()
    _,num = model(data).max(0)
    return str(num.item())

@app.route("/train",methods=["POST"])
def train_model():
    num_epochs = 20
    images_data = request.form["images"]
    labels_data = request.form["labels"]

    x = [list(map(int,i)) for i in images_data[:-1].split('\n')]
    images_data = torch.tensor(x).float()
    labels_data = torch.tensor(list(map(int,labels_data[:-1].split('\n')))).long()

    train_dataset = torch.utils.data.TensorDataset(images_data,labels_data)
    train_dataloader = torch.utils.data.DataLoader(train_dataset)

    loss = []
    for epoch in range(num_epochs):
        tmp = train(model,criterion,optimizer,train_dataloader)
        loss.append(float(tmp))
    torch.save(model.state_dict(),"model_data.pt")

    response = {"loss":loss,"last_loss":loss[-1],"result":"Training Succesful!" if loss[-1]<0.3 else "Training not succseful"}
    return response

if __name__=="__main__":
    app.run(host="0.0.0.0",port="5000")
