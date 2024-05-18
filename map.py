import plotly.graph_objects as go
import numpy as np
def create_map(df, selected_year_range, selected_species):
    start_year, end_year = selected_year_range
    if selected_species:
        df_filtered = df[(df['sampleYear'] >= start_year) & (df['sampleYear'] <= end_year) & (df['Species'] == selected_species)]
    else:
        df_filtered = df[(df['sampleYear'] >= start_year) & (df['sampleYear'] <= end_year)]
    location_counts = df_filtered.groupby(['Lat', 'Lon', 'LocationID']).size().reset_index(name='Total')

    max_marker_size = 20
    location_counts['MarkerSize'] = location_counts['Total'].clip(upper=max_marker_size)

    min_value = location_counts['Total'].min()
    max_value = location_counts['Total'].max()

    colors = ['#E57E25', '#D93E0F']
    fig = go.Figure()

    location_counts['LogTotal'] = np.log(location_counts['Total'])

    scatter = go.Scattermapbox(
    lat=location_counts['Lat'],
    lon=location_counts['Lon'],
    mode='markers',
    marker=dict(
        size=location_counts['LogTotal'] / max(location_counts['LogTotal']) * 20,
        color=location_counts['LogTotal'],
        colorscale='YlOrRd', 
        colorbar=dict(title='Logarithm'),
        opacity=0.7
    ),
    text='Fangort: ' + location_counts['LocationID'].astype(str) + ', Gefangene Lachse: ' + location_counts['Total'].astype(str) + ', Jahre: ' + str(start_year) + '-' + str(end_year) + (', Art: ' + selected_species if selected_species else '')
)


    fig.add_trace(scatter)

    avg_lat = location_counts['Lat'].mean()
    avg_lon = location_counts['Lon'].mean()


    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_accesstoken="pk.eyJ1IjoibWF4aW1pbGlhbnBhemVyIiwiYSI6ImNsdTJxMTM4NjB4aTQyam54bXpnNTBpbGYifQ.7eNGm_OaZxNMBbK_7tnOxw",
        mapbox_zoom=2.5,
        mapbox_center={"lat": avg_lat, "lon": avg_lon}, 
        width=1000,
        height=600
    )

    return fig