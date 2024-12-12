from dejan.linkbert import linkbert

def run_linkbert(text=None, group="phrase"):
    """
    Runs the LinkBERT model with given text and grouping strategy.
    
    :param text: The input text to analyze. If None, a default text will be used.
    :param group: The grouping strategy ('subtoken', 'token', 'phrase'). Default is 'phrase'.
    """
    # If text is not provided, use a default text
    if text is None:
        text = "LinkBERT is a model developed by Dejan Marketing designed to predict natural link placement within web content."
    
    # Initialize the linkbert model
    model = linkbert()

    # Perform prediction based on selected grouping strategy
    links = model.predict_link_tokens(text, group=group)

    # Print the results
    print(f"Predicted link tokens ({group}):")
    for link in links:
        print(link)
