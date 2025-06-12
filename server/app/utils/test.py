from logger import Logger

logger = Logger(bold_numbers=True)
def test_logger():
    logger.debug("This is a [debug] message1.")
    logger.info("This is an [info] message3.")
    logger.warning("This is a [warning] message5/6.")
    logger.error("This4|3 is an [error] message.")
    logger.critical("This232/3333 is a [critical] message.")
    logger.info("Test completed [successfully].")

import unicodedata

def roman_to_sinhala(text):
    """
    Convert Pali Roman script to Sinhala.

    Args:
        text: Input string in Pali Roman script (e.g., 'saṃvaṇṇanā').
    
    Returns:
        String in Sinhala script (e.g., 'සංවණ්ණනා').
    """
    # Normalize to NFC to handle precomposed characters
    text = unicodedata.normalize('NFC', text.lower())

    # Define mappings
    consonant_map = {
        'k': 'ක', 'g': 'ග', 'c': 'ච', 'j': 'ජ', 'ṭ': 'ට', 'ḍ': 'ඩ', 't': 'ත',
        'd': 'ද', 'p': 'ප', 'b': 'බ', 'm': 'ම', 'y': 'ය', 'r': 'ර', 'l': 'ල',
        'v': 'ව', 's': 'ස', 'h': 'හ', 'n': 'න', 'ñ': 'ඤ', 'ṅ': 'ඞ', 'ṇ': 'ණ',
        'ḷ': 'ළ'
    }
    special_map = {'ṃ': 'ං', 'ṁ': 'ං'}  # Handle both 'ṃ' and 'ṁ' for anusvara
    vowel_map = {
        'a': '', 'ā': 'ා', 'i': 'ි', 'ī': 'ී', 'u': 'ු', 'ū': 'ූ', 'e': 'ෙ', 'o': 'ො'
    }
    independent_vowel_map = {
        'a': 'අ', 'ā': 'ආ', 'i': 'ඉ', 'ī': 'ඊ', 'u': 'උ', 'ū': 'ඌ', 'e': 'එ', 'o': 'ඔ'
    }

    output = []
    i = 0
    while i < len(text):
        char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else None

        # Handle special characters
        if char in special_map:
            output.append(special_map[char])
            i += 1
            continue

        # Handle long vowels (e.g., 'ā', 'ī')
        if char in 'aiueo' and next_char == '̄':
            char = char + '̄'
            i += 2
        else:
            i += 1

        # Handle vowels
        if char in vowel_map:
            # Use dependent vowel if last character is a consonant
            if output and 'ක' <= output[-1] <= 'ෆ':
                output.append(vowel_map[char])
            else:
                output.append(independent_vowel_map[char])
            continue

        # Handle consonants
        if char in consonant_map:
            output.append(consonant_map[char])
            # Add virama if next character is a consonant or special character
            if next_char and (next_char in consonant_map or next_char in special_map):
                output.append('්')
            continue

        # Append unmapped characters (e.g., spaces, punctuation)
        output.append(char)

    return ''.join(output)

# Test the function
test_text = "saṃvaṇṇanārambhe ratanattayavandanā saṃvaṇṇetabbassa dhammassa pabhavanissayavisuddhipaṭivedanatthaṃ"
print(roman_to_sinhala(test_text))

if __name__ == "__main__":
    test_logger()
    print("Logger test completed.")