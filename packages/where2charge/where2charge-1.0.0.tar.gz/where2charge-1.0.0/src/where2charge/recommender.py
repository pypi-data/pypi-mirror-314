"""
This file get connected to the server and handles the logic
behind our work. To start working with this code, first a
Recommender object must be successfully instantiated.
"""

__all__=['Recommender']

import json

import geopandas as gpd
import pandas as pd

from .logic.analyzer import Analyzer
from .logic.data_handler import get_supplementary_data
from .logic.googleAPI_handler import GoogleAPIHandler



def _merge_data(google_data, evcs_data):
    """
    merge the data from Google Places API and census tract data, EVCS data
    :param google_data:
    :param evcs_data:
    :return:
    """
    # Convert to GeoDataFrame
    gdf10 = gpd.GeoDataFrame(google_data,
                             geometry=gpd.points_from_xy(google_data['Longitude'], google_data['Latitude']))
    gdf_all = gpd.GeoDataFrame(evcs_data,
                               geometry=gpd.points_from_xy(evcs_data['Longitude'], evcs_data['Latitude']))

    # Create buffer
    buffer_size = 0.0001   # buffer size might be problematic
    gdf10['buffer'] = gdf10.geometry.buffer(buffer_size)
    # Drop or rename conflicting columns
    gdf10 = gdf10.drop(columns=['index_left', 'index_right'], errors='ignore')
    gdf_all = gdf_all.drop(columns=['index_left', 'index_right'], errors='ignore')
    # Perform spatial join
    merged = gpd.sjoin(gdf10.set_geometry('buffer'), gdf_all, how='inner', predicate='intersects')
    # Cleanup and finalize
    result = merged.drop(columns=['buffer']).reset_index(drop=True)
    return result


def _clean_routes(data):
    """
    Simplifies 'Route' entries in the data from Google queries to only latitude and longitude coordinates.
    These points can be shown on a map by drawing a polyline
    :param data: List of dictionaries, where each dictionary represents a record containing route data.
    :return: Updated dataset with modified 'Route' entries.
    """
    for entry in data:
        route = entry.get("Route")  # Get the "Route" data for each row
        if route:  # Check if the route data exists
            coordinates = []
            for leg in route.get("legs", []):
                for step in leg.get("steps", []):
                    # Extract start and end coordinates
                    start = (step["start_location"]["lat"], step["start_location"]["lng"])
                    end = (step["end_location"]["lat"], step["end_location"]["lng"])
                    coordinates.append(start)
                    coordinates.append(end)
            # Replace the "Route" data with extracted coordinates
            entry["Route"] = coordinates
    return data


def _to_list(data)->list:
    """
    this function transforms the data from a dataframe into a list of objects (json)
    [{'Name': 'Charger1', 'Location': {'lat': ..., 'lng': ...}, 'Review score': 1.0,
            'Distance': '0.2 km', 'Travel_Time': '1 min', 'Route': {...}},
     {'Name':...}]

    :param data: dataframe created in Recommender.get_suggestions() method
    :return: a dictionary where
    """
    # we need to remove geometry (it shouldn't be geo dataframe) to be able to convert to json
    if 'geometry' in data.columns:
        data = data.drop(columns=['geometry'])
    else:
        pass
    # we need to orient on records to all columns infor for each row then move to the next
    data = data.to_json(orient='records')
    # converting the json string to a list
    data = json.loads(data)
    return data


class Recommender:
    """
    In order to make suggestion to EV users, we need to have a logic handler that
    controls and mixes all different parts of the logic. Therefore, one connection
    to openai api and one connection to google Places api is needed. Since using
    global variables is not popular and recommended, the alternative is to switch
    to object-oriented programming (OOP).

    In our new design, the user may need to instantiate a recommender object in
    which there are other objects that need to be in working status first.
    These objects are: a data collection object, a Google api handler object,
    and an analyzer object.
    """
    def __init__(self, google_api_key, openai_api_key):
        """
        the recommendation system can work when analyzer and google api connections
        can work.
        :param google_api_key:
        :param openAI_api_key:
        :return:
        """
        try:
            self.google_handler = GoogleAPIHandler(google_api_key)
            self.analyzer = Analyzer(openai_api_key)
            try:
                self.evcs_data = pd.read_csv('src/where2charge/logic/data/merged_df.csv')
                #todo: Probably won't work when where2charge is installed as a package
            except FileNotFoundError as e:
                print(f'---- {e}')
                self.evcs_data = get_supplementary_data()
            print('** Recommender successfully initialized')
        except Exception as e: #todo: exact error type and message TBD
            print('** Recommender failed to initialize')
            raise e


    def get_suggestions(
            self, lat, lng, n_recomm=5, charger_type=None
    ):
        """
        Main function that is called from outside of this package.
        :param lat: latitude of user's given address
        :param lng: longitude of user's given address'
        :param n_recomm: number of recommendations that the user is asking for
        :param charger_type: charger type of user's electric vehicle
        :return: A json string formatted in a way that server and app are implemented based on
        """
        print('request attributes:', lat, lng, n_recomm, charger_type)  # log
        #todo error handling
        ## find suggestions ##
        google_data = self.google_handler.get_all_data_from_google(lat, lng)
        data = _merge_data(google_data, self.evcs_data)
        # google_data.to_csv('data_google.csv', index=False) # log
        # data.to_csv('data.csv', index=False) # log

        # data = self.analyzer.get_suggestions(data, n_recomm, charger_type)
        # todo: there are some limitations in the supplementary data which reduces google results
        #  from 10 entries to around 3-4 entries. when we fix this, we will use the complete
        #  dataset and analyze based on all features we have for each EVCS
        data = self.analyzer.get_suggestions(google_data, n_recomm, None)
        data = self.google_handler.get_routes(data, lat, lng)
        data.to_csv('data_sorted.csv', index=False) # log

        ## formatting the data ##
        data = _to_list(data)
        data = _clean_routes(data)
        # this function is going to be called from server which is located outside of
        # this package. so we should have a standard output. That's why I feel send out
        # the output as a json string is a better thing to do.
        data = json.dumps({'locations': data})
        return data