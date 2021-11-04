

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import streamlit_analytics# source: https://pypi.org/project/streamlit-analytics/


# We use streamlit_analytics to track the site like in Google Analytics
streamlit_analytics.start_tracking()
# your streamlit code here


# configuring the page and the logo
st.set_page_config(page_title='Mohamed Gabr - The Smart City', page_icon ='logo.png', layout = 'wide', initial_sidebar_state = 'auto')


import os
import base64

# the functions to prepare the image to be a hyperlink
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code



# loading the data
DATE_TIME = "date/time"
DATA_URL = (
    "DubaiTrafficFake.csv"
)

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data(100000)
#print(data)
# creating the mapping functions

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_provider='carto',
        map_style="road",
        tooltip={
            'html': '<b>Traffic Volume Level:</b> {elevationValue}',
            'style': {
            'color': 'white'
            }
        },
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,# pitch (float, default None) – Up/down angle relative to the map’s plane, with 0 being looking directly at the map
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["longdubai", "latdubai"],# the lat & long columns in the csv file
                radius=100,# the number of points that it uses to aggregate the value من عدد النقط الموجودة يحدد ارتفاع العمود
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# adding whats app to the page
# from streamlit.components.v1 import components
# st.markdown(f"""<head><script src='https://apps.elfsight.com/p/platform.js' defer></script><div class='elfsight-app-7efae684-c950-4e81-8d00-f6cf1ba9d008'></div></head>""", unsafe_allow_html=True)


# installing Google analytics
# import re
# code = """<!-- Global site tag (gtag.js) - Google Analytics -->
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-QX8H7VED8C"></script>
# <script>
#   window.dataLayer = window.dataLayer || [];
#   function gtag(){dataLayer.push(arguments);}
#   gtag('js', new Date());
#
#   gtag('config', 'G-QX8H7VED8C');
# </script>"""
#st.markdown(code, unsafe_allow_html=True)
# a=os.path.dirname(st.__file__)+'/static/index.html'
# with open(a, 'r') as f:
#     data_GA=f.read()
#     if len(re.findall('UA-', data_GA))==0:
#         with open(a, 'w') as ff:
#             newdata=re.sub('<head>','<head>'+code,data_GA)
#             print(newdata)
#             ff.write(newdata)


# preparing the layout for the top section of the app
# dividing the layout vertically (dividing the first row)
row1_1, row1_2, row1_3 = st.columns((1,6,3))

# first row first column
with row1_1:
    gif_html = get_img_with_href('logo.png', 'https://golytics.github.io/')
    st.markdown(gif_html, unsafe_allow_html=True)
    #st.image('logo.png')
    #st.markdown('<a href="index.html"><img src="logo.png"><br>MG</a>', unsafe_allow_html=True)
    #st.markdown('<h1>Home</h1>', unsafe_allow_html=True)
with row1_2:
    #st.image('logo.png')
    st.title("Smart City Aspects: Monitoring & Prediction Using Artificial Intelligence")
    #st.write("Select the hour of prediction to get the traffic volume for each area")
    st.markdown("<h2>Traffic Volume Prediction</h2>", unsafe_allow_html=True)
    hour_selected = st.slider("Select the hour of prediction By sliding the slider so you can "
                              "view different time slots and get the traffic volume for each area in the selected time slot", 0, 23)
# first row second column
with row1_3:
    st.info(
    """
    ##
    This data product is a part of a project for creating a smart city monitoring and prediction dashboard. The project focused on
    the aspects of traffic volumes during the day, traffic video surveillance, air quality, sea water quality, power consumption
    levels, weather conditions, and preventive maintenance for IOT sensors. All the big data pipelines have been created, the data
    have been cleaned, and many models have been built to satisfy the client's requirements.** Here, we focus ONLY on Traffic Prediction**
    
    
    """)

# filtering data based on the slider
data = data[data[DATE_TIME].dt.hour == hour_selected]

# preparing the layout for the maps
# dividing the layout vertically (dividing the second row)

row2_1, row2_2, row2_3, row2_4 = st.columns((2,1,1,1))

# setting the zoom level and the locations for the districts
#la_guardia= [40.7900, -73.8700]
la_guardia=[25.153849,55.270783]# this is Dubai airport coordinates
jfk = [25.13083, 55.23273]
newark = [25.17760, 55.34878]
zoom_level = 12
#print(type(data["lat"]))
midpoint = (np.average(data["latdubai"]), np.average(data["longdubai"]))

with row2_1:
    st.write("**All Dubai City from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("**Downtown Dubai**")
    map(data, la_guardia[0],la_guardia[1], zoom_level)

with row2_3:
    st.write("**Al Quz**")
    map(data, jfk[0],jfk[1], zoom_level)

with row2_4:
    st.write("**Ras Al Khor Industrial Area 1**")
    map(data, newark[0],newark[1], zoom_level)

# FILTERING DATA FOR THE HISTOGRAM
filtered = data[
    (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "volume": hist})
#print(chart_data)

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of traffic volumes per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("volume:Q"),
        tooltip=['minute', 'volume']
    ).configure_mark(
        opacity=0.5,
        color='blue'
    ), use_container_width=True)

#st.write('**Note: ** The data used in this data product are modified due to NDA agreements with the client. So, the data, used here, is not reliable for decision making.')
st.info('**Note: ** The data used in this data product are modified due to NDA agreements with the client. So, the data, used here, is not reliable for decision making.')

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed By: <a href="https://golytics.github.io/" target="_blank">Dr. Mohamed Gabr</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)



streamlit_analytics.stop_tracking(unsafe_password="forward1")