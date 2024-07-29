# -*- coding: utf-8 -*-
"""8. CNN 모델.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Kh4kMYkgV6vYJggaJyYi1m4VZf0L5PUv

# **1. 간단한 CNN 모델 만들기**
"""

import torch
import torch.nn as nn
import torch.optim as optim

# 배치크기 * 채널(1: 그레이스케일, 3: 트루컬러) * 너비 * 높이
inputs = torch.Tensor(1, 1, 28, 28) # 입력 크기
print(inputs.shape)

# 첫번째 Conv2D
conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding='same') # 가중치 32개로 늘림. 3*3커널
out = conv1(inputs)
print(out.shape)

# 첫번째 MaxPool2D
pool = nn.MaxPool2d(kernel_size=2) # 이미지 크기 반으로
out = pool(out)
print(out.shape)

# 두번째 Conv2D
conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding='same')
out = conv2(out)
print(out.shape)

# 두번째 MaxPool2D
pool = nn.MaxPool2d(kernel_size=2)
out = pool(out)
print(out.shape)

flatten = nn.Flatten() # 데이터 한 줄로
out = flatten(out)
print(out.shape) # 64 * 7 * 7

fc = nn.Linear(3136, 10) # 10개의 클래스로
out = fc(out)
print(out.shape)

"""# **2. CNN으로 MNIST 분류하기**"""

import torchvision.datasets as datasets
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)

train_data = datasets.MNIST(
    root = 'data',
    train = True,
    transform = transforms.ToTensor(),
    download = True
) # MNIST 데이터(train)

test_data = datasets.MNIST(
    root = 'data',
    train = False,
    transform = transforms.ToTensor(),
    download = True
) # MNIST 데이터(test)

train_data

test_data

loader = DataLoader(
    dataset = train_data,
    batch_size = 64,
    shuffle = True
)

imgs, labels = next(iter(loader))
fig, axes = plt.subplots(8, 8, figsize=(16, 16))

# 데이터 출력
for ax, img, label in zip(axes.flatten(), imgs, labels):
    ax.imshow(img.reshape((28, 28)), cmap='gray')
    ax.set_title(label.item())
    ax.axis('off')

model = nn.Sequential(
    # 히든 레이어 쌓기
    # 히든 레이어 1
    nn.Conv2d(1, 32, kernel_size=3, padding='same'),
    nn.ReLU(),
    nn.MaxPool2d(kernel_size=2),
    # 히든 레이어 2
    nn.Conv2d(32, 64, kernel_size=3, padding='same'),
    nn.ReLU(),
    nn.MaxPool2d(kernel_size=2),

    nn.Flatten(),
    nn.Linear(64*7*7, 10)
).to(device)

model

optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 10

for epoch in range(epochs):
    sum_losses = 0
    sum_accs = 0

    for x_batch, y_batch in loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        y_pred = model(x_batch)
        loss = nn.CrossEntropyLoss()(y_pred, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        sum_losses = sum_losses + loss
        y_prob = nn.Softmax(1)(y_pred)
        y_pred_index = torch.argmax(y_prob, axis=1)
        acc = (y_batch == y_pred_index).float().sum() / len(y_batch) * 100
        sum_accs = sum_accs + acc
    avg_loss = sum_losses / len(loader)
    avg_acc = sum_accs / len(loader)
    print(f'Epoch {epoch:4d}/{epochs} Loss: {avg_loss:.6f} Accuracy: {avg_acc:.2f}%')

test_loader = DataLoader(
    dataset = test_data,
    batch_size = 64,
    shuffle = False
)

imgs, labels = next(iter(test_loader))
fig, axes = plt.subplots(8, 8, figsize=(16, 16))

for ax, img, label in zip(axes.flatten(), imgs, labels):
    ax.imshow(img.reshape((28, 28)), cmap='gray')
    ax.set_title(label.item())
    ax.axis('off')

model.eval() # 모델을 테스트 모드로 전환 (학습 모드 동작X)

sum_accs = 0

for x_batch, y_batch in test_loader:
    x_batch = x_batch.to(device)
    y_batch = y_batch.to(device)
    y_pred = model(x_batch)
    y_prob = nn.Softmax(1)(y_pred)
    y_pred_index = torch.argmax(y_prob, axis=1)
    acc = (y_batch == y_pred_index).float().sum() / len(y_batch) * 100
    sum_accs = sum_accs + acc

avg_acc = sum_accs / len(test_loader)
print(f'테스트 정확도는 {avg_acc:.2f}% 입니다.')

"""# **3. ○, X, △ 분류하기**
○, X, △를 그림판에 여러가지 이미지를 저장 후 CNN으로 학습을 시켜 해당 데이터를 분류하는 모델을 만들어보자.
"""

import torchvision

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/컴퓨터비전_시즌2/4. 딥러닝 기초/data

!unzip -qq "/content/drive/MyDrive/컴퓨터비전_시즌2/4. 딥러닝 기초/data/shape.zip"

# 데이터 경로
train_path = '/content/drive/MyDrive/컴퓨터비전_시즌2/4. 딥러닝 기초/data/shape/train'
test_path = '/content/drive/MyDrive/컴퓨터비전_시즌2/4. 딥러닝 기초/data/shape/test'

# 이미지 28*28 변환
# 그레이스케일 적용
# 텐서 변환
# 정규화 적용
# 색반전(배경 흰색, 글 검정 -> 배경 검정, 글 흰색)
transformer = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.Grayscale(1),
    transforms.ToTensor(),
    transforms.Normalize((0.5), (0.5)), # 평균 0.5 표준편차 0.5로 정규화
    transforms.RandomInvert(1)
])

trainset = torchvision.datasets.ImageFolder(root=train_path, transform=transformer)
testset = torchvision.datasets.ImageFolder(root=test_path, transform=transformer)

len(trainset), len(testset)

trainset.classes, testset.classes

class_map = {
    0: 'cir',
    1: 'tri',
    2: 'x'
}

loader = DataLoader(
    dataset=trainset,
    batch_size=8,
    shuffle=True
)

imgs, labels = next(iter(loader))
fig, axes = plt.subplots(2, 4, figsize=(8, 4))

for ax, img, label in zip(axes.flatten(), imgs, labels):
    ax.imshow(img.reshape(28, 28), cmap='gray')
    ax.set_title(class_map[label.item()])
    ax.axis('off')

device = 'cuda' if torch.cuda.is_available() else 'cpu'
device

model = nn.Sequential(
    nn.Conv2d(1, 32, kernel_size=3, padding='same'),
    nn.ReLU(),

    nn.Conv2d(32, 32, kernel_size=3, padding='same'),
    nn.ReLU(),

    nn.MaxPool2d(kernel_size=2),
    nn.Dropout(0.25),

    nn.Conv2d(32, 64, kernel_size=3, padding='same'),
    nn.ReLU(),

    nn.Conv2d(64, 64, kernel_size=3, padding='same'),
    nn.ReLU(),

    nn.MaxPool2d(kernel_size=2),
    nn.Dropout(0.25),

    nn.Flatten(),
    nn.Linear(64*7*7, 3)
).to(device)

model

optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 20

for epoch in range(epochs):
    sum_losses = 0
    sum_accs = 0

    for x_batch, y_batch in loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        y_pred = model(x_batch)
        loss = nn.CrossEntropyLoss()(y_pred, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        sum_losses = sum_losses + loss
        y_prob = nn.Softmax(1)(y_pred)
        y_pred_index = torch.argmax(y_prob, axis=1)
        acc = (y_batch == y_pred_index).float().sum() / len(y_batch) * 100
        sum_accs = sum_accs + acc

    avg_loss = sum_losses / len(loader)
    avg_acc = sum_accs / len(loader)
    print(f'Epoch {epoch:4d}/{epochs} Loss: {avg_loss:.6f} Accuracy: {avg_acc:.2f}%')

test_loader = DataLoader(
    dataset=testset,
    batch_size=8,
    shuffle=True
)

imgs, labels = next(iter(test_loader))
fig, axes = plt.subplots(2, 4, figsize=(8, 4))

for ax, img, label in zip(axes.flatten(), imgs, labels):
    ax.imshow(img.reshape(28, 28), cmap='gray')
    ax.set_title(class_map[label.item()])
    ax.axis('off')

model.eval()

sum_accs = 0

img_list    = torch.Tensor().to(device)
y_pred_list = torch.Tensor().to(device)
y_true_list = torch.Tensor().to(device)


for x_batch, y_batch in test_loader:
    x_batch = x_batch.to(device)
    y_batch = y_batch.to(device)
    y_pred = model(x_batch)
    y_prob = nn.Softmax(1)(y_pred)
    y_pred_index = torch.argmax(y_prob, axis=1)

    y_pred_list = torch.cat((y_pred_list, y_pred_index), dim=0)
    y_true_list = torch.cat((y_true_list, y_batch), dim=0)
    img_list = torch.cat((img_list, x_batch), dim=0)

    acc = (y_batch == y_pred_index).float().sum() / len(y_batch) * 100
    sum_accs = sum_accs + acc

avg_acc = sum_accs / len(test_loader)
print(f'테스트 정확도는 {avg_acc:.2f}% 입니다.')

fig, axes = plt.subplots(12, 5, figsize=(25, 25))

img_list_cpu = img_list.cpu()
y_pred_list_cpu = y_pred_list.cpu()
y_true_list_cpu = y_true_list.cpu()

for ax, img, y_pred, y_true in zip(axes.flatten(), img_list_cpu, y_pred_list_cpu, y_true_list_cpu):
  ax.imshow(img.reshape(28, 28), cmap='gray')
  ax.set_title(f'pred: {class_map[y_pred.item()]}, true: {class_map[y_true.item()]}')
  ax.axis('off')

plt.show()

