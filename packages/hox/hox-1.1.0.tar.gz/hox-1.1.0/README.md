<div align="center">
<h1>HOX</h1>
HOX is not an alternative to big ml library like pytorch or tensorflow, it lacks features and optimization, such as gpu support. The goal is to create a lightweight library (< 100 lines of code) that is easy to use and quick to implement for creating small projects or experiment with ml.<br><br>
</div>

```cmd
pip install hox
```

---

## examples/mnist
The code snippet down below shows mnist training. The utils module used to load mnist is not directly installed with hox, you can find it in this github repo at examples/mnist
```python
from hox import *
import utils

#Create model (2 layers, 784 input neurons, 144 first layer, 10 output layer)
model = Model.create([Dense(784, 144, Relu()), Dense(144, 10, Sigmoid())])

#Upload mnist dataset
X, Y, x, y = utils.mnist()

#Shuffle the dataset to improve training stability
indices = np.random.permutation(len(X))
X, Y = X[indices], Y[indices]

#Train the model
model.train(X, Y, epochs = 1, rate = 2, batch_size = 16)

#Save the trained model
model.save("mnist")
```
The code snippet down below shows an accuracy test for the model we just trained.
```python
from hox import *
import utils

#Load model
model = Model.load("mnist")

#Upload mnist dataset
X, Y, x, y = utils.mnist()

#Accuracy tested on test10k data (x, y)
counter = 0
for i in range(len(x)):
    if np.argmax(model.forward(x[i])) == y[i]:
        counter +=1
print(str((counter*100)/len(y)) + "% accuracy")
```
