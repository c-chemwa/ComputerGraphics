import pandas as pd
from functions import generate_email, has_special_chars
from transformers import AutoModel, AutoTokenizer
import torch
import json

# Load the data
df = pd.read_excel('TestFiles.xlsx')

#Application of the email generation function
df['Email'] = df['Student Name'].apply(generate_email)

#Saving the unique character names to a log file
special_char_names = df[df['Student Name'].apply(has_special_chars)]
special_char_names.to_csv('logs/special_char_names.log', index=False)

#For the different genders, we save them to different log files.
males = df[df['Gender'] == 'Male']
females = df[df['Gender'] == 'Female']

males.to_csv('output/male_students.csv', index=False)
females.to_csv('output/female_students.csv', index=False)

#Logs the counts of males and females
with open('logs/gender_counts.log', 'w') as log_file:
    log_file.write(f"Male students: {len(males)}\n")
    log_file.write(f"Female students: {len(females)}\n")

#calculates similarities with the LaBSE model
def get_embeddings(names):
    inputs = tokenizer(names, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    return outputs.pooler_output

male_names = males['Student Name'].tolist()
female_names = females['Student Name'].tolist()

male_embeddings = get_embeddings(male_names)
female_embeddings = get_embeddings(female_names)

similarities = torch.mm(male_embeddings, female_embeddings.T).cpu().numpy()

#Filters results with at least 50% and saves
similar_pairs = []
for i, male_name in enumerate(male_names):
    for j, female_name in enumerate(female_names):
        if similarities[i, j] > 0.5:
            similar_pairs.append({
                'male_name': male_name,
                'female_name': female_name,
                'similarity': similarities[i, j].item()
            })



with open('output/similarity_results.json', 'w') as f:
    json.dump(similar_pairs, f, indent=4)


model_name = "sentence-transformers/LaBSE"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

#Merge male and female dataframes
combined_df = pd.concat([males, females]).sample(frac=1).reset_index(drop=True)

#Saves the combined dataframes as json and jsonl
combined_df.to_json('output/combined.json', orient='records', indent=4)
combined_df.to_json('output/combined.jsonl', orient='records', lines=True)
