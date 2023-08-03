import streamlit as st
import plotly.graph_objs as go

from openweathermap_connection import OpenWeatherMapOneCallConnection, OpenWeatherMapConnection

st.set_page_config(page_title='Weather', page_icon='🌐', layout='centered', initial_sidebar_state='collapsed')
st.title('🌐 Weather')

class LocationError(Exception):
    pass

# Get latitude and longitude from city
location = st.text_input('Enter a location in the US in the format <city, state>', 'Boston, MA')
city_conn = st.experimental_connection(name='city_conn', type=OpenWeatherMapConnection)
city_cur = city_conn.city_id_registry()
location_split = (location + ',').split(',')
city = location_split[0].strip()
state= location_split[1].strip()
if not city or not state:
    raise LocationError('Location not in the format <city, state>')
pts = city_cur.geopoints_for(city_name=city, state=state, country='US')
if len(pts) > 0:
    pt = pts[0]
else:
    raise LocationError('Location not found')
lat = pt.lat
lon = pt.lon

unit = st.radio('Unit', ['metric', 'imperial'])
unit_symbol = {'metric': 'C', 'imperial': 'F'}

with st.echo():
    conn = st.experimental_connection('weather', lat=lat, lon=lon, units=unit, type=OpenWeatherMapOneCallConnection, ttl=3600)
    temperature_data = conn.get_temperature_df()
    
    fig = go.Figure()
    fig.add_traces([go.Scatter(x=temperature_data['dt'], y=temperature_data['temp'], name='temperature'),
                    go.Scatter(x=temperature_data['dt'], y=temperature_data['low_temp'], name='low'),
                    go.Scatter(x=temperature_data['dt'], y=temperature_data['high_temp'], name='high')])
    fig.update_xaxes(title='UTC Time')
    fig.update_yaxes(title=f'Temperature (deg{unit_symbol[unit]})')
    st.plotly_chart(fig)