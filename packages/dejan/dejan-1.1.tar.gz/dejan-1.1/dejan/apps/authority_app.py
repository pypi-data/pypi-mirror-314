from dejan.authority import authority

def run_authority(domain):
    """
    Handles fetching authority metrics for a given domain.
    
    :param domain: The domain to analyze.
    """
    try:
        authority_value = authority(domain)
        print(f"Domain Authority for {domain}: {authority_value:.2f}")
    except ValueError as e:
        print(f"Error fetching authority: {e}")
