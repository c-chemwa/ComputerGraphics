import pandas as pd
from functions import generate_email

# Load the data
df = pd.read_excel('TestFiles.xlsx')
df['Email'] = df['Student Name'].apply(generate_email)
