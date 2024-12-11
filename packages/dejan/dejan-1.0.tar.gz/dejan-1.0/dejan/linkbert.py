from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

class linkbert:
    def __init__(self, model_name="dejanseo/LinkBERT-mini"):
        """
        Initializes the LinkBERT model for inference.
        
        :param model_name: The name of the model on Hugging Face.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        
    def predict_link_tokens(self, text, group="token"):
        """
        Predicts link tokens in the provided text using the LinkBERT model.
        
        :param text: The input text to analyze.
        :param group: The grouping strategy ('subtoken', 'token', 'phrase').
        :return: A list of predicted link tokens or phrases.
        """
        # Tokenize the input text and run inference
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs).logits
        
        # Get the predictions
        predictions = torch.argmax(outputs, dim=-1)
        
        # Convert the token IDs back to tokens
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        link_tokens = []
        current_word = ""
        current_phrase = []
        in_phrase = False

        for i, token in enumerate(tokens):
            if token in ["[CLS]", "[SEP]", "[PAD]"]:
                continue

            # Remove the SentencePiece underscore for new words
            if token.startswith("▁"):
                token = token[1:]
                if current_word:
                    if in_phrase:
                        current_phrase.append(current_word)
                    else:
                        link_tokens.append(current_word)
                    current_word = ""

            if predictions[0][i] == 1:  # Assuming 1 is the label for link tokens
                if group == "subtoken":
                    link_tokens.append(token)
                elif group == "token":
                    current_word += token
                elif group == "phrase":
                    current_word += token
                    in_phrase = True
            else:
                if current_word:
                    if group == "token":
                        link_tokens.append(current_word)
                    elif group == "phrase":
                        current_phrase.append(current_word)
                    current_word = ""
                    in_phrase = False

                if group == "phrase" and current_phrase:
                    link_tokens.append(" ".join(current_phrase))
                    current_phrase = []

        # Handle any remaining word or phrase at the end
        if current_word:
            if group == "token":
                link_tokens.append(current_word)
            elif group == "phrase":
                current_phrase.append(current_word)

        if current_phrase:
            link_tokens.append(" ".join(current_phrase))

        return link_tokens
    
# Example usage
if __name__ == "__main__":
    linkbert_instance = linkbert()
    text = "LinkBERT is a model developed by Dejan Marketing designed to predict natural link placement within web content."
    
    # Group by subtoken
    links_subtoken = linkbert_instance.predict_link_tokens(text, group="subtoken")
    print(f"Predicted link tokens (subtoken): {links_subtoken}")
    
    # Group by token
    links_token = linkbert_instance.predict_link_tokens(text, group="token")
    print(f"Predicted link tokens (token): {links_token}")
    
    # Group by phrase
    links_phrase = linkbert_instance.predict_link_tokens(text, group="phrase")
    print(f"Predicted link tokens (phrase): {links_phrase}")
