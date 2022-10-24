import pandas as pd
from datetime import datetime

now = datetime.now()
today = now.strftime('%m월 %d일')



df = pd.read_excel('src/results/menu_list.xlsx', engine='openpyxl')
print(df.at[0, today])