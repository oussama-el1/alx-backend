import requests
import pandas as pd

# Step 1: Download the CSV file
url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2020/5/7d3576d97e7560ae85135cc214ffe2b3412c51d7.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240523%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240523T162339Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=41f6b525e87271b9ff31e1df18ba57e8f729afe29179ea553793aa97e7887706"

response = requests.get(url)
response.raise_for_status()


with open('downloaded_file.csv', 'wb') as file:
    file.write(response.content)

df = pd.read_csv('downloaded_file.csv')

print(df.head())

df.to_csv('saved_file.csv', index=False)
