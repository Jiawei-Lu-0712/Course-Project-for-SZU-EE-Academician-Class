import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, set_seed
import matplotlib.pyplot as plt
from torch.nn import Transformer
from tqdm import tqdm

# Set seed for reproducibility
np.random.seed(1)
torch.manual_seed(1)
set_seed(1)

# Load dataset
splits = {
    'test': 'eng-cmn/test-00000-of-00001.parquet',
    'train': 'eng-cmn/train-00000-of-00001.parquet'
}
df_train = pd.read_parquet("hf://datasets/AlienKevin/yue-cmn-eng/" + splits["train"])
df_test = pd.read_parquet("hf://datasets/AlienKevin/yue-cmn-eng/" + splits["test"])

# Use a pretrained tokenizer
src_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tgt_tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

class TranslationDataset(Dataset):
    def __init__(self, df):
        self.src_texts = df['translation'].apply(lambda x: x['eng']).tolist()
        self.tgt_texts = df['translation'].apply(lambda x: x['cmn']).tolist()

    def __len__(self):
        return len(self.src_texts)

    def __getitem__(self, idx):
        src = src_tokenizer(self.src_texts[idx], return_tensors='pt', padding='max_length', max_length=32, truncation=True)
        tgt = tgt_tokenizer(self.tgt_texts[idx], return_tensors='pt', padding='max_length', max_length=32, truncation=True)
        return src['input_ids'].squeeze(), tgt['input_ids'].squeeze()

train_dataset = TranslationDataset(df_train.head(1000))  # limit for fast training
test_dataset = TranslationDataset(df_test.head(200))
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# Model definition
class SimpleTransformer(nn.Module):
    def __init__(self, vocab_size_src, vocab_size_tgt, d_model=256, nhead=4, num_layers=3):
        super().__init__()
        self.encoder_embedding = nn.Embedding(vocab_size_src, d_model)
        self.decoder_embedding = nn.Embedding(vocab_size_tgt, d_model)
        self.transformer = Transformer(d_model=d_model, nhead=nhead, num_encoder_layers=num_layers, num_decoder_layers=num_layers)
        self.fc_out = nn.Linear(d_model, vocab_size_tgt)

    def forward(self, src, tgt):
        src = self.encoder_embedding(src).permute(1, 0, 2)
        tgt = self.decoder_embedding(tgt).permute(1, 0, 2)
        output = self.transformer(src, tgt)
        return self.fc_out(output).permute(1, 0, 2)

model = SimpleTransformer(len(src_tokenizer), len(tgt_tokenizer)).cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss(ignore_index=0)

# Training loop
losses = []
for epoch in range(10):
    model.train()
    epoch_loss = 0
    for src, tgt in tqdm(train_loader):
        src, tgt = src.cuda(), tgt.cuda()
        tgt_input = tgt[:, :-1]
        tgt_output = tgt[:, 1:]

        output = model(src, tgt_input)
        output = output.reshape(-1, output.shape[-1])
        tgt_output = tgt_output.reshape(-1)

        loss = criterion(output, tgt_output)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    avg_loss = epoch_loss / len(train_loader)
    losses.append(avg_loss)
    print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")

# Plot training loss
plt.plot(losses)
plt.title("Training Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig("training_loss.png")
plt.close()

# Save attention from one encoder layer
def visualize_feature_map(model, src_sample):
    model.eval()
    src_sample = src_sample.unsqueeze(0).cuda()
    with torch.no_grad():
        emb = model.encoder_embedding(src_sample).permute(1, 0, 2)
        att_map = model.transformer.encoder.layers[0].self_attn(emb, emb, emb)[1]
    att_map = att_map.squeeze().cpu().numpy()
    plt.imshow(att_map, cmap='viridis')
    plt.title("Encoder Attention Map")
    plt.colorbar()
    plt.savefig("attention_map.png")
    plt.close()

# Visualize one feature map
visualize_feature_map(model, train_dataset[0][0])
