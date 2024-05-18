import plotly.express as px

def create_bar_chart(df, year_range):
    start_year, end_year = year_range
    
    df_filtered = df[(df['sampleYear'] >= start_year) & (df['sampleYear'] <= end_year)]
    
    min_catches = 10

    species_method_counts = df_filtered.groupby(['Species', 'Gear']).size().reset_index(name='Total_Catches')

    species_method_counts_filtered = species_method_counts[species_method_counts['Total_Catches'] >= min_catches]

    fig = px.bar(species_method_counts_filtered, x='Species', y='Total_Catches', color='Gear',
                 title='Fangmethoden pro Lachsspezies im Zeitraum {}-{}'.format(start_year, end_year),
                 labels={'Species': 'Lachsspezies', 'Total_Catches': 'Anzahl der gefangenen Lachse', 'Gear': 'Fangmethode'})
    fig.update_xaxes(title='Lachsspezies')
    fig.update_yaxes(title='Anzahl der gefangenen Lachse')
    
    return fig


def create_sunburst_chart(df, selected_year_range, selected_species, min_catches):
    start_year, end_year = selected_year_range
    
    df_filtered = df[(df['sampleYear'] >= start_year) & (df['sampleYear'] <= end_year)]
    if selected_species:
        df_filtered = df_filtered[df_filtered['Species'] == selected_species]
    
    species_method_counts = df_filtered.groupby(['Species', 'Gear']).size().reset_index(name='Total_Catches')

    species_method_counts_filtered = species_method_counts[species_method_counts['Total_Catches'] >= min_catches]

    fig = px.sunburst(species_method_counts_filtered, path=['Species', 'Gear'], values='Total_Catches',
                      title=f'Fangmethoden pro Lachsspezies im Zeitraum {start_year}-{end_year}',
                      labels={'Species': 'Lachsspezies', 'Total_Catches': 'Anzahl der gefangenen Lachse', 'Gear': 'Fangmethode'})
    
    return fig

