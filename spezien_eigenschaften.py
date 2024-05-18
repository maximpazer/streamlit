def calculate_metrics(df,selected_year_range, selected_species):
    if selected_species is None:
        df_filtered = df[(df['sampleYear'] >= selected_year_range[0]) & (df['sampleYear'] <= selected_year_range[1])]
    else:
        df_filtered = df[(df['sampleYear'] >= selected_year_range[0]) & (df['sampleYear'] <= selected_year_range[1])]
        df_filtered = df_filtered[df_filtered['Species'] == selected_species]
    
    df_filtered = df_filtered[df_filtered['Salt.Water.Age'] > 1]
    
    average_length = int(df_filtered['Length'].mean())
    average_weight = df_filtered['Weight'].mean()
    average_age = df_filtered['Salt.Water.Age'].mean()
    female_count = df_filtered[df_filtered['Sex'] == 'female'].shape[0]
    male_count = df_filtered[df_filtered['Sex'] == 'male'].shape[0]

    sex_ratio = round(female_count / male_count, 2) if male_count != 0 else 0
    fish_count = df_filtered.shape[0]

    
    return average_length, average_weight, average_age, female_count, male_count, sex_ratio, fish_count
