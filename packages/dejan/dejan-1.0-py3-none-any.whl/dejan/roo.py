import requests
import pandas as pd

# Mapping search engine codes to their descriptions and URLs
SEARCH_ENGINES = {
    2: "https://algoroo.com/API_v2.php?key=W3ROMzRGLxSRHHtPL12PXOPDuJiNtaSy&user=algoroo@algoroo.com&se=2",  # Google.com (Desktop)
    3: "https://algoroo.com/API_v2.php?key=W3ROMzRGLxSRHHtPL12PXOPDuJiNtaSy&user=algoroo@algoroo.com&se=3",  # Google.com.au (Desktop)
    4: "https://algoroo.com/API_v2.php?key=W3ROMzRGLxSRHHtPL12PXOPDuJiNtaSy&user=algoroo@algoroo.com&se=4",  # Google.com (Mobile)
    5: "https://algoroo.com/API_v2.php?key=W3ROMzRGLxSRHHtPL12PXOPDuJiNtaSy&user=algoroo@algoroo.com&se=5"   # Google.com.au (Mobile)
}

def roo(search_engine, as_dataframe=False):
    """
    Fetches the roo data for the specified search engine.

    :param search_engine: The integer key representing the search engine (2, 3, 4, or 5).
    :param as_dataframe: If True, converts the JSON data to a pandas DataFrame.
    :return: The JSON data or a pandas DataFrame, depending on as_dataframe.
    
    :raises ValueError: If an invalid search engine is provided.
    :raises requests.HTTPError: If the API request fails.
    """
    if search_engine not in SEARCH_ENGINES:
        raise ValueError(f"Invalid search engine selected. Choose from: {list(SEARCH_ENGINES.keys())}")
    
    url = SEARCH_ENGINES[search_engine]
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()

    if as_dataframe:
        return convert_to_dataframe(data)
    return data

def convert_to_dataframe(data):
    """
    Converts the roo JSON data into a pandas DataFrame.

    :param data: The JSON data returned by the API.
    :return: A pandas DataFrame containing the processed data.
    """
    # Check the structure of the data to determine how to convert it to a DataFrame
    if isinstance(data, list):
        # If the data is a list of dictionaries, convert it directly
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # If the data is a dictionary, try to find the relevant data to convert
        if 'records' in data:
            df = pd.DataFrame(data['records'])
        else:
            # Flatten the dictionary and create a DataFrame with one row
            df = pd.json_normalize(data)
    else:
        raise ValueError("The structure of the data is not supported for conversion to DataFrame.")
    
    return df
