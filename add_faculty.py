import os
import django
import pandas as pd

# Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

# Setup Django
django.setup()

from authenticate.models import MyUser
import pandas as pd

def create_users_from_excel(excel_file):
    df = pd.read_excel(excel_file)

    for index, row in df.iterrows():
        username = row['Faculty ID']
        password = row['Password']
        email = row['Email']
        name = row['Name of the Faculty']
        department = row['Department']
        joined = row['joined']

        if not username or not email or not name:
            print(f"Skipping row {index + 1} due to missing essential data.")
            continue

        if MyUser.objects.filter(username=username).exists():
            print(f"Skipping row {index + 1} as the username {username} already exists.")
            continue

        # Create user using the data from the Excel file
        try:
            user = MyUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                name=name,
                user_type=MyUser.FACULTY,  
                department=department,
                joined=joined 
            )
            print(f"User {index+1} {name} created successfully.")
        except ValidationError as e:
            print(f"Error {index+1} creating user {name}: {e}")

        index +=1

if __name__ == '__main__':
    excel_file_path = 'Faculty_data.xlsx' 
    create_users_from_excel(excel_file_path)
