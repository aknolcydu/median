#install imported packages + pip install xlwt
import requests
import pandas as pd
import io
import numpy as np
response = requests.get("https://raw.githubusercontent.com/tarikkranda/pi_datasets/main/country_vaccination_stats.csv")
urldata=response.content
data=pd.read_csv(io.StringIO(urldata.decode('utf-8')))
countries=data.groupby(['country']).count().reset_index()
results=list()
for item in countries['country']:
    country = data.loc[data['country'] == item]
    default_value=0
    for vacc_value in country['daily_vaccinations']:
        if pd.isna(vacc_value):
            continue
        elif default_value==0:
            default_value=vacc_value
        elif vacc_value<default_value:
            default_value=vacc_value
    country = country.replace(np.nan, default_value)
    vaccinations = sorted(country['daily_vaccinations'].tolist(), key = lambda x:float(x))
    if len(vaccinations) % 2 == 0:
        index=len(vaccinations) / 2
        res = (vaccinations[int(index)]+vaccinations[int(index)-1]) / 2
    else:
        index = (len(vaccinations) - 1) / 2
        res = vaccinations[int(index)]
    lst = [item,res]
    results.append(lst)
df = pd.DataFrame(results, columns =['country', 'median'])
df = df.sort_values(by=['median'], ascending=False).head(3)
print(df)





