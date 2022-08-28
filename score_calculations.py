def calculate_similarity_score(df, selected):
    mask = df['English_Title'].values == selected
    df_new = df[mask]
    selected_dict = df_new.transpose().to_dict().get(df_new.index[0])

    list_of_potential_recommendations, score_current = [], []
    for column_name, manga in df.iterrows():
        if manga["English_Title"] != "Unknown":
            value = abs(manga["Score"] - selected_dict.get("Score"))
            value += abs(manga["Popularity"] - selected_dict.get("Popularity"))
            value += abs(manga["Favorites"] - selected_dict.get("Favorites"))
            value = 1 - (value / 3)
            x = list(set(selected_dict.get("Genres").replace("'", "")[1:-1].split(", ")))
            y = list(set(manga["Genres"].replace("'", "")[1:-1].split(", ")))
            common_genre = list(set(x) & set(y))
            genre_value = len(common_genre) + 1
            value += genre_value / 2
            value *= 2
            list_of_potential_recommendations.append([manga["English_Title"], value])
            score_current.append(value)
        else:
            score_current.append(0)

    return list_of_potential_recommendations, score_current
