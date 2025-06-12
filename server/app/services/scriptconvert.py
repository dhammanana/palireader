import re
import unicodedata
"""
Pali Script Converter Library

This library provides functionality to convert Pali text between different scripts.
Converted from JavaScript to Python.
Code was converted from tipitaka.lk node script.
"""

# ISO 15924 script codes
class Script:
    SI = 'Sinh'    # Sinhala
    HI = 'Deva'    # Devanagari
    RO = 'Latn'    # Roman/Latin
    THAI = 'Thai'  # Thai
    LAOS = 'Laoo'  # Lao
    MY = 'Mymr'    # Myanmar
    KM = 'Khmr'    # Khmer
    BENG = 'Beng'  # Bengali
    GURM = 'Guru'  # Gurmukhi
    THAM = 'Lana'  # Tai Tham
    GUJA = 'Gujr'  # Gujarati
    TELU = 'Telu'  # Telugu
    KANN = 'Knda'  # Kannada
    MALA = 'Mlym'  # Malayalam
    BRAH = 'Brah'  # Brahmi
    TIBT = 'Tibt'  # Tibetan
    CYRL = 'Cyrl'  # Cyrillic

SCRIPT_LANG = {
    'Sinh': Script.SI,    # Sinhala
    'Deva': Script.HI,    # Devanagari
    'Latn': Script.RO,    # Roman/Latin
    'Thai': Script.THAI,  # Thai
    'Laoo': Script.LAOS,  # Lao
    'Mymr': Script.MY,    # Myanmar
    'Khmr': Script.KM,    # Khmer
    'Beng': Script.BENG,  # Bengali
    'Guru': Script.GURM,  # Gurmukhi
    'Lana': Script.THAM,  # Tai Tham
    'Gujr': Script.GUJA,  # Gujarati
    'Telu': Script.TELU,  # Telugu
    'Knda': Script.KANN,  # Kannada
    'Mlym': Script.MALA,  # Malayalam
    'Brah': Script.BRAH,  # Brahmi
    'Tibt': Script.TIBT,  # Tibetan
    'Cyrl': Script.CYRL,  # Cyrillic
}

# Script information dictionary
PALI_SCRIPT_INFO = {
    Script.SI: ['Sinhala', 'සිංහල', [(0x0d80, 0x0dff)], {'locale': 'si', 'localeName': 'සිංහල'}],
    Script.HI: ['Devanagari', 'नागरी', [(0x0900, 0x097f)], {'locale': 'hi', 'localeName': 'हिन्दी'}],
    Script.RO: ['Roman', 'Roman', [(0x0000, 0x017f), (0x1e00, 0x1eff)], {'locale': 'en', 'localeName': 'English'}],
    Script.THAI: ['Thai', 'ไทย', [(0x0e00, 0x0e7f), 0xf70f, 0xf700], {'locale': 'th', 'localeName': 'ไทย'}],
    Script.LAOS: ['Laos', 'ລາວ', [(0x0e80, 0x0eff)], {'locale': 'lo', 'localeName': 'ລາວ'}],
    Script.MY: ['Myanmar', 'ဗမာစာ', [(0x1000, 0x107f)], {'locale': 'my', 'localeName': 'ဗမာစာ'}],
    Script.KM: ['Khmer', 'ភាសាខ្មែរ', [(0x1780, 0x17ff)], {'locale': 'km', 'localeName': 'ភាសាខ្មែរ'}],
    Script.BENG: ['Bengali', 'বাংলা', [(0x0980, 0x09ff)], {'locale': 'bn', 'localeName': 'বাংলা', 'group': 'indian'}],
    Script.GURM: ['Gurmukhi', 'ਗੁਰਮੁਖੀ', [(0x0a00, 0x0a7f)], {'locale': 'pa', 'localeName': 'ਪੰਜਾਬੀ', 'group': 'indian'}],
    Script.GUJA: ['Gujarati', 'ગુજરાતી', [(0x0a80, 0x0aff)], {'locale': 'gu', 'localeName': 'ગુજરાતી', 'group': 'indian'}],
    Script.TELU: ['Telugu', 'తెలుగు', [(0x0c00, 0x0c7f)], {'locale': 'te', 'localeName': 'తెలుగు', 'group': 'indian'}],
    Script.KANN: ['Kannada', 'ಕನ್ನಡ', [(0x0c80, 0x0cff)], {'locale': 'kn', 'localeName': 'ಕನ್ನಡ', 'group': 'indian'}],
    Script.MALA: ['Malayalam', 'മലയാളം', [(0x0d00, 0x0d7f)], {'locale': 'ml', 'localeName': 'മലയാളം', 'group': 'indian'}],
    Script.THAM: ['Tai Tham', 'Tai Tham LN', [(0x1a20, 0x1aaf)], {'locale': 'th', 'localeName': 'ไทย (Lanna)', 'group': 'other'}],
    Script.BRAH: ['Brahmi', 'Brāhmī', [(0xd804, 0xd804), (0xdc00, 0xdc7f)], {'locale': 'hi', 'localeName': 'हिन्दी (Brah)', 'group': 'other'}],
    Script.TIBT: ['Tibetan', 'བོད་སྐད།', [(0x0f00, 0x0fff)], {'locale': 'bo', 'localeName': 'བོད་སྐད།', 'group': 'other'}],
    Script.CYRL: ['Cyrillic', 'кириллица', [(0x0400, 0x04ff), (0x0300, 0x036f)], {'locale': 'ru', 'localeName': 'ру́сский', 'group': 'other'}],
}

# Script index dictionary
SCRIPT_INDEX = {
    Script.SI: 0,
    Script.HI: 1,
    Script.RO: 2,
    Script.THAI: 3,
    Script.LAOS: 4,
    Script.MY: 5,
    Script.KM: 6,
    Script.BENG: 7,
    Script.GURM: 8,
    Script.THAM: 9,
    Script.GUJA: 10,
    Script.TELU: 11,
    Script.KANN: 12,
    Script.MALA: 13,
    Script.BRAH: 14,
    Script.TIBT: 15,
    Script.CYRL: 16,
}

# Character mappings
SPECIALS = [
    # independent vowels
    ['අ', 'अ', 'a', 'อ', 'ອ', 'အ', 'អ', 'অ', 'ਅ', '\u1A4B', 'અ', 'అ', 'ಅ', 'അ', '𑀅', 'ཨ', 'а'],
    ['ආ', 'आ', 'ā', 'อา', 'ອາ', 'အာ', 'អា', 'আ', 'ਆ', '\u1A4C', 'આ', 'ఆ', 'ಆ', 'ആ', '𑀆', 'ཨཱ', 'а̄'],
    ['ඉ', 'इ', 'i', 'อิ', 'ອິ', 'ဣ', 'ឥ', 'ই', 'ਇ', '\u1A4D', 'ઇ', 'ఇ', 'ಇ', 'ഇ', '𑀇', 'ཨི', 'и'],
    ['ඊ', 'ई', 'ī', 'อี', 'ອີ', 'ဤ', 'ឦ', 'ঈ', 'ਈ', '\u1A4E', 'ઈ', 'ఈ', 'ಈ', 'ഈ', '𑀈', 'ཨཱི', 'ӣ'],
    ['උ', 'उ', 'u', 'อุ', 'ອຸ', 'ဥ', 'ឧ', 'উ', 'ਉ', '\u1A4F', 'ઉ', 'ఉ', 'ಉ', 'ഉ', '𑀉', 'ཨུ', 'у'],
    ['ඌ', 'ऊ', 'ū', 'อู', 'ອູ', 'ဦ', 'ឩ', 'ঊ', 'ਊ', '\u1A50', 'ઊ', 'ఊ', 'ಊ', 'ഊ', '𑀊', 'ཨཱུ', 'ӯ'],
    ['එ', 'ए', 'e', 'อเ', 'ອເ', 'ဧ', 'ឯ', 'এ', 'ਏ', '\u1A51', 'એ', 'ఏ', 'ಏ', 'ഏ', '𑀏', 'ཨེ', 'е'],
    ['ඔ', 'ओ', 'o', 'อโ', 'ອໂ', 'ဩ', 'ឱ', 'ও', 'ਓ', '\u1A52', 'ઓ', 'ఓ', 'ಓ', 'ഓ', '𑀑', 'ཨོ', 'о'],
    # various signs
    # niggahita - anusawara
    ['ං', 'ं', 'ṃ', '\u0E4D', '\u0ECD', 'ံ', 'ំ', 'ং', 'ਂ', '\u1A74', 'ં', 'ం', 'ಂ', 'ം', '𑀁', '\u0F7E', 'м̣'],
    # visarga - not in pali but deva original text has it
    ['ඃ', 'ः', 'ḥ', 'ะ', 'ະ', 'း', 'ះ', 'ঃ', 'ਃ', '\u1A61', 'ઃ', 'ః', 'ಃ', 'ഃ', '𑀂', '\u0F7F', 'х̣'],
    # virama (al - hal). roman/cyrillic need special handling
    ['්', '्', '', '\u0E3A', '\u0EBA', '္', '្', '্', '੍', '\u1A60', '્', '్', '್', '്', '\uD804\uDC46', '\u0F84', ''],
    # digits
    ['0', '०', '0', '๐', '໐', '၀', '០', '০', '੦', '\u1A90', '૦', '౦', '೦', '൦', '𑁦', '༠', '0'],
    ['1', '१', '1', '๑', '໑', '၁', '១', '১', '੧', '\u1A91', '૧', '౧', '೧', '൧', '𑁧', '༡', '1'],
    ['2', '२', '2', '๒', '໒', '၂', '២', '২', '੨', '\u1A92', '૨', '౨', '೨', '൨', '𑁨', '༢', '2'],
    ['3', '३', '3', '๓', '໓', '၃', '៣', '৩', '੩', '\u1A93', '૩', '౩', '೩', '൩', '𑁩', '༣', '3'],
    ['4', '४', '4', '๔', '໔', '၄', '៤', '৪', '੪', '\u1A94', '૪', '౪', '೪', '൪', '𑁪', '༤', '4'],
    ['5', '५', '5', '๕', '໕', '၅', '៥', '৫', '੫', '\u1A95', '૫', '౫', '೫', '൫', '𑁫', '༥', '5'],
    ['6', '६', '6', '๖', '໖', '၆', '៦', '৬', '੬', '\u1A96', '૬', '౬', '೬', '൬', '𑁬', '༦', '6'],
    ['7', '७', '7', '๗', '໗', '၇', '៧', '৭', '੭', '\u1A97', '૭', '౭', '೭', '൭', '𑁭', '༧', '7'],
    ['8', '८', '8', '๘', '໘', '၈', '៨', '৮', '੮', '\u1A98', '૮', '౮', '೮', '൮', '𑁮', '༨', '8'],
    ['9', '९', '9', '๙', '໙', '၉', '៩', '৯', '੯', '\u1A99', '૯', '౯', '೯', '൯', '𑁯', '༩', '9'],
]

CONSOS = [
    # velar stops
    ['ක', 'क', 'k', 'ก', 'ກ', 'က', 'ក', 'ক', 'ਕ', '\u1A20', 'ક', 'క', 'ಕ', 'ക', '𑀓', 'ཀ', 'к'],
    ['ඛ', 'ख', 'kh', 'ข', 'ຂ', 'ခ', 'ខ', 'খ', 'ਖ', '\u1A21', 'ખ', 'ఖ', 'ಖ', 'ഖ', '𑀔', 'ཁ', 'кх'],
    ['ග', 'ग', 'g', 'ค', 'ຄ', 'ဂ', 'គ', 'গ', 'ਗ', '\u1A23', 'ગ', 'గ', 'ಗ', 'ഗ', '𑀕', 'ག', 'г'],
    ['ඝ', 'घ', 'gh', 'ฆ', '\u0E86', 'ဃ', 'ឃ', 'ঘ', 'ਘ', '\u1A25', 'ઘ', 'ఘ', 'ಘ', 'ഘ', '𑀖', 'གྷ', 'гх'],
    ['ඞ', 'ङ', 'ṅ', 'ง', 'ງ', 'င', 'ង', 'ঙ', 'ਙ', '\u1A26', 'ઙ', 'ఙ', 'ಙ', 'ങ', '𑀗', 'ང', 'н̇'],
    # palatal stops
    ['ච', 'च', 'c', 'จ', 'ຈ', 'စ', 'ច', 'চ', 'ਚ', '\u1A27', 'ચ', 'చ', 'ಚ', 'ച', '𑀘', 'ཙ', 'ч'],
    ['ඡ', 'छ', 'ch', 'ฉ', '\u0E89', 'ဆ', 'ឆ', 'ছ', 'ਛ', '\u1A28', 'છ', 'ఛ', 'ಛ', 'ഛ', '𑀙', 'ཚ', 'чх'],
    ['ජ', 'ज', 'j', 'ช', 'ຊ', 'ဇ', 'ជ', 'জ', 'ਜ', '\u1A29', 'જ', 'జ', 'ಜ', 'ജ', '𑀚', 'ཛ', 'дж'],
    ['ඣ', 'झ', 'jh', 'ฌ', '\u0E8C', 'ဈ', 'ឈ', 'ঝ', 'ਝ', '\u1A2B', 'ઝ', 'ఝ', 'ಝ', 'ഝ', '𑀛', 'ཛྷ', 'джх'],
    ['ඤ', 'ञ', 'ñ', 'ญ', '\u0E8E', 'ဉ', 'ញ', 'ঞ', 'ਞ', '\u1A2C', 'ઞ', 'ఞ', 'ಞ', 'ഞ', '𑀜', 'ཉ', 'н̃'],
    # retroflex stops
    ['ට', 'ट', 'ṭ', 'ฏ', '\u0E8F', 'ဋ', 'ដ', 'ট', 'ਟ', '\u1A2D', 'ટ', 'ట', 'ಟ', 'ട', '𑀝', 'ཊ', 'т̣'],
    ['ඨ', 'ठ', 'ṭh', 'ฐ', '\u0E90', 'ဌ', 'ឋ', 'ঠ', 'ਠ', '\u1A2E', 'ઠ', 'ఠ', 'ಠ', 'ഠ', '𑀞', 'ཋ', 'т̣х'],
    ['ඩ', 'ड', 'ḍ', 'ฑ', '\u0E91', 'ဍ', 'ឌ', 'ড', 'ਡ', '\u1A2F', 'ડ', 'డ', 'ಡ', 'ഡ', '𑀟', 'ཌ', 'д̣'],
    ['ඪ', 'ढ', 'ḍh', 'ฒ', '\u0E92', 'ဎ', 'ឍ', 'ঢ', 'ਢ', '\u1A30', 'ઢ', 'ఢ', 'ಢ', 'ഢ', '𑀠', 'ཌྷ', 'д̣х'],
    ['ණ', 'ण', 'ṇ', 'ณ', '\u0E93', 'ဏ', 'ណ', 'ণ', 'ਣ', '\u1A31', 'ણ', 'ణ', 'ಣ', 'ണ', '𑀡', 'ཎ', 'н̣'],
    # dental stops
    ['ත', 'त', 't', 'ต', 'ຕ', 'တ', 'ត', 'ত', 'ਤ', '\u1A32', 'ત', 'త', 'ತ', 'ത', '𑀢', 'ཏ', 'т'],
    ['ථ', 'थ', 'th', 'ถ', 'ຖ', 'ထ', 'ថ', 'থ', 'ਥ', '\u1A33', 'થ', 'థ', 'ಥ', 'ഥ', '𑀣', 'ཐ', 'тх'],
    ['ද', 'द', 'd', 'ท', 'ທ', 'ဒ', 'ទ', 'দ', 'ਦ', '\u1A34', 'દ', 'ద', 'ದ', 'ദ', '𑀤', 'ད', 'д'],
    ['ධ', 'ध', 'dh', 'ธ', '\u0E98', 'ဓ', 'ធ', 'ধ', 'ਧ', '\u1A35', 'ધ', 'ధ', 'ಧ', 'ധ', '𑀥', 'དྷ', 'дх'],
    ['න', 'न', 'n', 'น', 'ນ', 'န', 'ន', 'ন', 'ਨ', '\u1A36', 'ન', 'న', 'ನ', 'ന', '𑀦', 'ན', 'н'],
    # labial stops
    ['ප', 'प', 'p', 'ป', 'ປ', 'ပ', 'ប', 'প', 'ਪ', '\u1A38', 'પ', 'ప', 'ಪ', 'പ', '𑀧', 'པ', 'п'],
    ['ඵ', 'फ', 'ph', 'ผ', 'ຜ', 'ဖ', 'ផ', 'ফ', 'ਫ', '\u1A39', 'ફ', 'ఫ', 'ಫ', 'ഫ', '𑀨', 'ཕ', 'пх'],
    ['බ', 'ब', 'b', 'พ', 'ພ', 'ဗ', 'ព', 'ব', 'ਬ', '\u1A3B', 'બ', 'బ', 'ಬ', 'ബ', '𑀩', 'བ', 'б'],
    ['භ', 'भ', 'bh', 'ภ', '\u0EA0', 'ဘ', 'ភ', 'ভ', 'ਭ', '\u1A3D', 'ભ', 'భ', 'ಭ', 'ഭ', '𑀪', 'བྷ', 'бх'],
    ['ම', 'म', 'm', 'ม', 'ມ', 'မ', 'ម', 'ম', 'ਮ', '\u1A3E', 'મ', 'మ', 'ಮ', 'മ', '𑀫', 'མ', 'м'],
    # liquids, fricatives, etc.
    ['ය', 'य', 'y', 'ย', 'ຍ', 'ယ', 'យ', 'য', 'ਯ', '\u1A3F', 'ય', 'య', 'ಯ', 'യ', '𑀬', 'ཡ', 'й'],
    ['ර', 'र', 'r', 'ร', 'ຣ', 'ရ', 'រ', 'র', 'ਰ', '\u1A41', 'ર', 'ర', 'ರ', 'ര', '𑀭', 'ར', 'р'],
    ['ල', 'ल', 'l', 'ล', 'ລ', 'လ', 'ល', 'ল', 'ਲ', '\u1A43', 'લ', 'ల', 'ಲ', 'ല', '𑀮', 'ལ', 'л'],
    ['ළ', 'ळ', 'ḷ', 'ฬ', '\u0EAC', 'ဠ', 'ឡ', 'ল়', 'ਲ਼', '\u1A4A', 'ળ', 'ళ', 'ಳ', 'ള', '𑀴', 'ལ༹', 'л̣'],
    ['ව', 'व', 'v', 'ว', 'ວ', 'ဝ', 'វ', 'ৰ', 'ਵ', '\u1A45', 'વ', 'వ', 'ವ', 'വ', '𑀯', 'ཝ', 'в'],
    ['ස', 'स', 's', 'ส', 'ສ', 'သ', 'ស', 'স', 'ਸ', '\u1A48', 'સ', 'స', 'ಸ', 'സ', '𑀲', 'ས', 'с'],
    ['හ', 'ह', 'h', 'ห', 'ຫ', 'ဟ', 'ហ', 'হ', 'ਹ', '\u1A49', 'હ', 'హ', 'ಹ', 'ഹ', '𑀳', 'ཧ', 'х'],
]

VOWELS = [
    # dependent vowel signs
    ['ා', 'ा', 'ā', 'า', 'າ', 'ာ', 'ា', 'া', 'ਾ', '\u1A63', 'ા', 'ా', 'ಾ', 'ാ', '𑀸', '\u0F71', 'а̄'],
    ['ි', 'ि', 'i', '\u0E34', '\u0EB4', 'ိ', 'ិ', 'ি', 'ਿ', '\u1A65', 'િ', 'ి', 'ಿ', 'ി', '𑀺', '\u0F72', 'и'],
    ['ී', 'ी', 'ī', '\u0E35', '\u0EB5', 'ီ', 'ី', 'ী', 'ੀ', '\u1A66', 'ી', 'ీ', 'ೀ', 'ീ', '𑀻', '\u0F71\u0F72', 'ӣ'],
    ['ු', 'ु', 'u', '\u0E38', '\u0EB8', 'ု', 'ុ', 'ু', 'ੁ', '\u1A69', 'ુ', 'ు', 'ು', 'ു', '𑀼', '\u0F74', 'у'],
    ['ූ', 'ू', 'ū', '\u0E39', '\u0EB9', 'ူ', 'ូ', 'ূ', 'ੂ', '\u1A6A', 'ૂ', 'ూ', 'ೂ', 'ൂ', '𑀽', '\u0F71\u0F74', 'ӯ'],
    # for th/lo - should appear in front
    ['ෙ', 'े', 'e', 'เ', 'ເ', 'ေ', 'េ', 'ে', 'ੇ', '\u1A6E', 'ે', 'ే', 'ೇ', 'േ', '𑁂', '\u0F7A', 'е'],
    # for th/lo - should appear in front
    ['ො', 'ो', 'o', 'โ', 'ໂ', 'ော', 'ោ', 'ো', 'ੋ', '\u1A6E\u1A63', 'ો', 'ో', 'ೋ', 'ോ', '𑁄', '\u0F7C', 'о'],
]

# Sinhala consonant range
SINH_CONSO_RANGE = 'ක-ෆ'
# Thai consonant range
THAI_CONSO_RANGE = 'ก-ฮ'
# Lao consonant range
LAO_CONSO_RANGE = 'ກ-ຮ'
# Myanmar consonant range
MYMR_CONSO_RANGE = 'က-ဠ'

# Independent vowel to dependent vowel mapping
IV_TO_DV = {
    'අ': '', 'ආ': 'ා', 'ඉ': 'ි', 'ඊ': 'ී', 
    'උ': 'ු', 'ඌ': 'ූ', 'එ': 'ෙ', 'ඔ': 'ො'
}

def get_script_for_code(char_code):
    """
    Determine the script of a character based on its Unicode code point.
    
    Args:
        char_code: Unicode code point of the character.
        
    Returns:
        Script identifier or -1 if not found.
    """
    for script, info in PALI_SCRIPT_INFO.items():
        for range_info in info[2]:
            if isinstance(range_info, tuple) and char_code >= range_info[0] and char_code <= range_info[1]:
                return script
            elif isinstance(range_info, int) and char_code == range_info:
                return script
    return -1
'''
def prepare_hash_maps(from_index, to_index, use_vowels=True):
    """
    Prepare mapping tables for character conversion.

    Args:
        from_index: Index in the SCRIPT_INDEX for the source script.
        to_index: Index in the SCRIPT_INDEX for the target script.
        use_vowels: Boolean indicating whether to include vowels in the mapping.

    Returns:
        List of tuples, each containing the length of the input character sequence
        and a dictionary mapping input characters to output characters.
    """
    full_array = CONSOS + SPECIALS
    if use_vowels:
        full_array += VOWELS

    final_array = [[], [], []]  # Max 3 for different character lengths
    for val in full_array:
        if from_index < len(val) and from_index > -1:  # Check if the source character exists
            # Group by length of the source character
            final_array[len(val[from_index]) - 1].append((val[from_index], val[to_index]))

    # Filter non-empty arrays, create (length, dict) tuples, and sort by length (descending)
    return [(len(arr[0][0]), dict(arr)) for arr in final_array if arr][::-1]

def replace_by_maps(input_text, hash_maps):
    """
    Replace characters in the input text using the provided mapping tables.

    Args:
        input_text: String to convert.
        hash_maps: List of tuples containing (length, mapping_dict).

    Returns:
        Converted string.
    """
    output_array = []
    b = 0
    while b < len(input_text):
        match = False
        for length, hash_map in hash_maps:
            in_chars = input_text[b:b + length]
            if in_chars in hash_map:
                output_array.append(hash_map[in_chars])  # Can be empty string
                b += length
                match = True
                break
        if not match:
            output_array.append(input_text[b])
            b += 1
    return ''.join(output_array)
'''

def prepare_hash_maps(from_index, to_index, use_vowels=True):
    """
    Prepare mapping tables for character conversion.

    Args:
        from_index: Index in the SCRIPT_INDEX for the source script.
        to_index: Index in the SCRIPT_INDEX for the target script.
        use_vowels: Boolean indicating whether to include vowels in the mapping.

    Returns:
        List of tuples, each containing the length of the input character sequence
        and a dictionary mapping input characters to output characters.
    """
    full_array = CONSOS + SPECIALS
    if use_vowels:
        full_array += VOWELS

    final_array = [[], [], []]  # Max 3 for different character lengths
    for val in full_array:
        if from_index < len(val) and val[from_index]:  # Check if source character exists and is non-empty
            final_array[len(val[from_index]) - 1].append((val[from_index], val[to_index]))

    # Filter non-empty arrays, create (length, dict) tuples, and sort by length (descending)
    return [(len(arr[0][0]), dict(arr)) for arr in final_array if arr][::-1]

def replace_by_maps(input_text, hash_maps):
    """
    Replace characters in the input text using the provided mapping tables.

    Args:
        input_text: String to convert.
        hash_maps: List of tuples containing (length, mapping_dict).

    Returns:
        Converted string.
    """
    output_array = []
    b = 0
    while b < len(input_text):
        match = False
        for length, hash_map in hash_maps:
            if b + length <= len(input_text):  # Ensure we don't go beyond string length
                in_chars = input_text[b:b + length]
                if in_chars in hash_map:
                    output_array.append(hash_map[in_chars])  # Can be empty string
                    b += length
                    match = True
                    break
        if not match:
            output_array.append(input_text[b])  # Copy unmatched character
            b += 1  # Always increment to prevent infinite loop
    return ''.join(output_array)

def insert_a(input_text, script):
    """
    Insert 'a' after consonants not followed by virama, dependent vowel, or 'a'
    in Roman or Cyrillic scripts.

    Args:
        input_text: Input string to process.
        script: Target script identifier.

    Returns:
        Processed string with inserted 'a' characters.
    """
    a = 'а' if script == Script.CYRL else 'a'
    text = input_text
    # Replace consonant followed by non-vowel/non-virama with consonant + 'a' + next char
    text = re.sub(f'([{SINH_CONSO_RANGE}])([^\\u0DCF-\\u0DDF\\u0DCA{a}])', f'\\1{a}\\2', text)
    text = re.sub(f'([{SINH_CONSO_RANGE}])([^\\u0DCF-\\u0DDF\\u0DCA{a}])', f'\\1{a}\\2', text)
    # Handle consonant at end of string
    text = re.sub(f'([{SINH_CONSO_RANGE}])$', f'\\1{a}', text)
    return text


def remove_a(input_text, script):
    """
    Remove implicit 'a' from consonants and handle independent vowels.

    Args:
        input_text: Input string to process.
        script: Source script identifier.

    Returns:
        Processed string with implicit 'a' removed.
    """
    text = input_text
    vowel_set = ''.join([
        '\u0D85', '\u0D86', '\u0D89', '\u0D8A', '\u0D8B', '\u0D8C', '\u0D91', '\u0D94', '\u0DCA'
    ])
    # Add virama to consonants not followed by vowels or virama
    # text = re.sub(f'([{SINH_CONSO_RANGE}])([^\\u0D85\\u0D86\\u0D89\\u0D8A\\u0D8B\\u0D8C\\u0D91\\u0D94\\u0DCA])',
    #               '\\1\\u0DCA\\2', text)
    # text = re.sub(f'([{SINH_CONSO_RANGE}])([^\\u0D85\\u0D86\\u0D89\\u0D8A\\u0D8B\\u0D8C\\u0D91\\u0D94\\u0DCA])',
    #               '\\1\\u0DCA\\2', text)

    text = re.sub(rf'([{SINH_CONSO_RANGE}])([^{vowel_set}])', r'\1' + chr(0x0DCA) + r'\2', text)
    text = re.sub(rf'([{SINH_CONSO_RANGE}])([^{vowel_set}])', r'\1' + chr(0x0DCA) + r'\2', text)
    text = re.sub(rf'([{SINH_CONSO_RANGE}])$', r'\1' + chr(0x0DCA), text)


    # Handle consonant at end of string
    # text = re.sub(f'([{SINH_CONSO_RANGE}])$', '\\1\\u0DCA', text)
    # Replace consonant + independent vowel with consonant + dependent vowel
    for iv, dv in IV_TO_DV.items():
        text = text.replace(f'([{SINH_CONSO_RANGE}]){iv}', f'\\1{dv}')
    return text

def fix_m_above(text, script):
    """
    Replace 'ṁ' with Sinhala niggahita (ං) per specific request.

    Args:
        text: Input string to process.

    Returns:
        Processed string.
    """
    return text.replace('ṁ', 'ං')

def roman_to_sinhala(text, script):
    """
    Convert Pali Roman script text to Sinhala, handling vowels contextually.

    Args:
        text: Input string in Roman script.
        script: Source script identifier (Script.RO).

    Returns:
        Converted string in Sinhala.
    """
    if script != Script.RO:
        return text  # Only handle Roman script

    # Define mappings
    consonant_map = {c[2]: c[0] for c in CONSOS if c[2]}  # Roman to Sinhala consonants
    special_map = {s[2]: s[0] for s in SPECIALS if s[2]}  # Roman specials (e.g., 'ṃ' → 'ං')
    vowel_map = {
        'a': '', 'ā': 'ා', 'i': 'ි', 'ī': 'ී', 'u': 'ු', 'ū': 'ූ', 'e': 'ෙ', 'o': 'ො',
        'A': '', 'Ā': 'ා', 'I': 'ි', 'Ī': 'ී', 'U': 'ු', 'Ū': 'ූ', 'E': 'ෙ', 'O': 'ො'
    }  # Roman vowels to Sinhala dependent vowels
    independent_vowel_map = {
        'a': 'අ', 'ā': 'ආ', 'i': 'ඉ', 'ī': 'ඊ', 'u': 'උ', 'ū': 'ඌ', 'e': 'එ', 'o': 'ඔ',
        'A': 'අ', 'Ā': 'ආ', 'I': 'ඉ', 'Ī': 'ඊ', 'U': 'උ', 'Ū': 'ඌ', 'E': 'එ', 'O': 'ඔ'
    }

    output = []
    i = 0
    text = un_capitalize(text)  # Convert to lowercase for consistency

    while i < len(text):
        char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else None

        # Handle special characters (e.g., 'ṃ')
        if char in special_map and char not in vowel_map:
            output.append(special_map[char])
            i += 1
            continue

        # Check for long vowels (e.g., 'ā')
        if char in 'aiueoAIUEO' and next_char == '̄':
            roman_vowel = char + '̄'
            i += 2
        else:
            roman_vowel = char
            i += 1

        # Handle vowels
        if roman_vowel in vowel_map:
            # If previous character is a consonant, use dependent vowel
            if output and output[-1] in SINH_CONSO_RANGE:
                output.append(vowel_map[roman_vowel])
            else:
                # Standalone vowel becomes independent
                output.append(independent_vowel_map[roman_vowel])
            continue

        # Handle consonants
        if char in consonant_map:
            output.append(consonant_map[char])
            # If not followed by a vowel, add virama
            if not next_char or (next_char not in vowel_map and next_char != '̄'):
                output.append('්')
            continue

        # Unmapped character, append as is
        output.append(char)

    return ''.join(output)



def convert_to(text, script):
    """
    Convert text from Sinhala to another script.

    Args:
        text: Input string in Sinhala.
        script: Target script identifier.

    Returns:
        Converted string.
    """
    hash_maps = prepare_hash_maps(SCRIPT_INDEX[Script.SI], SCRIPT_INDEX[script])
    return replace_by_maps(text, hash_maps)

def convert_from(text, script):
    """
    Convert text from another script to Sinhala.

    Args:
        text: Input string in source script.
        script: Source script identifier.

    Returns:
        Converted string in Sinhala.
    """
    hash_maps = prepare_hash_maps(SCRIPT_INDEX.get(script, -1), SCRIPT_INDEX[Script.SI])
    return replace_by_maps(text, hash_maps)


def convert_from_w_v(text, script):
  
    from_index = SCRIPT_INDEX.get(script, -1)
    if from_index == -1:
        return text  # Return unchanged text if script is invalid
    hash_maps = prepare_hash_maps(from_index, SCRIPT_INDEX[Script.SI], use_vowels=False)
    return replace_by_maps(text, hash_maps)

def beautify_sinh(text, script, rend_type=''):
    """
    Beautify Sinhala text by adjusting joiners.

    Args:
        text: Input string to beautify.
        script: Script identifier.
        rend_type: Rendering type (optional).

    Returns:
        Beautified string.
    """
    return re.sub(r'\u0DCA([\u0DBA\u0DBB])', r'\u0DCA\u200D\1', text)

def un_beautify_sinh(text):
    """
    Undo beautification for Sinhala text.

    Args:
        text: Input string to process.

    Returns:
        Processed string.
    """
    text = text.replace('ඒ', 'එ').replace('ඕ', 'ඔ')
    return text.replace('ේ', 'ෙ').replace('ෝ', 'ො')

def beautify_mymr(text, script, rend_type=''):
    """
    Beautify Myanmar text by adjusting punctuation and special characters.

    Args:
        text: Input string to beautify.
        script: Script identifier.
        rend_type: Rendering type (optional).

    Returns:
        Beautified string.
    """
    text = text.replace(r'[,;]', '၊')  # Comma/semicolon to single line
    text = re.sub(r'[\u2026\u0964\u0965]+', '။', text)  # Ellipsis/danda to double line
    text = text.replace('ဉ\u1039ဉ', 'ည')  # kn + kna to single char
    text = text.replace('သ\u1039သ', 'ဿ')  # s + sa to great sa
    text = re.sub(r'င္([က-ဠ])', r'င\u103A\1', text)  # kinzi
    text = text.replace('္ယ', 'ျ')  # yansaya
    text = text.replace('္ရ', 'ြ')  # rakar
    text = text.replace('္ဝ', 'ွ')  # wahswe
    text = text.replace('္ဟ', 'ှ')  # hahto
    text = re.sub(r'([ခဂငဒပဝ]ေ?)\u102c', r'\1\u102b', text)  # aa to tall aa
    text = re.sub(r'(က္ခ|န္ဒ|ပ္ပ|မ္ပ)(ေ?)\u102b', r'\1\2\u102c', text)  # restore tall aa
    return re.sub(r'(ဒ္ဓ|ဒွ)(ေ?)\u102c', r'\1\2\u102b', text)

def un_beautify_mymr(text):
    """
    Undo beautification for Myanmar text.

    Args:
        text: Input string to process.

    Returns:
        Processed string.
    """
    text = text.replace('\u102B', 'ာ')
    text = text.replace('ှ', '္ဟ')  # hahto
    text = text.replace('ွ', '္ဝ')  # wahswe
    text = text.replace('ြ', '္ရ')  # rakar
    text = text.replace('ျ', '္ယ')  # yansaya
    text = text.replace('\u103A', '')  # kinzi
    text = text.replace('ဿ', 'သ\u1039သ')  # great sa
    text = text.replace('ည', 'ဉ\u1039ဉ')  # nnga
    text = text.replace('သံဃ', 'သင္ဃ')  # nigghahita to ṅ
    text = text.replace('၊', ',')  # single line to comma
    return text.replace('။', '.')  # double line to period

def beautify_common(text, script, rend_type=''):
    """
    Apply common beautification steps across scripts.

    Args:
        text: Input string to beautify.
        script: Script identifier.
        rend_type: Rendering type (optional).

    Returns:
        Beautified string.
    """
    if rend_type == 'cen':
        text = text.replace('॥', '')  # Remove double dandas
    elif rend_type.startswith('ga'):
        text = text.replace('।', ';').replace('॥', '.')  # Single to semicolon, double to period
    text = text.replace('॰…', '…')  # Remove abbreviation before ellipsis
    text = text.replace('॰', '·')  # Abbreviation to middle dot
    text = text.replace(r'[।॥]', '.')  # Dandas to period
    text = re.sub(r'\s([\s,!;\?\.])', r'\1', text)  # Cleanup spaces
    return text

def un_capitalize(text):
    """
    Convert text to lowercase for Roman script.

    Args:
        text: Input string to process.

    Returns:
        Lowercase string.
    """
    return text.lower()

def swap_e_o(text, script, rend_type=''):
    """
    Swap 'e' and 'o' vowels with preceding consonants in Thai or Lao scripts.

    Args:
        text: Input string to process.
        script: Script identifier.
        rend_type: Rendering type (optional).

    Returns:
        Processed string.
    """
    if script == Script.THAI:
        return re.sub(f'([{THAI_CONSO_RANGE}])([เโ])', r'\2\1', text)
    if script == Script.LAOS:
        return re.sub(f'([{LAO_CONSO_RANGE}])([ເໂ])', r'\2\1', text)
    raise ValueError(f"Unsupported script {script} for swap_e_o method.")

def un_swap_e_o(text, script):
    """
    Undo swapping of 'e' and 'o' vowels in Thai or Lao scripts.

    Args:
        text: Input string to process.
        script: Source script identifier.

    Returns:
        Processed string.
    """
    if script == Script.THAI:
        return re.sub(f'([เโ])([{THAI_CONSO_RANGE}])', r'\2\1', text)
    if script == Script.LAOS:
        return re.sub(f'([ເໂ])([{LAO_CONSO_RANGE}])', r'\2\1', text)
    raise ValueError(f"Unsupported script {script} for un_swap_e_o method.")

def beautify_thai(text, script, rend_type=''):
    """
    Beautify Thai text by adjusting special glyphs.

    Args:
        text: Input string to beautify.
        script: Script identifier.

    Returns:
        Beautified string.
    """
    text = text.replace('\u0E34\u0E4D', '\u0E36')  # iṃ to single unicode
    text = text.replace('ญ', '\uF70F')
    return text.replace('ฐ', '\uF700')

def un_beautify_thai(text, script):
    """
    Undo beautification for Thai text.

    Args:
        text: Input string to process.
        script: Script identifier.

    Returns:
        Processed string.
    """
    text = text.replace('ฎ', 'ฏ')  # Correct common mistake
    text = text.replace('\u0E36', '\u0E34\u0E4D')  # Split iṃ
    text = text.replace('\uF70F', 'ญ')
    return text.replace('\uF700', 'ฐ')

def un_beautify_khmer(text, script):
    """
    Undo beautification for Khmer text.

    Args:
        text: Input string to process.
        script: Script identifier.

    Returns:
        Processed string.
    """
    text = text.replace('\u17B9', '\u17B7\u17C6')  # Split iṃ
    return text.replace('\u17D1', '\u17D2')  # End of word virama

def cleanup_zwj(text):
    """
    Remove zero-width joiners from text.

    Args:
        text: Input string to process.

    Returns:
        Processed string.
    """
    return re.sub(r'[\u200C\u200D]', '', text)

def beautify_brahmi(text):
    """
    Beautify Brahmi text by replacing dandas and dashes.

    Args:
        text: Input string to beautify.

    Returns:
        Beautified string.
    """
    text = text.replace('।', '𑁇')
    text = text.replace('॥', '𑁈')
    return text.replace('–', '𑁋')

def beautify_tham(text):
    """
    Beautify Tai Tham text by adjusting special characters.

    Args:
        text: Input string to beautify.

    Returns:
        Beautified string.
    """
    text = text.replace('\u1A60\u1A41', '\u1A55')  # Medial ra
    text = text.replace('\u1A48\u1A60\u1A48', '\u1A54')  # Great sa
    text = text.replace('।', '\u1AA8')
    return text.replace('॥', '\u1AA9')

def beautify_tibet(text):
    """
    Beautify Tibetan text by adjusting dandas and subjoined consonants.

    Args:
        text: Input string to beautify.

    Returns:
        Beautified string.
    """
    text = text.replace('।', '།')  # Tibetan dandas
    text = text.replace('॥', '༎')
    for i in range(40):
        text = re.sub(chr(0x0F84) + chr(0x0F40 + i), chr(0x0F90 + i), text)
    text = text.replace('\u0F61\u0FB1', '\u0F61\u0FBB')  # yya
    text = text.replace('\u0F5D\u0FAD', '\u0F5D\u0FBA')  # vva
    text = text.replace('\u0F5B\u0FAC', '\u0F5B\u0F84\u0F5C')  # jjha
    text = text.replace('\u0F61\u0FB7', '\u0F61\u0F84\u0F67')  # yha
    return text.replace('\u0F5D\u0FB7', '\u0F5D\u0F84\u0F67')  # vha

def un_beautify_tibet(text):
    """
    Undo beautification for Tibetan text (placeholder).

    Args:
        text: Input string to process.

    Returns:
        Processed string.
    """
    return text  # TODO: Implement if needed

# Function mappings
CONVERT_TO_FUNC_DEFAULT = [convert_to]
CONVERT_TO_FUNC = {
    Script.SI: [],
    Script.RO: [insert_a, convert_to],
    Script.CYRL: [insert_a, convert_to],
}

CONVERT_FROM_FUNC_DEFAULT = [convert_from]
# CONVERT_FROM_FUNC = {
#     Script.SI: [],
#     Script.RO: [convert_from_w_v, fix_m_above, remove_a],
#     Script.CYRL: [convert_from_w_v, remove_a],
# }

# Update CONVERT_FROM_FUNC for Roman script
CONVERT_FROM_FUNC = {
    Script.SI: [],
    Script.RO: [roman_to_sinhala, fix_m_above],  # Replace old pipeline
    Script.CYRL: [convert_from_w_v, remove_a],
}

BEAUTIFY_FUNC_DEFAULT = []
BEAUTIFY_FUNC = {
    Script.SI: [beautify_sinh, beautify_common],
    Script.RO: [beautify_common],
    Script.THAI: [swap_e_o, beautify_thai, beautify_common],
    Script.LAOS: [swap_e_o, beautify_common],
    Script.MY: [beautify_mymr, beautify_common],
    Script.KM: [beautify_common],
    Script.THAM: [beautify_tham],
    Script.GUJA: [beautify_common],
    Script.TELU: [beautify_common],
    Script.MALA: [beautify_common],
    Script.BRAH: [beautify_brahmi, beautify_common],
    Script.TIBT: [beautify_tibet],
    Script.CYRL: [beautify_common],
}

UN_BEAUTIFY_FUNC_DEFAULT = []
UN_BEAUTIFY_FUNC = {
    Script.SI: [cleanup_zwj, un_beautify_sinh],
    Script.HI: [cleanup_zwj],
    Script.RO: [un_capitalize],
    Script.THAI: [un_beautify_thai, un_swap_e_o],
    Script.LAOS: [un_swap_e_o],
    Script.KM: [un_beautify_khmer],
    Script.MY: [un_beautify_mymr],
    Script.TIBT: [un_beautify_tibet],
}

class TextProcessor:
    """
    A class to handle Pali text conversion and beautification between scripts.
    """
    @staticmethod
    def basic_convert_from_sinh(input_text, script):
        """
        Convert text from Sinhala to another script.

        Args:
            input_text: Input string in Sinhala.
            script: Target script identifier.

        Returns:
            Converted string.
        """
        text = input_text
        for func in CONVERT_TO_FUNC.get(script, CONVERT_TO_FUNC_DEFAULT):
            text = func(text, script)
        return text

    @staticmethod
    def basic_convert_to_sinh(input_text, script):
        """
        Convert text from another script to Sinhala.

        Args:
            input_text: Input string in source script.
            script: Source script identifier.

        Returns:
            Converted string in Sinhala.
        """
        text = input_text
        for func in CONVERT_FROM_FUNC.get(script, CONVERT_FROM_FUNC_DEFAULT):
            text = func(text, script)
        return text

    @staticmethod
    def beautify(input_text, script, rend_type=''):
        """
        Apply script-specific beautification.

        Args:
            input_text: Input string to beautify.
            script: Script identifier.
            rend_type: Rendering type (optional).

        Returns:
            Beautified string.
        """
        text = input_text
        for func in BEAUTIFY_FUNC.get(script, BEAUTIFY_FUNC_DEFAULT):
            text = func(text, script, rend_type)
        return text

    @staticmethod
    def convert_from_sinh(input_text, script):
        """
        Convert and beautify text from Sinhala to another script.

        Args:
            input_text: Input string in Sinhala.
            script: Target script identifier.

        Returns:
            Converted and beautified string.
        """
        text = TextProcessor.basic_convert_from_sinh(input_text, script)
        return TextProcessor.beautify(text, script)

    @staticmethod
    def convert_to_sinh(input_text, script):
        """
        Convert and unbeautify text from another script to Sinhala.

        Args:
            input_text: Input string in source script.
            script: Source script identifier.

        Returns:
            Converted string in Sinhala.
        """
        text = input_text
        for func in UN_BEAUTIFY_FUNC.get(script, UN_BEAUTIFY_FUNC_DEFAULT):
            text = func(text)
        return TextProcessor.basic_convert_to_sinh(text, script)

    @staticmethod
    def convert_any_to_sinh(input_text):
        """
        Convert mixed-script text to Sinhala.

        Args:
            input_text: Input string with mixed scripts.

        Returns:
            Converted string in Sinhala.
        """
        mixed_text = cleanup_zwj(input_text) + ' '  # Handle ZWJ and add space for last char
        cur_script = -1
        run = ''
        output = ''
        for char in mixed_text:
            new_script = get_script_for_code(ord(char))
            if new_script != cur_script or char == mixed_text[-1]:
                output += TextProcessor.convert_to_sinh(run, cur_script)
                cur_script = new_script
                run = char
            else:
                run += char
        return output
        

def myanmar_to_roman(myanmar):
    sinh = TextProcessor.convert_to_sinh(myanmar, Script.MY)
    roman = TextProcessor.convert_from_sinh(sinh, Script.RO)
    return roman


def roman_to_sinhala1(text):
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

def roman_to_sinhala(text):
    from aksharamukha import transliterate
    sinhala_text = transliterate.process('IAST', 'Sinhala', text, post_options=['SinhalaPali'])
    return sinhala_text



if __name__ == '__main__':
    sin = "දජ්ජෙය්‍යුං"
    ori_roman = 'dajjeyyuṃ'
    # sinh = TextProcessor.convert_to_sinh(ori_roman, Script.RO)
    sinh = roman_to_sinhala(ori_roman)
    print(sinh)
    # roman = TextProcessor.convert_from_sinh(sin, Script.RO)

    if sinh in sin:
        print("OKKKK")
    else:
        print(sin)
