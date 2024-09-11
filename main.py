import pandas as pd
import logging
from functions import generate_email, has_special_chars, compare_names
from auth import authenticate
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

#Setting up logging of the files
logging.basicConfig(filename='computations.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def upload_to_drive(file_path, file_name, credentials):
    try:
        #Builds the Google Drive service for uploading
        service = build('drive', 'v3', credentials=credentials)

        #uploads file to Drive
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, mimetype='text/csv')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        print(f"File {file_name} uploaded successfully. File ID: {file.get('id')}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")


def main():
    try:
        #loading the data from excel file
        df = pd.read_excel('TestFiles.xlsx')
        logging.info("Data loaded successfully")

        #generates email addresses
        df['Email'] = df['Student Name'].apply(generate_email)
        logging.info("Email addresses generated")

        #compare names for similarity
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                name1 = df.iloc[i]['Student Name']
                name2 = df.iloc[j]['Student Name']
                similarity_score = compare_names(name1, name2)

                if similarity_score > 0.8:  # Adjust the threshold for your needs
                    logging.info(f"Names {name1} and {name2} are similar with a score of {similarity_score:.2f}")

        #separates the male and female students
        males = df[df['Gender'] == 'M']
        females = df[df['Gender'] == 'F']

        #logs the counts
        logging.info(f"Number of male students: {len(males)}")
        logging.info(f"Number of female students: {len(females)}")

        #find names with special characters
        special_char_names = df[df['Student Name'].apply(has_special_chars)]
        special_char_names.to_csv('special_char_names.csv', index=False)
        special_char_names.to_csv('special_char_names.tsv', index=False)
        special_char_names.to_json('special_char_names.json', index=False)
        logging.info("Special character names identified and saved")

        #save the male and female lists
        males.to_csv('male_students.csv', index=False)
        males.to_csv('male_students.tsv', index=False)
        males.to_json('male_students.json', index=False)
        females.to_csv('female_students.csv', index=False)
        females.to_csv('female_students.tsv', index=False)
        females.to_json('female_students.json', index=False)
        logging.info("Male and female student lists saved")

        #authenticates the Google Drive API
        creds = authenticate()

        #backs up files to Google Drive
        upload_to_drive('male_students.csv', 'male_students.csv', creds)
        upload_to_drive('male_students.tsv', 'male_students.tsv', creds)
        upload_to_drive('male_students.json', 'male_students.json', creds)
        upload_to_drive('female_students.csv', 'female_students.csv', creds)
        upload_to_drive('female_students.tsv', 'female_students.tsv', creds)
        upload_to_drive('female_students.json', 'female_students.json', creds)
        upload_to_drive('special_char_names.csv', 'special_char_names.csv', creds)
        upload_to_drive('special_char_names.tsv', 'special_char_names.tsv', creds)
        upload_to_drive('special_char_names.json', 'special_char_names.json', creds)

        print("Processing complete. Check the log file and Google Drive for details.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
