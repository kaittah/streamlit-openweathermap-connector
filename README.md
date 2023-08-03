#### Streamlit OpenWeatherMap Connector

This connects to the OpenWeatherMap API using the [PyOWM](https://pyowm.readthedocs.io/en/latest/) package.

There are 2 types of connections created from Streamlit's [ExperimentalBaseConnection](https://docs.streamlit.io/library/api-reference/connections/st.connections.experimentalbaseconnection). 

The first connection returns an OWM object.
Example usage:
```
from openweathermap_connection import OpenWeatherMapConnection

conn = st.experimental_connection(name='example_conn', type=OpenWeatherMapConnection)
city_cur = conn.city_id_registry()
```
From there you can access the following entry points that `pyowm` provides:
- agro_manager()
- airpollution_manager() 
- alert_manager() 
- city_id_registry()
- geocoding_manager()
- stations_manager()
- tile_manager()
- uvindex_manager()
- weather_manager()

The second connection returns an entry point to OneCall.
Example usage:
```
from openweathermap_connection import OpenWeatherMapOneCallConnection

conn = st.experimental_connection('weather', lat=40.1, lon=-70.5, units='imperial', type=OpenWeatherMapOneCallConnection, ttl=3600)
temperature_data = conn.get_temperature_df()
current_temperature = conn.get_current()
```

This class lets you retrieve weather data with the [pyowm weather manager](https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#onecall).

`get_temperature_df` is a custom method that takes the hourly and daily forecasts and combines them into a single `pandas` dataframe with datetime and temperature.


