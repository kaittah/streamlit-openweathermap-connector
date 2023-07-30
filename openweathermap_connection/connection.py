from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import pyowm
import pandas as pd

class OpenWeatherMapConnection(ExperimentalBaseConnection[pyowm.owm.OWM]):
    """streamlit connection to OpenWeatherMap OneCall API"""

    def _connect(self, **kwargs) -> pyowm.owm.OMW:
        if 'owm_api_key' in kwargs:
            owm_api_key = kwargs.pop('owm_api_key')
        else:
            owm_api_key = self._secrets['owm_api_key']
        return pyowm.owm.OWM(owm_api_key)
    
    def agro_manager(self) -> pyowm.agro10.agro_manager.AgroManager: 
        """
        Gives a `pyowm.agro10.agro_manager.AgroManager` instance that can be used to read/write data from the
        Agricultural API.
        :return: a `pyowm.agro10.agro_manager.AgroManager` instance
        """
        return self._instance.agro_manager()

    def airpollution_manager(self) -> pyowm.airpollutionapi30.airpollution_manager.AirPollutionManager:
        """
        Gives a `pyowm.airpollutionapi30.airpollution_manager.AirPollutionManager` instance that can be used to fetch air
        pollution data.
        :return: a `pyowm.airpollutionapi30.airpollution_manager.AirPollutionManager` instance
        """
        return self._instance.airpollution_manager()

    def alert_manager(self) -> pyowm.alertapi30.alert_manager.AlertManager:
        """
        Gives an *AlertManager* instance that can be used to read/write weather triggers and alerts data.
        :return: an *AlertManager* instance
        """
        return self._instance.alert_manager()

    def city_id_registry(self) -> pyowm.commons.cityidregistry.CityIDRegistry:
        """
        Gives the *CityIDRegistry* singleton instance that can be used to lookup for city IDs.

        :returns: a *CityIDRegistry* instance
        """
        return self._instance.city_id_registry()

    def stations_manager(self) -> pyowm.stationsapi30.stations_manager.StationsManager:
        """
        Gives a *StationsManager* instance that can be used to read/write
        meteostations data.
        :returns: a *StationsManager* instance
        """
        return self._instance.stations_manager()

    def tile_manager(self, layer_name) -> pyowm.tiles.tile_manager.TileManager:
        """
        Gives a `pyowm.tiles.tile_manager.TileManager` instance that can be used to fetch tile images.
        :param layer_name: the layer name for the tiles (values can be looked up on `pyowm.tiles.enums.MapLayerEnum`)
        :return: a `pyowm.tiles.tile_manager.TileManager` instance
        """
        return self._instance.tile_manager()

    def uvindex_manager(self) -> pyowm.uvindexapi30.uvindex_manager.UVIndexManager:
        """
        Gives a `pyowm.uvindexapi30.uvindex_manager.UVIndexManager` instance that can be used to fetch UV data.
        :return: a `pyowm.uvindexapi30.uvindex_manager.UVIndexManager` instance
        """
        return self._instance.uvindex_manager()

    def weather_manager(self) -> pyowm.weatherapi25.weather_manager.WeatherManager:
        """
        Gives a `pyowm.weatherapi25.weather_manager.WeatherManager` instance that can be used to fetch air
        pollution data.
        :return: a `pyowm.weatherapi25.weather_manager.WeatherManager` instance
        """
        return self._instance.weather_manager()

    def geocoding_manager(self) -> pyowm.geocoding10.geocoding_manager.GeocodingManager:
        """
        Gives a `pyowm.geocoding10.geocoding_manager.GeocodingManager` instance that can be used to perform direct
        and reverse geocoding
        :return: a `pyowm.geocoding10.geocoding_manager.GeocodingManager` instance
        """
        return self._instance.geocoding_manager()
