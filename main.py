# main.py
import pandas as pd
import logging
from functions import generate_email, has_special_chars

# Set up logging
logging.basicConfig(filename='computations.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    try:
        # Load the data
        df = pd.read_excel('TestFiles.xlsx')
        logging.info("Data loaded successfully")

        # Generate email addresses
        df['Email'] = df['Student Name'].apply(generate_email)
        logging.info("Email addresses generated")

        # Create separate lists for male and female students
        males = df[df['Gender'] == 'M']
        females = df[df['Gender'] == 'F']

        # Log the counts
        logging.info(f"Number of male students: {len(males)}")
        logging.info(f"Number of female students: {len(females)}")

        # Identify names with special characters
        special_char_names = df[df['Student Name'].apply(has_special_chars)]
        special_char_names.to_csv('special_char_names.csv', index=False)
        logging.info("Special character names identified and saved")

        # Save male and female lists
        males.to_csv('male_students.csv', index=False)
        females.to_csv('female_students.csv', index=False)
        logging.info("Male and female student lists saved")

        print("Processing complete. Check the log file for details.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()