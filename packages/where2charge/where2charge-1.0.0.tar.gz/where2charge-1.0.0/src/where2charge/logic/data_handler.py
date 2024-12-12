"""This module contains functions to download, process, and save the data for EV charging stations and census tracts."""

__all__ = ['get_supplementary_data']

# import necessary libraries
import pandas as pd
import geopandas as gpd
import requests
from shapely.geometry import Point
import os
from datetime import datetime



# download the data from the source
def _get_data(adr_prefix):
    url1 = 'https://developer.nrel.gov/api/alt-fuel-stations/v1.csv?access=public&api_key=foEpOo7RpC4gPM41vxhvNB8IQLzek39WVbwjlX5p&cards_accepted=all&cng_fill_type=all&cng_has_rng=all&cng_psi=all&country=US&download=true&e85_has_blender_pump=false&ev_charging_level=2%2Cdc_fast&ev_connector_type=all&ev_network=all&fuel_type=ELEC&funding_sources=all&hy_is_retail=true&limit=all&lng_has_rng=all&lpg_include_secondary=false&maximum_vehicle_class=all&offset=0&owner_type=all&state=all&status=E%2CT&utf8_bom=true'
    url2 = 'https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD'
    # Output file name
    output_file1 = adr_prefix+'/data/alt_fuel_stations_updated.csv'
    output_file2 = adr_prefix+'/data/EVregistration.csv'
    # Make the GET request
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    # Check if the request was successful
    if response1.status_code == 200:
        with open(output_file1, 'wb') as file:
            file.write(response1.content)
        print(f"EV charger data downloaded successfully as '{output_file1}'.")
    else:
        raise Exception(f"EV charger data failed to download file. HTTP Status Code: {response1.statuscode}")
    if response2.status_code == 200:
        with open(output_file2, 'wb') as file:
            file.write(response2.content)
        print(f"EV registration data downloaded successfully as '{output_file2}'.")
    else:
        raise Exception(f"EV registration data failed to download file. HTTP Status Code: {response2.statuscode}")
    return pd.read_csv(output_file1), pd.read_csv(output_file2)


def _get_geo_data(evcs_df, adr_prefix):
    # read the data
    # df1 = pd.read_csv('./data/alt_fuel_stations_updated.csv')
    try:
        tracts = gpd.read_file(adr_prefix+"/data/TRACT_2020_90_20_PL.shp")

        # Create a geometry column from the Latitude and Longitude columns
        geometry = [Point(xy) for xy in zip(evcs_df['Longitude'], evcs_df['Latitude'])]

        geo_df = gpd.GeoDataFrame(evcs_df, geometry=geometry)
        # Select the columns we want to keep
        tracts = tracts[['GEOID_20','TRACT_20_N','AREA_SQMI','geometry']]
        # Ensure the coordinate reference systems match
        geo_df = geo_df.set_crs('EPSG:4326')  # We considered 4326 for both as it is the most common CRS
        tracts = tracts.to_crs('EPSG:4326')

        # Perform the spatial join now that we have the same CRS
        geo_df = gpd.sjoin(geo_df, tracts, how="left", predicate='intersects')
        # test the sjoin and raise exception if it fails
        

        geo_df = geo_df.dropna(subset=['GEOID_20'])
        geo_df.to_csv(adr_prefix+"/data/geo_df.csv", index=False)
        return pd.read_csv(adr_prefix+"/data/geo_df.csv")
    except Exception as e: # any issue with the previous steps will lead to an exception
        raise Exception(f"Failed to get the geodata. Error: {e}")


def _merge_data(geo_df, df_EV, adr_prefix):
    try:
        # count of EVs by 2020 Vensus Tract Column
        df_EV_count = df_EV.groupby('2020 Census Tract').size().reset_index(name='EVs')
        # change 2020 Census Tract column name to GEOID_20
        df_EV_count  = df_EV_count.rename(columns={'2020 Census Tract': 'GEOID_20'})

        # change to int to merge
        df_EV_count ['GEOID_20'] = df_EV_count ['GEOID_20'].astype(int)
        geo_df['GEOID_20'] = geo_df['GEOID_20'].astype(int)

        # merge
        merged_df = geo_df.merge(df_EV_count, on='GEOID_20', how='left')
        merged_df = merged_df[['Fuel Type Code', 'Station Name', 'Street Address', 'Intersection Directions',
        'City', 'Station Phone', 'Groups With Access Code', 'Access Days Time', 
        'EV Level1 EVSE Num', 'EV Level2 EVSE Num', 'EV DC Fast Count', 'EV Other Info',
        'EV Network', 'Latitude', 'Longitude', 'ID', 'Open Date', 'EV Connector Types', 
        'Facility Type', 'EV Pricing', 'Restricted Access', 'EV Workplace Charging', 'EVs']]
        merged_df.to_csv(adr_prefix+"/data/merged_df.csv", index=False)
        return merged_df
    except Exception as e:
        raise Exception(f"Failed to merge the final data. Error: {e}")


# push geo_df to github
def _push_data(self, adr_prefix):
# Get today's date
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    os.system(f"git add {adr_prefix}/data/merged_df.csv")
    os.system(f"git commit -m 'Uploading the final version of the data - {today}'")  # f string should be outside the quotes
    os.system("git push origin main")


def get_supplementary_data(address_prefix='src/where2charge/logic', generate=False):
    if generate:
        print("**** generating supplementary data ")
        evcs_df, evreg_df = _get_data(address_prefix)
        geo_df = _get_geo_data(evcs_df, address_prefix)
        data = _merge_data(geo_df, evreg_df, address_prefix)
        # push_data()
    else:
        data = pd.read_csv(address_prefix+'/data/merged_df.csv')
    return data
