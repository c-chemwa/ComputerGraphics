import re
from transformers import AutoModel, AutoTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity

def generate_email(name):
    parts = re.findall(r'\w+', name.lower())
    if len(parts) >= 2:
        email = f"{parts[0][0]}{parts[-1]}@gmail.com"
    else:
        email = f"{parts[0]}@gmail.com"
    return email

def has_special_chars(name):
    return bool(re.search(r'[^a-zA-Z\s]', name))

# Load LaBSE model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/LaBSE")
model = AutoModel.from_pretrained("sentence-transformers/LaBSE")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).pooler_output
    return embeddings.numpy()

def compare_names(name1, name2):
    embedding1 = get_embedding(name1)
    embedding2 = get_embedding(name2)
    similarity = cosine_similarity(embedding1, embedding2)[0][0]
    return similarity