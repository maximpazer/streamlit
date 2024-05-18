import pandas as pd
import plotly.express as px
import streamlit as st

from spezien_eigenschaften import calculate_metrics

from map import create_map
from length_weight_3years import fig_gewichte,fig_laengen
from age_sex_3years import create_ratio_chart,fig_salt_water_age
from salmon.submission.map import create_map
from fangarten import create_sunburst_chart
from lachsarten import create_pie_chart

st.set_page_config(page_title="Alaskas Lachse", page_icon="🦈",
                   layout="wide")



# Laden und Bereitstellen des Datensatzes
@st.cache_data
def load_data():
    df = pd.read_csv("./dashboard_data.csv")
    df['Weight'] = df['Weight'] * 0.453592

    return df
df = load_data()

st.markdown("<h1 style='text-align: center; color: #FFFFF; font-size: 42px;'>A L A S K A:</h1> <h2 style='text-align: center';> eine bedrohte Lachspopulation? </h2>", unsafe_allow_html=True)
st.divider()

col1,col2 = st.columns(2,gap="large")
with col1:
    st.header("Der Lachs")
    st.info("""
**Über den Lachs:**
Lachse sind faszinierende Wanderfische, die für ihre epischen Wanderungen von Meeresgewässern zu ihren Laichgründen in den Flüssen bekannt sind. 

**Die Herausforderungen für den Lachs:**
Besonders in Alaska sind die Daten über Lachse von entscheidender Bedeutung. Die Region beherbergt einige der letzten intakten Lachslebensräume, was sie zu einem wichtigen Schauplatz für die Erhaltung von Lachsbeständen macht.

**Ziel des Dashboards:**
Dieses Dashboard zielt darauf ab, die Entwicklung der Lachspopulationen aufzuzeigen. Es bietet Einblicke in die verschiedenen Metriken, die für das Verständnis der Trends der Lachspopulationen in Alaska wichtig sind.
""")
with col2:
    st.header("Lachsarten ")
    col3,col4,col5,col6,col7 = st.columns(5)
    with col3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/d/d8/Chinook_Salmon_Adult_Male.jpg", "Chinook")

    with col4:
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Dog_Salmon_Breeding_Male.jpg", "Chum")

    with col5:
        st.image("https://s3.animalia.bio/animals/photos/full/original/coho-salmon-adult-male.webp","Coho")

    with col6:
        st.image("https://upload.wikimedia.org/wikipedia/commons/c/c2/Humpback_Salmon_Adult_Male.jpg", "Pink")
    with col7:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Oncorhynchus_nerka.jpg/300px-Oncorhynchus_nerka.jpg","Sockeye")

    # Button --> all species
    if "all_button_clicked" not in st.session_state:
        st.session_state.all_button_clicked = False
    if st.button("All",use_container_width=True):
        st.session_state.all_button_clicked = True

    # Slider --> species selection
    species_order = ["chinook", "chum", "coho", "pink", "sockeye"]
    selected_species = st.select_slider("Select a species", options=species_order)

    if selected_species != st.session_state.get("selected_species", None):
        st.session_state.all_button_clicked = False
        st.session_state.selected_species = selected_species

    if st.session_state.all_button_clicked:
        selected_species = None

    species_images = {
    "chinook": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Chinook_Salmon_Adult_Male.jpg",
    "chum": "https://upload.wikimedia.org/wikipedia/commons/7/71/Dog_Salmon_Breeding_Male.jpg",
    "coho": "https://s3.animalia.bio/animals/photos/full/original/coho-salmon-adult-male.webp",
    "pink": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Humpback_Salmon_Adult_Male.jpg",
    "sockeye": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Oncorhynchus_nerka.jpg/300px-Oncorhynchus_nerka.jpg",
    "all": "https://i0.wp.com/kenrand.co/wp-content/uploads/2019/03/pac-sam-species_titlecrop.gif?resize=920%2C431",
    }


st.divider()

# Sidebar 
selected_species = st.sidebar.selectbox('Select a species (sidebar)', ['All species'] + list(df['Species'].unique()))
if selected_species == 'All species':
    selected_species = None

values = st.sidebar.slider('Select a range of years (sidebar)', 1960, 2016, (1960, 2016))
min_value = int(values[0])
max_value = int(values[1])

# Df filtern nach Jahr
df_filtered = df[(df['sampleYear'] >= min_value) & (df['sampleYear'] <= max_value)]

# Metriken berechnen 
average_length, average_weight, average_age, female_count, male_count, sex_ratio, fish_count = calculate_metrics(df_filtered, values, selected_species)
entire_year_range = (df['sampleYear'].min(), df['sampleYear'].max())
all_length = int(calculate_metrics(df, entire_year_range, selected_species)[0])
all_weight = round(calculate_metrics(df, entire_year_range, selected_species)[1],2)
all_age = round(calculate_metrics(df, entire_year_range, selected_species)[2],2)
all_sex_ratio = calculate_metrics(df, entire_year_range, selected_species)[5]

# Metriken darstellen
col_metric1, col_metric2,col_metric3,col_metric4,col_metric5 = st.columns(5)
with col_metric1:
    st.metric("Average Length", str(average_length/10) + " cm",str(round(((average_length/all_length-1)*100),2)) + " %")
    st.button("i",help="Diese Metriken stellen die Veränderung der durchschnittlichen Länge, des Gewichts, des Alters und des Geschlechterverhältnisses der gefangenen Lachse dar. Ausgangspunkt sind die durchschnittlichen Werte von 1960 bis 2016. Grün zeigt eine Verbesserung, Rot eine Verschlechterung im Vergleich zu den durchschnittlichen Werten von 1960 bis 2016.")
with col_metric2:
    st.metric("Average Weight", str(round(average_weight,2)) + " kg", delta=str(round(((round(average_weight,2)/all_weight-1)*100),2)) + " %")
with col_metric3:
    st.metric("Average Age (Saltwater)", str(round(average_age, 2)) + " years",delta=str(round(((round(average_age,2)/all_age-1)*100),2)) + " %")
with col_metric4:
    st.metric("Ratio Male to Female", sex_ratio,delta=str(round(((sex_ratio/all_sex_ratio-1)*100),2)) + " %")
with col_metric5:
    st.metric("Total number of fish caught", fish_count)



st.divider()


# darstellen der Gewichte, Längen..
col1,col2 = st.columns(2,gap="large")
with col1:
    auswahl = st.selectbox("Auswahl", ["Längen", "Gewichte","Ratio Male-Female","Saltwater Age"])
    if auswahl == "Längen":
        st.plotly_chart(fig_laengen(df,values,selected_species),use_container_width=True)
    elif auswahl == "Gewichte":
        st.plotly_chart(fig_gewichte(df,values,selected_species),use_container_width=True)
    elif auswahl == "Ratio Male-Female":
        st.plotly_chart(create_ratio_chart(df,values,selected_species),use_container_width=True)
    elif auswahl == "Saltwater Age":
        st.plotly_chart(fig_salt_water_age(df,values,selected_species),use_container_width=True)

# erstellen der Karte
with col2:
    map_fig = create_map(df, values, selected_species)
    st.plotly_chart(map_fig,use_container_width=True)
    

st.divider()

# sunburst chart
col1,col2 = st.columns(2)
with col1:
    st.header("Fangarten")
    fig = create_sunburst_chart(df,values, selected_species,50)
    st.plotly_chart(fig, use_container_width=True)
    top_gears = df['Gear'].value_counts().index[:7]
    selected_gear = st.selectbox('Wählen Sie eine Fangart aus:', top_gears)

    fangarten_bilder = {
    "fishwheel": "https://www.researchgate.net/publication/261175674/figure/fig12/AS:296830626746380@1447781345025/Salmon-fish-wheel-Chilkat-River-Alaska-August-7-2007-Credit-Keith-Criddle.png",
    "gillnet": "https://i.ytimg.com/vi/Hs2atBRSOtY/maxresdefault.jpg",
    "weir": "https://as1.ftcdn.net/v2/jpg/01/37/47/56/1000_F_137475605_TZDyTUvoAEdp23RFeeWnpiflXsL8cf2v.jpg",
    "trap": "https://carmelfinley.files.wordpress.com/2013/06/fishtrap.jpeg",
    "handpicked or carcass": "https://water.ca.gov/-/media/DWR-Images/Fish/2020_11_04_FL_Carcass_Survey-0083.jpg",
    "seine": "https://www.pac.dfo-mpo.gc.ca/fm-gp/salmon-saumon/images/seiner_drw.jpg",
    "spear": "https://live.staticflickr.com/8423/7544168736_18d2b62ee0_b.jpg",
    "troll": "https://fishingbooker-prod-blog-backup.s3.amazonaws.com/blog/media/2021/12/14142343/Trolling-rods-2-edited.jpg"

}
    
# pie chart --> Lachsarten
with col2:
    st.header("Verteilung der Lachsarten")
    fig = create_pie_chart(df,values)
    st.plotly_chart(fig, use_container_width=True)

# Bild der Fangarten
if selected_gear in fangarten_bilder:
        st.image(fangarten_bilder[selected_gear],use_column_width=True)
else:
        st.write("Kein Bild für diese Fangart verfügbar.")


