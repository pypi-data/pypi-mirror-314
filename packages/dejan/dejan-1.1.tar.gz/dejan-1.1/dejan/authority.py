import requests

def clean_domain(domain):
    """
    Cleans and formats the domain name.

    :param domain: The raw domain input.
    :return: The cleaned domain name.
    """
    # Remove http://, https://, www., and any path, convert to lowercase
    domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').lower()
    # Extract the base domain
    domain = domain.split('/')[0]
    return domain

def authority(domain):
    """
    Fetches the authority metric for a given domain.

    :param domain: The domain to analyze.
    :return: The authority metric as a float.
    :raises ValueError: If the API response is not valid or the domain is incorrect.
    """
    domain = clean_domain(domain)  # Clean the domain before using it in the API request
    url = f"https://dev.dejan.cc/data/?host={domain}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if 'authority' in data:
            return data['authority']
        else:
            raise ValueError(f"Error: {data.get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {e}")

# Example usage in Python
if __name__ == "__main__":
    domain = "http://dejan.ai/"
    try:
        authority_value = authority(domain)
        print(f"Domain Authority for {domain}: {authority_value:.2f}")
    except ValueError as e:
        print(e)
