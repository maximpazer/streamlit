import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_ratio_chart(df, values, selected_species):
    if selected_species is None:
        df_filtered = df
        species_label = "alle Spezies"
    else:
        df_filtered = df[df['Species'] == selected_species]
        species_label = f"{selected_species}"

    verlauf_Sex = df_filtered.groupby(['sampleYear', 'Sex']).size().unstack(fill_value=0)
    verlauf_Sex_filtered = verlauf_Sex.loc[values[0]:values[1]]

    #Verhältnis von Männchen zu Weibchen
    verhaeltnis_male_female = verlauf_Sex_filtered['male'] / verlauf_Sex_filtered['female']


    chart_df = pd.DataFrame({
        'Jahr': verhaeltnis_male_female.index,
        'Verhältnis': verhaeltnis_male_female.values
    })

    # Berechnung der Abweichungen von 1
    chart_df['Männlich'] = chart_df['Verhältnis'] - 1
    chart_df['Weiblich'] = 1 - chart_df['Verhältnis']

    fig_ratio = go.Figure(data=[
        go.Bar(name='Männlich', x=chart_df['Jahr'], y=chart_df['Männlich'], base=1, marker_color='blue'),
        go.Bar(name='Weiblich', x=chart_df['Jahr'], y=chart_df['Weiblich'], base=1, marker_color='pink')
    ])

    # Layoutanpassung
    fig_ratio.update_layout(
        autosize=True,
        barmode='relative',
        title_text=f'Verhältnis von männlich zu weiblich über die Jahre ({species_label})',
        xaxis_title='Jahr',
        yaxis_title='Verhältnis (Männlich/Weiblich)',
        yaxis=dict(tickformat='.2f'),
        showlegend=True
    )

    return fig_ratio



def fig_salt_water_age(df,values, selected_species):

    if selected_species is None:
        df_filtered = df
        species_label = "alle Spezies"
    else:
        df_filtered = df[df['Species'] == selected_species]
        species_label = f"{selected_species}"

    df_filtered = df_filtered[(df_filtered['Salt.Water.Age'] != -1) & (df_filtered['Salt.Water.Age'] != 0)]

    verlauf_salt_water_age = df_filtered.groupby(['sampleYear', 'Salt.Water.Age']).size().unstack(fill_value=0)
    verlauf_salt_water_age_filtered = verlauf_salt_water_age.loc[values[0]:values[1]]

    verlauf_salt_water_age_avg = verlauf_salt_water_age_filtered.rolling(window=3).mean()

    fig_salt_water_age = px.line(verlauf_salt_water_age_avg, labels={'index': 'Jahr', 'value': 'Durchschnittliches Salt Water Age'}, 
                                 title=f'Salt Water Age über 3 Jahre ({species_label})')
    fig_salt_water_age.update_layout(
         autosize=True,
    )
    return fig_salt_water_age


