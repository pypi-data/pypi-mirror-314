from datetime import datetime, timedelta
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pygeohash as pgh
import os
import sys
from pyproj import Geod
import logging
import re
from glob import glob
import random
from dssatsim.envs import (
    WTH_COLUMNS, 
    DATA_TYPES_TO_DB_TABLES, 
    SERVERLESS_DB_DIR
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if sys.platform.startswith('win'):
    import psycopg2 # somehow this lib won't load in linux

def inches_to_mm(inches):
    return inches * 25.4

def get_number_closer_to(number, range=3):
    new_number = number + random.randint(-range, range)
    return new_number if new_number > 0 else number

def generate_random_number(min_num=3, max_num=10):
    return random.randint(min_num, max_num)


def generate_irrigation_random_events(crop, minimum_apps_num=2, irrigation_min_inches=0.5, irrigation_max_inches=0.8, planting_date="2023-05-15"):
    irrigation_events = []
    
    # min apps is 2 and that is taken from here: https://www.canr.msu.edu/irrigation/upoads/files/MW-CWN-July08-15.24.pdf

    # To determine if crops need irrigation, there are simple tips and tools available. 
    # Crops in vegetative stages such as corn at V4 to V8 typically use 0.5 to 0.8 inches of water per week, 
    # while soybeans at V1 to V2 use 0.4 to 0.6 inches per week under normal conditions. 
    # Crops with a full canopy, such as winter wheat and forages before cutting, use 1.5 to 2 inches per week.

    # https://www.canr.msu.edu/news/four_fundamental_stages_of_corn_grain_yield_determination states that:
    #   ... rapid phase of corn vegetative growth, which generally occurs in early to mid-July in Michigan. 


    # to approximate the duration of the vegetative stage based on the month, I use this reference: https://www.extension.purdue.edu/extmedia/nch/nch-40.html
    veg_stages_duration = {
        "corn": {
            "04": 62, # i.e. if planting is ~mid April: The vegetative stage lasts 62 days
            "05": 44, # i.e. if planting is ~mid May: The vegetative stage lasts 44 days
            "06": 36, # i.e. if planting is ~mid June: The vegetative stage lasts 36 days
        },

        # to find the months, I used this ref: https://www.canr.msu.edu/news/soybean-planting-and-time-management-considerations
        # for estimating the average duration, I used: https://extension.umn.edu/growing-soybean/soybean-growth-stages
        "soybean": {
            "04": 28, # I am assuming this value to be the same for all months
            "05": 28, # I am assuming this value to be the same for all months
            "06": 28, # I am assuming this value to be the same for all months
        }
        
    }

    default_veg_duration = {
        "corn": 47, # the average of the values in the corn dict
        "soybean": 28 # the average of the values in the soybean dict
    }

    unknown_crop_veg_duration = 30

    _, month_got, _ = map(int, planting_date.split("-")) 
    veg_duration = veg_stages_duration.get(crop, {}).get(month_got, default_veg_duration.get(crop, unknown_crop_veg_duration))


    # find the date of the vegetative stage by adding the duration to the planting date
    planting_date_obj = datetime.strptime(planting_date, "%Y-%m-%d")
    veg_stage_end_date = planting_date_obj + timedelta(days=veg_duration)

    # determine how many weeks there are between the planting date and the vegetative stage end date
    weeks_between = (veg_stage_end_date - planting_date_obj).days // 7

    # determine the list of dates that fall within each of the weeks
    week_dates = []
    for i in range(weeks_between):
        date_obj = planting_date_obj + timedelta(weeks=i)
        date_obj_str = date_obj.strftime("%Y-%m-%d")
        week_dates.append(date_obj_str)


    # extract month and day from planting date. for eample: "2023-05-15"
    planting_date = planting_date.split("-")

    how_many_apps = random.randint(minimum_apps_num, len(week_dates)-1)
    # print(f"how_many_apps: {how_many_apps}")
    for i in range(how_many_apps):
        # select a random date from the week_dates list
        random_date_str = week_dates[i]
        # select a random amount of irrigation between the min and max inches
        random_irrigation_inches = random.uniform(irrigation_min_inches, irrigation_max_inches)
        random_irrigation_mm = round(inches_to_mm(random_irrigation_inches), 2)

        irrigation_events.append([random_date_str, random_irrigation_mm])

    return irrigation_events


def find_nearest_location(latitude, longitude):
    pass

def yrdoy_to_date(yrdoy):
    yrdoy_str = str(yrdoy)
    year, doy = yrdoy_str[:4], yrdoy_str[4:]
    return datetime.strptime(year + doy, "%Y%j")


def date_to_doy(date_str='2023-12-30'):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.timetuple().tm_yday


def format_wth_date_str(date_str='2023-12-30'):
    """ '2023-12-30' --> 23364 """
    yr = date_str.split("-")[0][2:]
    return f"{yr}{date_to_doy(date_str):03}"


def get_header_lines(out_fpath):
    """
    Reads the initial lines of a file until a line containing '@' within the first 10 characters is encountered.
    Args:
        out_fpath (str): The path to the file to be read.
    Returns:
        list: A list of initial lines from the file up to and including the line containing '@'.
    """
    
    table_start = -1
    init_lines = []
    with open(out_fpath, 'r', encoding='cp437') as f:
        while True:
            table_start += 1
            init_lines.append(f.readline())
            if '@' in init_lines[-1][:10]:
                break
    return init_lines


def get_most_recent_dssat_output_dir():
    match_list = glob(f"/tmp/dssat*/*.OUT")
    most_recent_folder = max(set(os.path.dirname(f) for f in match_list), key=os.path.getmtime)
    return most_recent_folder


def retrieve_fout_path(code="Summary"):
    most_recent_folder = get_most_recent_dssat_output_dir()
    return os.path.join(most_recent_folder, f"{code}.OUT")

def clean_up_folder(folder):
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))


def format_wth_date(date):
    """
    Converts a datetime-like object to a string in the format 'YYDDD'.
    
    Parameters:
    - date (datetime-like): A datetime object (e.g., pandas Timestamp, datetime.datetime, numpy.datetime64)
    
    Returns:
    - str: A string representing the date in 'YYDDD' format (e.g., '23364' for '2023-12-30')
    
    Raises:
    - TypeError: If the input is not a datetime-like object.
    """
    # Ensure the input is a pandas Timestamp, datetime, or numpy.datetime64 object
    if not isinstance(date, (pd.Timestamp, pd.DatetimeIndex, datetime, pd.core.arrays.datetimes.DatetimeArray)):
        raise TypeError("date must be a datetime-like object.")
    
    # If the input is a numpy.datetime64, convert it to pandas Timestamp
    if isinstance(date, pd.Series):
        if not pd.api.types.is_datetime64_any_dtype(date):
            raise TypeError("date must be a datetime-like object.")
        date = date.iloc[0]
    elif isinstance(date, pd.DatetimeIndex):
        date = date[0]
    elif isinstance(date, pd.core.arrays.datetimes.DatetimeArray):
        date = date[0]
    elif isinstance(date, pd.Timestamp):
        pass  # Already a pandas Timestamp
    elif isinstance(date, datetime):
        pass  # Already a datetime.datetime object
    
    # Extract the last two digits of the year
    yr = date.year % 100  # e.g., 2023 % 100 = 23
    
    # Extract the day of the year
    doy = date.dayofyear  # 1 to 366
    
    # Format as 'YYDDD', zero-padded
    formatted_date = f"{yr:02}{doy:03}"
    
    return formatted_date

def geohash_encode(lat, lon, length=8):
    """ Encode latitude and longitude to a geohash with a specified precision. """
    return pgh.encode(latitude=lat, longitude=lon, precision=length)

def wattspersqm_to_mgjpersqm(srad):
    """
    Convert solar radiation from W/m^2 to MJ/m^2/day.
    rf: https://www.fao.org/4/X0490E/x0490e0i.htm
    """
    return round(srad * 0.0864, 1)  # 0.0864 = 1 MJ/m^2/day / 11.574 W/m^2


def format_table_to_WTH_lines(ftable_name, is_file=True):
    """
        Convert a CSV table to a list of formatted lines for a DSSAT weather file (.WTH).

        The input table must have 365/366 rows and the following columns:
        @DATE, SRAD, TMAX, TMIN, RAIN, DEWP, WIND, PAR, EVAP, RHUM.

        Parameters:
        ftable_name (str or pandas.DataFrame): The name of the CSV file to read or a DataFrame.
            - If `is_file` is True, `ftable_name` should be a string representing the path to the CSV file.
            - If `is_file` is False, `ftable_name` should be a pandas DataFrame.
        is_file (bool): Flag indicating whether `ftable_name` is a file path (True) or a DataFrame (False).
        
        Returns:
        list: A list of strings, each representing a formatted line for a .WTH file.

        The function processes each row to ensure it matches the DSSAT weather file format:
        - @DATE: String, right-justified to 5 characters with leading zeros after the last two digits of the year. e.g. 23001 is 2023-01-01.
        - SRAD, TMAX, TMIN, RAIN: Floats, right-justified to 6 characters with leading spaces. Must be in this unit
            SRAD: Daily solar radiation, MJ m-2 day-1 
            TMAX: Maximum temperature, degrees Celsius
            TMIN: Minimum temperature, degrees Celsius
            RAIN: Daily rainfall, mm
        - The resulting line is formatted as: '00001  0.00  0.00  0.00  0.00 \n' for example.

        Example Usage:
        >>> format_table_to_WTH_lines('weather_data.csv')
        ['00001  0.00  0.00  0.00  0.00 \n', ...]
    """
    def format_row(row):
        row_str = ""
        for i, e in enumerate(row, start=1):
            if i in [2,  3,  4,  5]:
               row_str += str(e).rjust(6, " ")
        final_row = str(int(row.iloc[0])).rjust(5, "0") + row_str + " \n"
        return final_row

    table = pd.read_csv(ftable_name) if is_file else ftable_name
    list_lines = table.apply(lambda x: format_row(x), axis=1)

    return list_lines.values.tolist()


def extract_serverless_db_table_for_location(
    target_lat,
    target_lon,
    data_type,
    dbname="agxdbv1",
    columns=None,
    date=None,
):
    """
    Retrieves data from a Parquet file for the nearest latitude and longitude to the target location.

    Parameters:
    - target_lat (float): The target latitude to search for the nearest location.
    - target_lon (float): The target longitude to search for the nearest location.
    - data_type (str): The type of data to retrieve, which maps to a specific Parquet file.
    - dbname (str): Name of the database folder containing the Parquet files.
    - columns (list, optional): A list of column names to retrieve from the data. If None, all columns will be retrieved.
    - date (str, optional): A date in the format 'yyyy-mm-dd' or a year in the format 'yyyy' to filter the data.

    Returns:
    - pd.DataFrame: A DataFrame containing the retrieved data for the nearest location and the specified columns.
    - str: A string indicating the status or an error message if something went wrong.
    """

    data_dir = os.path.join(SERVERLESS_DB_DIR, dbname)

    try:
        # Get the file name for the given data_type
        if data_type not in DATA_TYPES_TO_DB_TABLES:
            msg = f"Data type '{data_type}' is not recognized."
            print(msg)
            return None, msg

        file_name = DATA_TYPES_TO_DB_TABLES[data_type]
        parquetfile_path = os.path.join(
            data_dir, f"{file_name}.parquet"
        )

        # Check if the file exists
        if not os.path.exists(parquetfile_path):
            msg = f"File '{file_name}.parquet' not found in folder '{data_dir}'."
            print(msg)
            return None, msg

        # Read the Parquet file into a DataFrame
        df = pd.read_parquet(parquetfile_path)
        # print(df.head(2))

        # Ensure 'latitude' and 'longitude' columns are present
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            msg = "The data does not contain 'latitude' and 'longitude' columns."
            print(msg)
            return None, msg

        # Handle missing values in 'latitude' and 'longitude'
        df = df.dropna(subset=['latitude', 'longitude'])

        # Convert to GeoDataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

        # Filter by date if provided
        if date:
            date_column = 'date'  # Adjust if your date column has a different name
            if date_column in gdf.columns:
                try:
                    gdf[date_column] = pd.to_datetime(gdf[date_column])
                    date = pd.to_datetime(date)
                    if date.strftime('%Y-%m-%d') == 'NaT':
                        # Year only
                        gdf = gdf[gdf[date_column].dt.year == date.year]
                    else:
                        # Full date
                        gdf = gdf[gdf[date_column] == date]
                except ValueError:
                    msg = "Invalid date format. Please use 'yyyy-mm-dd' or 'yyyy'."
                    print(msg)
                    return None, msg

                if gdf.empty:
                    msg = f"No data found for the specified date: {date}."
                    print(msg)
                    return None, msg
            else:
                msg = f"Date column '{date_column}' not found in the data."
                print(msg)
                return None, msg

        # Create a GeoSeries for the target point
        target_point = Point(target_lon, target_lat)

        # Initialize Geod object
        geod = Geod(ellps='WGS84')

        # Calculate geodesic distances
        distances = gdf.geometry.apply(
            lambda point: geod.inv(target_lon, target_lat, point.x, point.y)[2]
        )
        gdf['distance'] = distances

        # Find the nearest location
        nearest_row = gdf.loc[gdf['distance'].idxmin()]

        # Select specified columns if provided
        if columns:
            available_columns = set(gdf.columns)
            columns_set = set(columns)
            missing_columns = columns_set - available_columns
            if missing_columns:
                msg = (
                    f"The following columns are not found in the data: {', '.join(missing_columns)}"
                )
                print(msg)
                return None, msg
            # Ensure 'columns' is a list of strings
            if not isinstance(columns, list):
                msg = f"'columns' parameter should be a list of column names."
                print(msg)
                return None, msg
            nearest_row = nearest_row[list(columns) + ['latitude', 'longitude', 'distance']]
        else:
            # If columns are not specified, select all columns
            nearest_row = nearest_row.copy()

        # Convert the nearest_row to a DataFrame
        result_df = pd.DataFrame([nearest_row])

        # Reset index
        result_df.reset_index(drop=True, inplace=True)

        return result_df, "success"

    except Exception as e:
        msg = f"Error: {e}"
        print(msg)
        return None, msg


def extract_postgresql_db_table_for_location_todel(db_params, target_lat, target_lon, data_type, columns=None, date=None):
    """
    Retrieves data from a database table for the nearest latitude and longitude to the target location.

    This function finds the nearest latitude and longitude to the specified target coordinates using PostGIS,
    retrieves the specified columns from the corresponding database table, and returns the data in a DataFrame.
    The function can filter the results based on a specific date or year.

    Parameters:
    - db_params (dict): A dictionary containing the database connection parameters (e.g., host, port, user, password, dbname).
    - target_lat (float): The target latitude to search for the nearest location.
    - target_lon (float): The target longitude to search for the nearest location.
    - data_type (str): The type of data to retrieve, which maps to a specific database table.
    - columns (list, optional): A list of column names to retrieve from the table. If None, all columns will be retrieved.
    - date (str, optional): A date in the format 'yyyy-mm-dd' or a year in the format 'yyyy' to filter the data.

    Returns:
    - pd.DataFrame: A DataFrame containing the retrieved data for the nearest latitude, longitude, and the specified columns.
    - str: A string indicating the status or an error message if something went wrong.

    If no data is found for the nearest location or if an error occurs, the function will return None and an appropriate message.

    Notes:
    - The function uses PostGIS to perform geographic operations and retrieve the nearest point.
    - The `DATA_TYPES_TO_DB_TABLES` dictionary should be defined elsewhere in the code and should map `data_type` values to database table names.
    - The function handles both full dates ('yyyy-mm-dd') and years ('yyyy') for filtering the data.
    - If a date is provided, the function will filter the results based on the exact date or the year.
    - If an invalid date format is provided, the function will return None and print an error message.

    Example:
    ```
    db_params = {
        "host": "localhost",
        "port": 5432,
        "user": "username",
        "password": "password",
        "dbname": "weather_db"
    }
    df, msg = extract_serverless_db_table_for_location(db_params, 12.34, 56.78, 'weather', columns=['temperature', 'humidity'], date='2023')
    if df is not None:
        print(df)
    else:
        print(msg)
    ```
    """
    table_name = DATA_TYPES_TO_DB_TABLES[data_type]
    
    try:
        # Establish database connection
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Find the nearest latitude and longitude
                nearest_query = f"""
                    SELECT latitude, longitude, 
                           ST_Distance(ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, geom::geography) AS distance
                    FROM public."{table_name}"
                    ORDER BY geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
                    LIMIT 1
                """
                
                cur.execute(nearest_query, (target_lon, target_lat, target_lon, target_lat))
                nearest_point = cur.fetchone()
                
                if not nearest_point:
                    print("No nearby latitude or longitude pair found.")
                    return None
                
                nearest_lat = nearest_point[0]
                nearest_lon = nearest_point[1]
                
                # Determine the columns to retrieve
                if columns:
                    columns_str = "latitude, longitude, " + ", ".join(columns)
                else:
                    cur.execute(f"""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}' AND table_schema = 'public'
                    """)
                    all_columns = [row[0] for row in cur.fetchall()]
                    columns_str = ", ".join(all_columns)
                
                # Determine if the date is a full date or just a year
                date_condition = ""
                date_param = None
                if date:
                    try:
                        # Try to parse the date as a full date
                        datetime.strptime(date, '%Y-%m-%d')
                        date_condition = " AND date = %s"
                        date_param = date
                    except ValueError:
                        # If it's not a full date, assume it's just a year
                        try:
                            datetime.strptime(date, '%Y')
                            date_condition = " AND EXTRACT(YEAR FROM date::timestamp) = %s"
                            date_param = int(date)
                        except ValueError:
                            print("Invalid date format. Please use 'yyyy-mm-dd' or 'yyyy'.")
                            return None
                
                # Retrieve the specified columns
                columns_query = f"""
                    SELECT {columns_str}
                    FROM public."{table_name}"
                    WHERE latitude = %s AND longitude = %s{date_condition}
                """
                
                params = (nearest_lat, nearest_lon)
                if date_param is not None:
                    params += (date_param,)
                
                cur.execute(columns_query, params)
                result_rows = cur.fetchall()
                
        if result_rows:
            return pd.DataFrame(result_rows, columns=columns_str.split(", ")), "success"
        else:
            msg = "No data found for the nearest latitude and longitude."
            return None, msg

    except psycopg2.Error as e:
        msg = f"Database error: {e}"
        return None, msg


def extract_serverless_db_table_for_location(
    target_lat,
    target_lon,
    data_type,
    dbname="agxdbv1",
    columns=None,
    date=None,
    date_column='date',  # Allow dynamic date column name
):
    """
    Retrieves data from a Parquet file for the nearest latitude and longitude to the target location.

    Parameters:
    - target_lat (float): The target latitude to search for the nearest location.
    - target_lon (float): The target longitude to search for the nearest location.
    - data_type (str): The type of data to retrieve, which maps to a specific Parquet file.
    - dbname (str): Name of the database folder containing the Parquet files.
    - columns (list, optional): A list of column names to retrieve from the data. If None, all columns will be retrieved.
    - date (str, optional): A date in the format 'yyyy-mm-dd' or a year in the format 'yyyy' to filter the data.
    - date_column (str, optional): The name of the date column in the data.

    Returns:
    - pd.DataFrame: A DataFrame containing the retrieved data for the nearest location and the specified columns.
    - str: A string indicating the status or an error message if something went wrong.
    """

    data_dir = os.path.join(SERVERLESS_DB_DIR, dbname)

    try:
        # Validate target_lat and target_lon
        if not (-90 <= target_lat <= 90):
            msg = "Invalid latitude value. Must be between -90 and 90."
            
            return None, msg

        if not (-180 <= target_lon <= 180):
            msg = "Invalid longitude value. Must be between -180 and 180."
            
            return None, msg

        # Validate data_type
        if data_type not in DATA_TYPES_TO_DB_TABLES:
            msg = f"Data type '{data_type}' is not recognized."
            
            return None, msg

        # Construct Parquet file path
        file_name = DATA_TYPES_TO_DB_TABLES[data_type]
        parquetfile_path = os.path.join(data_dir, f"{file_name}.parquet")

        # Check file existence
        if not os.path.exists(parquetfile_path):
            msg = f"File '{file_name}.parquet' not found in folder '{data_dir}'."
            
            return None, msg

        # Read Parquet file into DataFrame
        df = pd.read_parquet(parquetfile_path)

        # Validate presence of 'latitude' and 'longitude' columns
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            msg = "The data does not contain 'latitude' and 'longitude' columns."
            
            return None, msg

        # Drop rows with missing latitude or longitude
        df = df.dropna(subset=['latitude', 'longitude'])

        # Convert to GeoDataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

        # Initialize Geod object for distance calculations
        geod = Geod(ellps='WGS84')

        # Calculate distance to target location
        gdf['distance'] = gdf.geometry.apply(
            lambda point: geod.inv(target_lon, target_lat, point.x, point.y)[2]
        )

        # Identify the nearest unique location
        # Sort by distance and drop duplicates to get unique latitude and longitude
        gdf_sorted = gdf.sort_values('distance')
        unique_locations = gdf_sorted.drop_duplicates(subset=['latitude', 'longitude'])

        if unique_locations.empty:
            msg = "No unique locations found in the data."
            
            return None, msg

        # Select the nearest location
        nearest_location = unique_locations.iloc[0]
        nearest_lat = nearest_location['latitude']
        nearest_lon = nearest_location['longitude']
        logger.info(f"Nearest location found at latitude: {nearest_lat}, longitude: {nearest_lon}")

        # Filter data for the nearest location
        location_gdf = gdf[
            (gdf['latitude'] == nearest_lat) &
            (gdf['longitude'] == nearest_lon)
        ]

        # Optional Date Filtering
        if date:
            if date_column not in location_gdf.columns:
                msg = f"Date column '{date_column}' not found in the data."
                
                return None, msg

            # Determine if the date is a year or a full date
            if re.fullmatch(r"\d{4}", date):
                # Date is a year
                target_year = int(date)
                location_gdf[date_column] = pd.to_datetime(location_gdf[date_column], errors='coerce')
                location_gdf = location_gdf[location_gdf[date_column].dt.year == target_year]

                if location_gdf.empty:
                    msg = f"No data found for the specified year: {target_year}."
                    
                    return None, msg

            elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                # Date is a specific date
                target_date = pd.to_datetime(date, format='%Y-%m-%d', errors='coerce')
                if pd.isna(target_date):
                    msg = "Invalid full date format. Please use 'yyyy-mm-dd'."
                    
                    return None, msg

                location_gdf[date_column] = pd.to_datetime(location_gdf[date_column], errors='coerce')
                location_gdf = location_gdf[location_gdf[date_column] == target_date]

                if location_gdf.empty:
                    msg = f"No data found for the specified date: {date}."
                    
                    return None, msg
            else:
                # Invalid date format
                msg = "Invalid date format. Please use 'yyyy-mm-dd' or 'yyyy'."
                
                return None, msg

        # After filtering, check if location_gdf is empty
        if location_gdf.empty:
            msg = "No data available after applying date filters."
            
            return None, msg

        # Select specified columns if provided
        if columns:
            if not isinstance(columns, list):
                msg = f"'columns' parameter should be a list of column names."
                
                return None, msg

            available_columns = set(location_gdf.columns)
            columns_set = set(columns)
            missing_columns = columns_set - available_columns
            if missing_columns:
                msg = f"The following columns are not found in the data: {', '.join(missing_columns)}"
                
                return None, msg

            # Ensure 'latitude', 'longitude', and 'distance' are included
            selected_columns = list(columns) + ['latitude', 'longitude', 'distance']
            # Verify that selected_columns are present
            selected_columns = [col for col in selected_columns if col in location_gdf.columns]
            location_gdf = location_gdf[selected_columns]

        # Reset index for cleanliness
        result_df = location_gdf.reset_index(drop=True)

        return result_df, "success"

    except Exception as e:
        msg = f"Error: {e}"
        
        return None, msg


def location_to_WTH_file(db_params, target_lat, target_lon, year, outdir, institution_code="AGXQ"):
    """
    Generates a weather file in WTH format for a specified location and year, and saves it to a specified directory.

    This function retrieves daily weather data for a given latitude and longitude from a database for a specified year,
    processes the data, and writes it to a WTH file format. The WTH file includes weather data such as solar radiation,
    maximum and minimum temperatures, rainfall, and more. The file is saved in the specified output directory with
    a filename based on the geohash encoding of the location.

    Parameters:
    - db_params (dict): Database parameters needed for retrieving weather data. Should include necessary connection details.
    - target_lat (float): Latitude of the target location. Will be rounded to three decimal places.
    - target_lon (float): Longitude of the target location. Will be rounded to three decimal places.
    - year (int or str): Year for which the weather data is to be retrieved. Will be converted to string.
    - outdir (str): Directory path where the WTH file will be saved.
    - institution_code (str, optional): Code for the institution providing the weather data. Default is "AGXQ".

    Returns:
    dict: A dictionary containing the following keys:
        - "wth_fpath" (str): The full file path where the WTH file is saved.
        - "location_encoding" (str): The geohash encoding of the specified latitude and longitude.
        - "year" (str): The year for which the weather data was retrieved.
        - "wth_table_df" (pd.DataFrame): The DataFrame containing the processed weather data that was written to the WTH file.

    Side Effects:
    - Writes a WTH file to the specified output directory.
    - Prints the file path where the WTH file is saved.

    Notes:
    - The WTH file format includes headers and weather data formatted according to the WTH standard.
    - The `location_to_daily_weather_table`, `format_wth_date`, `wattspersqm_to_mgjpersqm`, `format_table_to_WTH_lines`,
      and `geohash_encode` functions should be defined elsewhere in the code.
    - The `WTH_COLUMNS` variable should be defined and include the columns to be written to the WTH file.
    """
    
    target_lat = round(target_lat, 3)
    target_lon = round(target_lon, 3)
    year = str(year)
    daily_weather_table_, msg = extract_serverless_db_table_for_location(
        target_lat=target_lat, 
        target_lon=target_lon,
        data_type="wth",
        date=year
    )

    if daily_weather_table_ is None:
        print(msg)
        return
    
    ['@DATE', 'SRAD', 'TMAX', 'TMIN', 'RAIN', 'DEWP', 'WIND', 'PAR', 'EVAP', 'RHUM']
    daily_weather_table_["@DATE"] = daily_weather_table_["date"].apply(format_wth_date)
    daily_weather_table_["SRAD"] = daily_weather_table_["srad"].apply(wattspersqm_to_mgjpersqm)
    daily_weather_table_["TMAX"] = daily_weather_table_["tmax"].round(1)
    daily_weather_table_["TMIN"] = daily_weather_table_["tmin"].round(1)
    daily_weather_table_["RAIN"] = daily_weather_table_["prcp"].round(1)
    daily_weather_table_[["DEWP", "WIND", "PAR", "EVAP", "RHUM"]] = np.nan
    daily_weather_table_['TAVG'] = (daily_weather_table_['TMAX'] + daily_weather_table_['TMIN']) / 2

    tavg = daily_weather_table_['TAVG'].mean().round(1)

    daily_weather_table_ = daily_weather_table_[WTH_COLUMNS]
    wth_lines = format_table_to_WTH_lines(daily_weather_table_, is_file=False)

    location_encoding = geohash_encode(target_lat, target_lon)
    out_wth_fpath = os.path.join(outdir, f"{location_encoding}.WTH")

    LINE_1_2 = f"*WEATHER DATA : {location_encoding}\n\n"
    LINE_3 = "@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT\n"
    LINE_4 = f"{institution_code:>6}{target_lat:>9}{target_lon:>9}{-99.0:>6}{tavg:>6} -99.0 -99.0 -99.0\n"
    LINE_5 = "@DATE  SRAD  TMAX  TMIN  RAIN  DEWP  WIND   PAR  EVAP  RHUM\n"

    with open(out_wth_fpath, "w") as f:
        f.write(LINE_1_2)
        f.write(LINE_3)
        f.write(LINE_4)
        f.write(LINE_5)
        for line in wth_lines:
            f.write(line)
    print(f"File saved to {out_wth_fpath}")

    return {
        "wth_fpath": out_wth_fpath,
        "location_encoding": location_encoding,
        "year": year,
        "wth_table_df": daily_weather_table_,
    }


def location_to_SOL_file(db_params, target_lat, target_lon, outdir):
    """
    Generates a soil profile file in SOL format for a specified location and saves it to a specified directory.

    This function retrieves soil data for the nearest location to the specified latitude and longitude from a database,
    processes the data to create a SOL file that adheres to a specific format, and saves the file in the specified output directory.
    The function also returns a dictionary containing the file path and relevant metadata.

    Parameters:
    - db_params (dict): A dictionary containing the database connection parameters (e.g., host, port, user, password, dbname).
    - target_lat (float): The target latitude for which to retrieve soil data. The latitude is rounded to three decimal places.
    - target_lon (float): The target longitude for which to retrieve soil data. The longitude is rounded to three decimal places.
    - outdir (str): The directory where the SOL file will be saved.

    Returns:
    - dict: A dictionary containing the following keys:
        - "sol_fpath" (str): The full file path where the SOL file is saved.
        - "soil_profile_name" (str): The name of the soil profile retrieved from the database.
        - "location_encoding" (str): The geohash encoding of the specified latitude and longitude.
        - "sol_table_dict" (dict): A dictionary representation of the soil data retrieved from the database.

    Side Effects:
    - Writes a SOL file to the specified output directory.
    - Prints the file path where the SOL file is saved.

    Notes:
    - The function retrieves data from a database table using the `extract_serverless_db_table_for_location` function.
    - The SOL file format includes multiple lines with specific formats, including headers and detailed soil layer information.
    - The function handles specific soil layers (e.g., 5cm, 15cm, 30cm) and formats the data accordingly.
    - If no soil data is found for the nearest location, the function prints a message and returns None.

    Example Usage:
    ```
    db_params = {
        "host": "localhost",
        "port": 5432,
        "user": "username",
        "password": "password",
        "dbname": "soil_db"
    }
    result = location_to_SOL_file(db_params, 12.34, 56.78, "/path/to/output/dir")
    if result:
        print(result)
    ```
    """
    
    target_lat = round(target_lat, 3)
    target_lon = round(target_lon, 3)
    sol_table_, msg = extract_serverless_db_table_for_location(
        target_lat=target_lat, 
        target_lon=target_lon,
        data_type="sol",
    )

    if sol_table_ is None:
        print(msg)
        return
    
    if len(sol_table_) == 0:
        print("No soil data found for the nearest latitude and longitude.")
        return
    
    sol_table_as_dict = sol_table_.to_dict(orient='records')[0]

    line_header = "*SOILS: SoilGrids-for-DSSAT-10km v1.0 (US)\n\n"
    
    line_1 = f"*{sol_table_as_dict['soil_profile_name']:<14}{sol_table_as_dict['soil_data_source']:<6}{sol_table_as_dict['soil_texture']:<12}{sol_table_as_dict['soil_depth']:<7}{sol_table_as_dict['soil_series_name']}\n"
    line_2 = "@SITE        COUNTRY          LAT     LONG SCS Family\n"
    line_3 = f" {sol_table_as_dict['soil_site_name']:<12}{sol_table_as_dict['soil_country_name']:>7}{sol_table_as_dict['latitude']:>13}{sol_table_as_dict['longitude']:>9}{sol_table_as_dict['soil_classification_family']:>15}\n" 
    line_4 = "@ SCOM  SALB  SLU1  SLDR  SLRO  SLNF  SLPF  SMHB  SMPX  SMKE\n"
    line_5 = f"{sol_table_as_dict['soil_color']:>6}{sol_table_as_dict['soil_albedo']:>6.2f}{sol_table_as_dict['soil_evalopration_limit']:>6.2f}{sol_table_as_dict['soil_drainage_coefficient']:>6.2f}{sol_table_as_dict['soil_runoff_curve_no']:>6.2f}{sol_table_as_dict['soil_mineralization_factor']:>6.2f}{sol_table_as_dict['soil_photosynthesis_factor']:>6.2f}{sol_table_as_dict['soil_ph_in_buffer_determination_code']:>6}{sol_table_as_dict['soil_phosphorus_determination_code']:>6}{sol_table_as_dict['soil_potassium_determination_code']:>6}\n"
    line_6 = "@  SLB  SLMH  SLLL  SDUL  SSAT  SRGF  SSKS  SBDM  SLOC  SLCL  SLSI  SLCF  SLNI  SLHW  SLHB  SCEC  SADC\n"

    layer_rows_besides_soildepth = ['soil_master_horizon_Xcm', 'soil_lower_limit_Xcm', 'soil_upper_limit_drained_Xcm', 'soil_upper_limit_saturated_Xcm', 'soil_root_growth_factor_Xcm', 'soil_sat_hydraulic_conductivity_Xcm', 'soil_bulk_density_moist_Xcm', 'soil_organic_carbon_Xcm', 'soil_clay_Xcm', 'soil_silt_Xcm', 'soil_coarse_fraction_Xcm', 'soil_total_nitrogen_Xcm', 'soil_ph_in_water_Xcm', 'soil_ph_in_buffer_Xcm', 'soil_cation_exchange_capacity_Xcm', 'soil_sadc_Xcm' ]
    soil_layers = [5, 15, 30, 60, 100, 200]

    all_soil_layers_section = ""

    for soil_depth in soil_layers:
        line_for_this_depth = f"{soil_depth:>6}"
        for i, row in enumerate(layer_rows_besides_soildepth, start=1):
            row_str = row.replace("X", str(soil_depth))
            if i == 1:
                line_for_this_depth += f" {sol_table_as_dict[row_str]:<5}"
            elif i in [2, 3, 4]:
                line_for_this_depth += f"{float(sol_table_as_dict[row_str]):>6.3f}"
            elif i in [11, 14, 15, 16]:
                line_for_this_depth += f"{float(sol_table_as_dict[row_str]):>6.1f}"
            else:
                line_for_this_depth += f"{float(sol_table_as_dict[row_str]):>6.2f}"

        all_soil_layers_section += f"{line_for_this_depth}\n"

    location_encoding = geohash_encode(target_lat, target_lon)
    out_sol_fpath = os.path.join(outdir, f"{location_encoding}.SOL")

    with open(out_sol_fpath, "w") as f:
        f.write(line_header)
        f.write(line_1)
        f.write(line_2)
        f.write(line_3)
        f.write(line_4)
        f.write(line_5)
        f.write(line_6)
        f.write(all_soil_layers_section)
        f.write("\n")

    print(f"File saved to {out_sol_fpath}")

    return {
        "sol_fpath": out_sol_fpath,
        "soil_profile_name": sol_table_as_dict['soil_profile_name'],
        "location_encoding": location_encoding,
        "sol_table_dict": sol_table_as_dict,
    }



