import plotly.express as px

def fig_laengen(df,values, selected_species):

    if selected_species is None:
        df_filtered = df
        species_label = "alle Spezies"
    else:
        df_filtered = df[df['Species'] == selected_species]
        species_label = f"{selected_species}"

    verlauf_laengen = df_filtered.groupby('sampleYear')['Length'].mean()

    jahre_alle_3_jahre = list(range(int(verlauf_laengen.index.min()), int(verlauf_laengen.index.max()) + 1, 3))

    durchschnittliche_laengen_alle_3_jahre = verlauf_laengen[verlauf_laengen.index.isin(jahre_alle_3_jahre)]

    durchschnittliche_laengen_alle_3_jahre_filtered = durchschnittliche_laengen_alle_3_jahre.loc[values[0]:values[1]]

    fig_laengen = px.line(x=durchschnittliche_laengen_alle_3_jahre_filtered.index, y=durchschnittliche_laengen_alle_3_jahre_filtered.values,
                          labels={'x': 'Jahr', 'y': 'Durchschnittliche Länge'}, title=f'Verlauf der durchschnittlichen Längen alle 3 Jahre ({species_label})')
    fig_laengen.update_layout(
         autosize=True,
    )
    return fig_laengen

def fig_gewichte(df,values, selected_species):

    if selected_species is None:
        df_filtered = df
        species_label = "alle Spezies"
    else:
        df_filtered = df[df['Species'] == selected_species]
        species_label = f"{selected_species}"
    
    verlauf_gewichte = df_filtered.groupby('sampleYear')['Weight'].mean()

    jahre_alle_3_jahre = list(range(int(verlauf_gewichte.index.min()), int(verlauf_gewichte.index.max()) + 1, 3))

    durchschnittliche_gewichte_alle_3_jahre = verlauf_gewichte[verlauf_gewichte.index.isin(jahre_alle_3_jahre)]

    durchschnittliche_gewichte_alle_3_jahre_filtered = durchschnittliche_gewichte_alle_3_jahre.loc[values[0]:values[1]]

    fig_gewichte = px.line(x=durchschnittliche_gewichte_alle_3_jahre_filtered.index, y=durchschnittliche_gewichte_alle_3_jahre_filtered.values,
                           labels={'x': 'Jahr', 'y': 'Durchschnittliches Gewicht'}, title=f'Verlauf der durchschnittlichen Gewichte alle 3 Jahre ({species_label})')
    fig_gewichte.update_layout(
        autosize=True,
    )
    return fig_gewichte
