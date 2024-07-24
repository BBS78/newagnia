import pandas as pd
from tinydb import TinyDB, Query

mdb = TinyDB('./json/marksdb.json', encoding='utf-8')
User = Query()

json_data = mdb.search(User.user_id == "<@996353781300215868>")

data = [record for record in json_data]
df = pd.DataFrame(data).reset_index()
df = df.rename(columns={'index': 'ID'})

df.to_excel('output.xlsx', index=False)

