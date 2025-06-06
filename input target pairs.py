import tiktoken  # Library for tokenization using OpenAI's encoding schemes
import torch  #to import dataloader and dataset
from torch.utils.data import DataLoader, Dataset

# Define a custom PyTorch Dataset class for tokenizing text
class token(Dataset):
    def __init__(self, txt, max_length=3, stride=1):
        self.in_l = []   # List to hold input token sequences
        self.tar_l = []  # List to hold target token sequences (next tokens)

        k = tiktoken.get_encoding("gpt2")  # Get GPT-2 encoding
        l = k.encode(txt)  # Encode the input text into token IDs
        print(l)  # Print encoded token IDs for reference

        # Create sliding windows of input-target pairs
        for i in range(0, len(l) - max_length, stride):
            q = l[i:i + max_length]           # Input sequence of length max_length
            p = l[i + 1:i + max_length + 1]   # Target sequence (next tokens)
            self.in_l.append(torch.tensor(q))  # Convert input to tensor and store
            self.tar_l.append(torch.tensor(p)) # Convert target to tensor and store

    def __len__(self):
        # Return number of input-target pairs
        return len(self.tar_l)

    def __getitem__(self, idx):
        # Return input and target pair at a specific index
        return self.in_l[idx], self.tar_l[idx]

# Wrapper function to create a DataLoader from text
def dataloader(txt, batch_size=2, max_length=3, stride=1, shuffle=False, drop_last=False, num_workers=0):
    tk = token(txt, max_length=max_length, stride=stride)  # Create dataset object
    dataloader = DataLoader(
        tk,
        batch_size=batch_size,
        shuffle=shuffle,         # Whether to shuffle data
        drop_last=drop_last,     # Drop last batch if it's smaller than batch_size
        num_workers=num_workers  # Number of subprocesses to use for data loading
    )
    return dataloader

# Prompt user to enter input text
txt = input("Enter the text: ")

# Create a DataLoader from the input text
data = dataloader(
    txt,
    batch_size=2,
    max_length=3,
    stride=1,
    shuffle=False,
    drop_last=False,
    num_workers=0
)

# Iterate through the DataLoader and print input-target pairs
for batch_size, (in_l, tar_l) in enumerate(data):
    print(batch_size + 1)  # Print batch number
    print(in_l)            # Print input sequences in the batch
    print(tar_l)           # Print target sequences in the batch