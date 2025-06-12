import json
import base64

class SmallTool:
    @staticmethod
    def convert_func(content):
        # Split the content by '။' (Myanmar sentence-ending punctuation)
        segments = content.split('။')
        processed_segments = []
        
        for segment in segments:
            if not segment.strip():
                continue  # Skip empty segments
            
            # Check if the segment contains '၊' (Myanmar comma-like punctuation)
            if '၊' in segment:
                # Split by '၊' and ensure exactly two parts
                parts = segment.split('၊', 1)
                if len(parts) == 2:
                    pali, meaning = parts
                    # Create JSON object
                    data = {
                        "pali": pali.strip(),
                        "meaning": meaning.strip(),
                        "language": "my"
                    }
                    # Convert to JSON string
                    json_str = json.dumps(data, ensure_ascii=False)
                    # Base64 encode the JSON string
                    base64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
                    # Wrap in {{nissaya|<base64>}}
                    processed = f"{{{{nissaya|{base64_str}}}}}"
                else:
                    # If splitting doesn't yield two parts, keep the segment unchanged
                    processed = segment
            else:
                # If no '၊', keep the segment unchanged
                processed = segment
            
            processed_segments.append(processed)
        
        # Join segments with newline
        return '\n'.join(processed_segments)

if __name__ == "__main__":
    # Example input
    input_text = (
        "မနုဿဒေ-၀ဗြဟ္မတ္တိယေါ၊လူံစဥ်းစိမ်နတ်စဥ်းစိမ်ဗြဟ္မာ့စဥ်စိမ်တို့ကို။"
        "အာသာဒေန္တာပိယဖြစ်-ב-တန်ဘာဖြစ်ဖ-2025-02၊သာယာကြကုန်သော်လည်း။"
        "သုခ‌ေ၀ဒနတ္တာယဧ၀၊ဌာသာလျင်။"
        "အဿာဒေန်တိ၊သာယာကုန်၏။"
    )
    result = SmallTool.convert_func(input_text)
    print(result)