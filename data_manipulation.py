import pandas as pd
import numpy as np
from sklearn import preprocessing


def clean_input_data(data):
    df = pd.DataFrame(data)
    for column_name, manga in df.iterrows():
        if manga["English Title"] == "Unknown":
            df.loc[column_name, "English Title"] = manga["Synonims Titles"]
    df.drop(["Synonims Titles"], axis=1, inplace=True)

    x = df.select_dtypes(include=[np.number])
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_num = pd.DataFrame(x_scaled)
    df["Score"] = df_num[0]
    df["Popularity"] = [1 - x for x in df_num[1]]
    df["Favorites"] = df_num[2]

    df = df.rename(columns={"English Title": "English_Title", "Manga URL": "Manga_URL"})
    df = df.drop(df[df.English_Title == "Unknown"].index)
    return df
