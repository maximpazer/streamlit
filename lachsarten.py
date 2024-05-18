import pandas as pd
import plotly.express as px

def create_pie_chart(df, selected_year_range):
    df_filtered = df[(df['sampleYear'] >= selected_year_range[0]) & (df['sampleYear'] <= selected_year_range[1])]
    start_year, end_year = selected_year_range

    species_counts = df_filtered['Species'].value_counts()

    species_df = pd.DataFrame({'Lachsart': species_counts.index, 'Anzahl': species_counts.values})

    fig = px.pie(species_df, values='Anzahl', names='Lachsart', 
                    title='Verteilung der Lachsspezien im Zeitraum {}-{}'.format(start_year, end_year),
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      texttemplate='<b>%{label}</b>: %{percent:.1%}')
    fig.update_layout(title_font_size=20, legend_title_font_size=16, legend_font_size=14)
    
    return fig
