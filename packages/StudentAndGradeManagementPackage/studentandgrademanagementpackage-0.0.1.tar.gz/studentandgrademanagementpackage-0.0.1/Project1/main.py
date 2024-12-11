from data_access_analysis.data_access import DataAccess
from data_access_analysis.data_analysis import DataAnalysis
from menu import *
import sys
from pathlib import Path

# Add the root directory (Project1) to the system path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def main_menu():
    print("***** Welcome to the System *****")
    print("1: Student Login")
    print("2: Teacher Login")
    print("0: Exit")

if __name__ == "__main__":
    # Import initial user data
    credentials_path = "initial_login_data.csv"  # Path to the CSV file for student and teacher login
    DataAccess.import_user_credentials(credentials_path)
    
    # Import the default data uploaded by the teacher
    default_teacher_data_path = "teacher_upload_full_data.csv"  # Default path for the teacher's uploaded file
    try:
        DataAccess.import_all_data_from_csv(default_teacher_data_path)
        print(f"Default data imported successfully from {default_teacher_data_path}")
    except Exception as e:
        print(f"Failed to import default data: {e}")
    
    # Start the login interface
    login()