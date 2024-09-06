# ComputerGraphics

# Student Data Processor and Backup to Google Drive

## Overview

This project processes student data from an Excel file, generating email addresses, separating students by gender, identifying names with special characters, and backing up important data to Google Drive. The processed data is saved into CSV files and securely uploaded to Google Drive using the Google Drive API for backup.

## Features

- **Email Generation**: Automatically generates email addresses for students based on their names.
- **Gender-Based Separation**: Separates student data into male and female categories.
- **Special Character Identification**: Identifies students whose names contain special characters.
- **Google Drive Backup**: Automatically uploads the processed files (male, female, and special character lists) to Google Drive for safe storage.

## Project Structure

The project consists of the following core components:

### 1. `main.py`

This is the main script that orchestrates the processing and backup of student data. It:

- Loads student data from an Excel file.
- Generates email addresses using the `generate_email` function.
- Separates students by gender and saves male and female student lists as CSV files.
- Identifies names with special characters and saves this data as a separate CSV file.
- Authenticates with Google Drive and uploads the CSV files for backup.

### 2. `functions.py`

This file contains helper functions for the project:

- **`generate_email(name)`**: Generates an email address using the student's name. If the name has multiple parts, the email is formatted as the first letter of the first name followed by the full last name (e.g., `jdoe@gmail.com`).
- **`has_special_chars(name)`**: Checks if a student name contains any special characters and returns a boolean result.

### 3. `auth.py`

Handles authentication and authorization with Google Drive using OAuth 2.0. The first time the script is run, it will open a browser for the user to log in and authorize the app to access Google Drive. After authorization, a token is saved locally for future use.

### 4. `constraints.py`

Contains configuration constraints used throughout the project. These include:

- **`MAX_EMAIL_LENGTH`**: Defines the maximum allowable length for email addresses.
- **`ALLOWED_EMAIL_CHARS`**: Specifies which characters are allowed in generated email addresses.

### 5. Input File

- **`TestFiles.xlsx`**: The Excel file containing the student data. The following columns are expected:
  - **Student Name**: The full name of the student.
  - **Gender**: The gender of the student (e.g., "M" for male, "F" for female).

## How It Works

### Step 1: Data Processing

1. **Load Data**: The script reads the Excel file `TestFiles.xlsx` containing student information.
2. **Email Generation**: For each student, an email address is generated based on their name.
3. **Gender-Based Separation**: Students are categorized by gender (male or female) into separate CSV files: `male_students.csv` and `female_students.csv`.
4. **Special Character Identification**: Students whose names contain special characters are identified, and this information is saved in `special_char_names.csv`.

### Step 2: Google Drive Backup

1. **Authentication**: The Google Drive API is used to upload the CSV files for backup. Authentication is handled via OAuth 2.0.
2. **File Upload**: After authentication, the processed CSV files are uploaded to Google Drive.

## Requirements

### Python Packages

The project requires the following Python packages:

- `pandas`: For data processing and manipulation.
- `google-api-python-client`: To interact with Google Drive API.
- `google-auth-httplib2`: For OAuth 2.0 authorization.
- `google-auth-oauthlib`: To handle OAuth 2.0 authorization flow.
- `re`: To handle regular expressions for email generation and special character identification.
- `logging`: To log the details of the script's execution.

Install these dependencies by running:

```bash
pip install pandas google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Google Drive API Setup

To enable Google Drive API access, follow these steps:

1. Go to the [Google Cloud Console](https://console.developers.google.com/).
2. Create a new project (or select an existing one).
3. Enable the **Google Drive API**.
4. Create OAuth 2.0 credentials by choosing the "Desktop App" option.
5. Download the `credentials.json` file and place it in the root of this project.

## How to Run

1. Clone or download this repository.
2. Make sure you have all the required dependencies installed.
3. Place the `TestFiles.xlsx` file with student data in the project directory.
4. Add the `credentials.json` file from Google Cloud Console to the root directory of this project.
5. Run the script using:

```bash
python main.py
```

The first time you run the script, it will open a browser asking you to log in with your Google account and authorize access to Google Drive. Once authenticated, the token will be saved locally, and the script will upload the CSV files to your Google Drive.

## Logging

All actions performed by the script, such as loading data, generating emails, separating genders, and uploading files, are logged in the `computations.log` file. If an error occurs, it will be logged and displayed in the console.

## Output

The following CSV files are generated as output:
- **`male_students.csv`**: List of male students.
- **`female_students.csv`**: List of female students.
- **`special_char_names.csv`**: List of students whose names contain special characters.

These files will also be uploaded to your Google Drive for safe backup.

## Notes

- The script assumes that all students have at least one name in the "Student Name" column. If a name is missing or incomplete, the generated email may not follow the expected format.
- Only names with Latin alphabet characters are processed for email generation. Any special characters in names will be flagged and saved in a separate file.
- Google Drive upload will only work if the correct OAuth 2.0 credentials are provided and the user grants access during the authorization step.

## License

This project is licensed under the MIT License.
