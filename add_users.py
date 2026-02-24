import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

django.setup()

from authenticate.models import MyUser
from django.core.exceptions import ValidationError

def create_users_from_excel(excel_file):
    df = pd.read_excel(excel_file)

    for index, row in df.iterrows():
        username = row['Admission Number']
        password = 'apple123' 
        email = row['Email']
        department = row['Branch']  
        joined = row['year of joining']
        name = row['Name of the Student']

        if not username or not email or not name:
            print(f"Skipping row {index + 1} due to missing essential data.")
            continue

        if MyUser.objects.filter(username=username).exists():
            print(f"Skipping row {index + 1} as the username {username} already exists.")
            continue

        try:
            user = MyUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                name=name,
                user_type=MyUser.STUDENT,  
                department=department,
                joined=joined 
            )
            print(f"User {index+1} {name} created successfully.")
        except ValidationError as e:
            print(f"Error {index+1} creating user {name}: {e}")

        index +=1

if __name__ == '__main__':
    excel_file_path = 'Students_data.xlsx' 
    create_users_from_excel(excel_file_path)
