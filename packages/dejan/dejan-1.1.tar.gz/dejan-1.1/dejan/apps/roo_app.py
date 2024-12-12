from dejan.roo import roo
from datetime import datetime, timedelta
import pandas as pd

def run_roo(date_or_days, region="us", device="mobile"):
    """
    Handles the main logic for fetching ROO data based on the user's input.
    
    :param date_or_days: A string that is either a specific date (YYYY-MM-DD) or the number of days (7, 30, etc.)
    :param region: The region for the search engine (us or au).
    :param device: The device type for the search engine (desktop or mobile).
    """
    try:
        search_engine = determine_search_engine(region, device)

        # Try to parse as a date first
        try:
            specific_date = datetime.strptime(date_or_days, '%Y-%m-%d').date()
            data = get_roo_data_for_date(specific_date, search_engine)
        except ValueError:
            # If not a date, treat it as a number of days
            days = int(date_or_days)
            data = get_roo_data_for_days(days, search_engine)
        
        if isinstance(data, pd.DataFrame):
            print(data.to_string(index=False))
        else:
            print(f"Error: {data}")
    except Exception as e:
        print(f"Error fetching ROO data: {e}")

def get_roo_data_for_date(specific_date, search_engine):
    """
    Fetches the ROO data for a specific date.

    :param specific_date: The specific date for which to fetch data.
    :param search_engine: The search engine ID.
    :return: A DataFrame with the ROO data.
    """
    data = roo(search_engine, as_dataframe=True)
    data['rooDate'] = pd.to_datetime(data['rooDate']).dt.date
    filtered_data = data[data['rooDate'] == specific_date]
    return filtered_data

def get_roo_data_for_days(days, search_engine):
    """
    Fetches the ROO data for the last 'n' days.

    :param days: The number of days to look back.
    :param search_engine: The search engine ID.
    :return: A DataFrame with the most recent 'n' days of ROO data.
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    data = roo(search_engine, as_dataframe=True)
    data['rooDate'] = pd.to_datetime(data['rooDate']).dt.date
    filtered_data = data[(data['rooDate'] >= start_date) & (data['rooDate'] <= end_date)]
    
    # Sort by date in descending order and get the top 'n' rows
    filtered_data = filtered_data.sort_values(by='rooDate', ascending=False).head(days)
    
    return filtered_data

def determine_search_engine(region, device):
    """
    Determines the search engine code based on the region and device.

    :param region: The region for the search engine (us or au).
    :param device: The device type for the search engine (desktop or mobile).
    :return: The search engine ID.
    """
    search_engine_map = {
        ("us", "desktop"): 2,
        ("au", "desktop"): 3,
        ("us", "mobile"): 4,
        ("au", "mobile"): 5,
    }
    return search_engine_map.get((region.lower(), device.lower()), 4)  # Default to us mobile
