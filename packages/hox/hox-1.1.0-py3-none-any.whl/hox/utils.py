from hox import SGD
from tqdm import tqdm
import os
import urllib.request
import gzip
import shutil
import numpy as np

#Standard training loop with mini-batch support
def train(model, X, Y, **options):
    #Set variables for training
    rate, batch_size, epochs = options.get("rate", .5), options.get("batch_size", 16), options.get("epochs", 1)
    loss_format = lambda l: f"{l:.4f}"
    data_len = len(Y)
    loss_update_frequency = 50 #updates per epoch

    #Define optimizer
    optim = SGD(model, rate)

    #Training loop
    for epoch in range(epochs):
        pbar = tqdm(range(0, len(X), batch_size), desc="Epoch " + str(epoch), bar_format='{l_bar}{bar}|[{elapsed}<{remaining}]{postfix}')
        loss, loss_counter = 0, 0
        for batch_start in pbar:
            batch_end = min(batch_start + batch_size, len(X))
            optim.zero_grad()

            for index in range(batch_start, batch_end):
                output = model.run(X[index])
                if index % (data_len/loss_update_frequency) == 0:
                    loss_counter += 1
                    loss += abs(np.mean(Y[index] - output))
                    pbar.set_postfix(loss=loss_format(loss / loss_counter))
                optim.grad(Y[index])

            optim.step()

    model.save("mnist")
    print("Training completed.")

#Load mnist dataset
def mnist():
    print("Loading MNIST dataset...")
    print("Checking...")
    dataset_dir="./MNIST"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    base_url = "https://storage.googleapis.com/cvdf-datasets/mnist/"
    files = ["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
             "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]
    missing_files = []
    for file in files:
        file_path = os.path.join(dataset_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    if missing_files:
        print("Downloading missing files...")
        for file in missing_files:
            print(f"Downloading {file}...")
            url = base_url + file
            urllib.request.urlretrieve(url, os.path.join(dataset_dir, file))
            print("Download completed.")
    else:
        print("All files are already downloaded.")
    print("Preparing dataset...")
    X = (np.frombuffer(gzip.open("MNIST/train-images-idx3-ubyte.gz", "rb").read(), dtype=np.uint8)[16:].reshape((-1, 784)) / 255).astype(np.float32)
    Y = (np.eye(10)[np.frombuffer(gzip.open("MNIST/train-labels-idx1-ubyte.gz", "rb").read(), dtype=np.uint8)[8:]]).astype(np.float32)
    x = np.frombuffer(gzip.open("MNIST/t10k-images-idx3-ubyte.gz", "rb").read(), dtype=np.uint8)[16:].reshape((-1, 784)) / 255
    y = np.frombuffer(gzip.open("MNIST/t10k-labels-idx1-ubyte.gz", "rb").read(), dtype=np.uint8)[8:]
    print("MNIST dataset loaded.")
    return X, Y, x, y
