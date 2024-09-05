import pandas as pd
import logging
from functions import generate_email, has_special_chars
from auth import authenticate
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up logging
logging.basicConfig(filename='computations.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def upload_to_drive(file_path, file_name, credentials):
    try:
        # Build the Google Drive service
        service = build('drive', 'v3', credentials=credentials)

        # Upload file to Drive
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, mimetype='text/csv')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        print(f"File {file_name} uploaded successfully. File ID: {file.get('id')}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")


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

        # Authenticate Google Drive API
        creds = authenticate()

        # Backup files to Google Drive
        upload_to_drive('male_students.csv', 'male_students.csv', creds)
        upload_to_drive('female_students.csv', 'female_students.csv', creds)
        upload_to_drive('special_char_names.csv', 'special_char_names.csv', creds)

        print("Processing complete. Check the log file and Google Drive for details.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
