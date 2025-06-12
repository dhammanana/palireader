import re

def highlight_words_in_sentence(sentence, nissaya):
    # Convert sentence to lowercase and remove special characters
    cleaned_sentence = re.sub(r'[,\-\.\!\?\;]', '', sentence.lower())
    
    # Split the sentence into words
    sentence_words = cleaned_sentence.split()
    
    # Create a new nissaya array to store modified pairs
    modified_nissaya = []
    
    # Process each [word, meaning] pair in nissaya
    for word, meaning in nissaya:
        # Check if the word (or phrase) exists in the sentence
        # Join sentence words to check for multi-word phrases
        if word.lower() in cleaned_sentence:
            highlighted_word = f'<span style="color:green">{word}</span>'
        else:
            highlighted_word = word
        # Append the modified pair to the new nissaya array
        modified_nissaya.append([highlighted_word, meaning])
    
    return modified_nissaya

def translate_ai(sentence, nissaya):
    pass