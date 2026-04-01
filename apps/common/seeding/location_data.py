# country_data.py

# This data is used for seeding the Country model in Django.
# It includes country names, ISO 3166-3 alpha-3 codes (where available, otherwise Alpha-2),
# dial codes, currency codes, and currency names.
# Missing data has been filled in using publicly available information.

COUNTRIES_DATA = [
    {
        'name': 'Malawi',
        'code': 'MWI',
        'slug': 'malawi',
        'dial_code': '265',
        'currency_code': 'MWK',
        'currency_name': 'Malawi Kwacha',
        'is_active': True,
    },
    {
        'name': 'Mozambique',
        'code': 'MOZ',
        'slug': 'mozambique',
        'dial_code': '258',
        'currency_code': 'MZN',
        'currency_name': 'Mozambique Metical',
        'is_active': True,
    },
    {
        'name': 'Namibia',
        'code': 'NAM',
        'slug': 'namibia',
        'dial_code': '264',
        'currency_code': 'NAD',
        'currency_name': 'Namibian Dollar',
        'is_active': True,
    },
    {
        'name': 'Nigeria',
        'code': 'NGA',
        'slug': 'nigeria',
        'dial_code': '234',
        'currency_code': 'NGN',
        'currency_name': 'Naira',
        'is_active': True,
    },
    {
        'name': 'South Africa',
        'code': 'ZAF',
        'slug': 'south-africa',
        'dial_code': '27',
        'currency_code': 'ZAR',
        'currency_name': 'Rand',
        'is_active': True,
    },
    {
        'name': 'Zambia',
        'code': 'ZM',
        'slug': 'zambia',
        'dial_code': '260',
        'currency_code': 'ZMW',
        'currency_name': 'Zambian Kwacha',
        'is_active': True,
    },
    {
        'name': 'Zimbabwe',
        'code': 'ZW',
        'slug': 'zimbabwe',
        'dial_code': '263',
        'currency_code': 'ZWG',
        'currency_name': 'Zimbabwe Gold',
        'is_active': True,
    },
]

PROVINCES_DATA = [
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Harare",
        "province_slug": "harare",
        "province_code": "HRE", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Bulawayo",
        "province_slug": "bulawayo",
        "province_code": "BUL", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Manicaland",
        "province_slug": "manicaland",
        "province_code": "MAN", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Masvingo",
        "province_slug": "masvingo",
        "province_code": "MAS", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Mashonaland East",
        "province_slug": "mashonaland-east",
        "province_code": "MAE", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Mashonaland Central",
        "province_slug": "mashonaland-central",
        "province_code": "MAC", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Mashonaland West",
        "province_slug": "mashonaland-west",
        "province_code": "MAW", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Midlands",
        "province_slug": "midlands",
        "province_code": "MID", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Matebeleland North",
        "province_slug": "matebeleland-north",
        "province_code": "MNA", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_name": "Matebeleland South",
        "province_slug": "matebeleland-south",
        "province_code": "MSA", # Added province code
        "approved": 1
    },
    {
        "country_code": "ZAF", # South Africa
        "province_name": "Gauteng",
        "province_slug": "gauteng",
        "province_code": "GT", # Added province code
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_name": "Western Cape",
        "province_slug": "western-cape",
        "province_code": "WC", # Added province code
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_name": "Kwazulu Natal",
        "province_slug": "kwazulu-natal",
        "province_code": "KZN", # Added province code
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_name": "Blantyre",
        "province_slug": "blantyre",
        "province_code": "BLA", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_name": "Cabo Delgado",
        "province_slug": "cabo-delgado",
        "province_code": "CDG", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_name": "Maputo",
        "province_slug": "maputo",
        "province_code": "MAP", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_name": "Gaza",
        "province_slug": "gaza",
        "province_code": "GAZ", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_name": "Inhambane",
        "province_slug": "inhambane",
        "province_code": "INH", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_name": "Manica",
        "province_slug": "manica",
        "province_code": "MNC", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ",
        "province_name": "Nampula",
        "province_slug": "nampula",
        "province_code": "NAP", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ",
        "province_name": "Niassa",
        "province_slug": "niassa",
        "province_code": "NIA", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ",
        "province_name": "Sofala",
        "province_slug": "sofala",
        "province_code": "SOF", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ",
        "province_name": "Tete",
        "province_slug": "tete",
        "province_code": "TET", # Added province code
        "approved": 0
    },
    {
        "country_code": "MOZ",
        "province_name": "Zambezia",
        "province_slug": "zambezia",
        "province_code": "ZAM", # Added province code
        "approved": 0
    }
]

CITIES_DATA = [
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_name": "Chitungwiza",
        "city_slug": "chitungwiza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_name": "Ruwa",
        "city_slug": "ruwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_name": "Harare",
        "city_slug": "harare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_name": "Bulawayo",
        "city_slug": "bulawayo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Buhera",
        "city_slug": "buhera",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Chimanimani",
        "city_slug": "chimanimani",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Chipinge",
        "city_slug": "chipinge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Headlands",
        "city_slug": "headlands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Juliasdale",
        "city_slug": "juliasdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Makoni",
        "city_slug": "makoni",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Musikavanhu",
        "city_slug": "musikavanhu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Mutare",
        "city_slug": "mutare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Nyanga",
        "city_slug": "nyanga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Rusape",
        "city_slug": "rusape",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Vumba",
        "city_slug": "vumba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_name": "Penhalonga",
        "city_slug": "penhalonga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Bikita",
        "city_slug": "bikita",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Chiredzi",
        "city_slug": "chiredzi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Gutu",
        "city_slug": "gutu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Masvingo",
        "city_slug": "masvingo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Mwenezi",
        "city_slug": "mwenezi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Rutenga",
        "city_slug": "rutenga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Triangle",
        "city_slug": "triangle",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_name": "Zaka",
        "city_slug": "zaka",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Arcturus",
        "city_slug": "arcturus",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Beatrice",
        "city_slug": "beatrice",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Chikomba",
        "city_slug": "chikomba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Chivhu",
        "city_slug": "chivhu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Damofalls",
        "city_slug": "damofalls",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Goromonzi",
        "city_slug": "goromonzi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Marondera",
        "city_slug": "marondera",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Mudzi",
        "city_slug": "mudzi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Murehwa",
        "city_slug": "murehwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Mutoko",
        "city_slug": "mutoko",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Seke",
        "city_slug": "seke",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Wedza",
        "city_slug": "wedza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Domboshawa",
        "city_slug": "domboshawa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Dema",
        "city_slug": "dema",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_name": "Macheke",
        "city_slug": "macheke",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Bindura",
        "city_slug": "bindura",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Centenary",
        "city_slug": "centenary",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Christon",
        "city_slug": "christon",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Concession",
        "city_slug": "concession",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Guruve",
        "city_slug": "guruve",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Mazowe",
        "city_slug": "mazowe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Mt Darwin",
        "city_slug": "mt-darwin",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Mvurwi",
        "city_slug": "mvurwi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Rushinga",
        "city_slug": "rushinga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Shamva",
        "city_slug": "shamva",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_name": "Mbire",
        "city_slug": "mbire",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Banket",
        "city_slug": "banket",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Chegutu",
        "city_slug": "chegutu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Chinhoyi",
        "city_slug": "chinhoyi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Chirundu",
        "city_slug": "chirundu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Darwendale",
        "city_slug": "darwendale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Hurungwe",
        "city_slug": "hurungwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Kadoma",
        "city_slug": "kadoma",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Kariba",
        "city_slug": "kariba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Karoi",
        "city_slug": "karoi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Lake",
        "city_slug": "lake",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Lower",
        "city_slug": "lower",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Makonde",
        "city_slug": "makonde",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Mazvikadei",
        "city_slug": "mazvikadei",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Norton",
        "city_slug": "norton",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Zambezi",
        "city_slug": "zambezi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Zvimba",
        "city_slug": "zvimba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Selous",
        "city_slug": "selous",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Raffingora",
        "city_slug": "raffingora",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Mhangura",
        "city_slug": "mhangura",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Chirumhanzu",
        "city_slug": "chirumhanzu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Gokwe",
        "city_slug": "gokwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Gweru",
        "city_slug": "gweru",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Kwekwe",
        "city_slug": "kwekwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Mberengwa",
        "city_slug": "mberengwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Redcliff",
        "city_slug": "redcliff",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Shurugwi",
        "city_slug": "shurugwi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Zvishavane",
        "city_slug": "zvishavane",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_name": "Mvuma",
        "city_slug": "mvuma",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Binga",
        "city_slug": "binga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Bubi",
        "city_slug": "bubi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Deka",
        "city_slug": "deka",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Hwange",
        "city_slug": "hwange",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Lupane",
        "city_slug": "lupane",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Msuna",
        "city_slug": "msuna",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Nkayi",
        "city_slug": "nkayi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Tsholotsho",
        "city_slug": "tsholotsho",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Umguza",
        "city_slug": "umguza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_name": "Victoria Falls",
        "city_slug": "victoria-falls",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Beitbridge",
        "city_slug": "beitbridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Bulilimamangwe",
        "city_slug": "bulilimamangwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Figtree",
        "city_slug": "figtree",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Gwanda",
        "city_slug": "gwanda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Insiza",
        "city_slug": "insiza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Matobo",
        "city_slug": "matobo",
        "approved": 0
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Plumtree",
        "city_slug": "plumtree",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Shangani",
        "city_slug": "shangani",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_name": "Umzingwane",
        "city_slug": "umzingwane",
        "approved": 1
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "gauteng",
        "city_name": "Johannesburg",
        "city_slug": "johannesburg",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "gauteng",
        "city_name": "Pretoria",
        "city_slug": "pretoria",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "western-cape",
        "city_name": "Cape Town",
        "city_slug": "cape-town",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Hillcrest",
        "city_slug": "hillcrest",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Kloof",
        "city_slug": "kloof",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Waterfall",
        "city_slug": "waterfall",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Gillitts",
        "city_slug": "gillitts",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Assagay",
        "city_slug": "assagay",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Bothas Hill",
        "city_slug": "bothas-hill",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Crestholme",
        "city_slug": "crestholme",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_name": "Summerveld",
        "city_slug": "summerveld",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Mangochi",
        "city_slug": "mangochi",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Mangochi Town Center",
        "city_slug": "mangochi-town-center",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Mangochi Township",
        "city_slug": "mangochi-township",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Mponda",
        "city_slug": "mponda",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Maldeco",
        "city_slug": "maldeco",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Mbwadzulu",
        "city_slug": "mbwadzulu",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Chiponde",
        "city_slug": "chiponde",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Nankumba",
        "city_slug": "nankumba",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Chilipa",
        "city_slug": "chilipa",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_name": "Mangochi Boma",
        "city_slug": "mangochi-boma",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Pemba",
        "city_slug": "pemba",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Montepuez",
        "city_slug": "montepuez",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mocímboa da Praia",
        "city_slug": "mocimboa-da-praia",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Palma",
        "city_slug": "palma",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Macomia",
        "city_slug": "macomia",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Quissanga",
        "city_slug": "quissanga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Metuge",
        "city_slug": "metuge",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Chiúre",
        "city_slug": "chiure",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Ancuabe",
        "city_slug": "ancuabe",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Ibo",
        "city_slug": "ibo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mueda",
        "city_slug": "mueda",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Meluco",
        "city_slug": "meluco",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Centro",
        "city_slug": "centro",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Paquitequete",
        "city_slug": "paquitequete",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Murrebue",
        "city_slug": "murrebue",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Chali",
        "city_slug": "chali",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Cimento",
        "city_slug": "cimento",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Ponta Vermelha",
        "city_slug": "ponta-vermelha",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Bairro Novo",
        "city_slug": "bairro-novo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Nanhime",
        "city_slug": "nanhime",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Murrupula",
        "city_slug": "murrupula",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Muapula",
        "city_slug": "muapula",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mutiva",
        "city_slug": "mutiva",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Muiuane",
        "city_slug": "muiuane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mussoromosso",
        "city_slug": "mussoromosso",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Alto da Manga",
        "city_slug": "alto-da-manga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mia Couto",
        "city_slug": "mia-couto",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Baixa",
        "city_slug": "baixa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mucojo",
        "city_slug": "mucojo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Manilha",
        "city_slug": "manilha",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Areias",
        "city_slug": "areias",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Quibuidine",
        "city_slug": "quibuidine",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Zona Verde",
        "city_slug": "zona-verde",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Nova Vida",
        "city_slug": "nova-vida",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Quelimane",
        "city_slug": "quelimane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Muxúnguè",
        "city_slug": "muxungue",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Pangane",
        "city_slug": "pangane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Matemo",
        "city_slug": "matemo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Quionga",
        "city_slug": "quionga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mecufi",
        "city_slug": "mecufi",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Nacotuco",
        "city_slug": "nacotuco",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Mecula",
        "city_slug": "mecula",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Meza",
        "city_slug": "meza",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Nairoto",
        "city_slug": "nairoto",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "M'punga",
        "city_slug": "mpunga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Cobaia",
        "city_slug": "cobaia",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Napupa",
        "city_slug": "napupa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Napapa",
        "city_slug": "napapa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Nacujo",
        "city_slug": "nacujo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Napome",
        "city_slug": "napome",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Nagaze",
        "city_slug": "nagaze",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Porto",
        "city_slug": "porto",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Fortaleza",
        "city_slug": "fortaleza",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Cabo",
        "city_slug": "cabo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Makuti",
        "city_slug": "makuti",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Administrative Center",
        "city_slug": "administrative-center",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Local Villages",
        "city_slug": "local-villages",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Rural Communities",
        "city_slug": "rural-communities",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Agricultural Areas",
        "city_slug": "agricultural-areas",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Market Centers",
        "city_slug": "market-centers",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_name": "Traditional Communal Areas",
        "city_slug": "traditional-communal-areas",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_name": "Maputo",
        "city_slug": "maputo",
        "approved": 0
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_name": "Harare",
        "city_slug": "harare",
        "approved": 0
    }
]

SUBURBS_DATA = [
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "chitungwiza",
        "suburb_name": "Chitungwiza",
        "suburb_slug": "chitungwiza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "ruwa",
        "suburb_name": "Ruwa",
        "suburb_slug": "ruwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Harare City Center",
        "suburb_slug": "harare-city-center",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Amby",
        "suburb_slug": "amby",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Athlone",
        "suburb_slug": "athlone",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Eastlea",
        "suburb_slug": "eastlea",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Greendale",
        "suburb_slug": "greendale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Greengrove",
        "suburb_slug": "greengrove",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mandara",
        "suburb_slug": "mandara",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Manresa",
        "suburb_slug": "manresa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Msasa",
        "suburb_slug": "msasa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rhodesville",
        "suburb_slug": "rhodesville",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rockview",
        "suburb_slug": "rockview",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Sunway City",
        "suburb_slug": "sunway-city",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Zimre Park",
        "suburb_slug": "zimre-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Upper Hillside",
        "suburb_slug": "upper-hillside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Kamfinsa",
        "suburb_slug": "kamfinsa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Eastview",
        "suburb_slug": "eastview",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Budiriro",
        "suburb_slug": "budiriro",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Glen Norah",
        "suburb_slug": "glen-norah",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Glen View",
        "suburb_slug": "glen-view",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Dzivarasekwa",
        "suburb_slug": "dzivarasekwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Epworth",
        "suburb_slug": "epworth",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Highfield",
        "suburb_slug": "highfield",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Hatcliffe",
        "suburb_slug": "hatcliffe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Kambuzuma",
        "suburb_slug": "kambuzuma",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Kuwadzana",
        "suburb_slug": "kuwadzana",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mabvuku",
        "suburb_slug": "mabvuku",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mbare",
        "suburb_slug": "mbare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Marimba Park",
        "suburb_slug": "marimba-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mufakose",
        "suburb_slug": "mufakose",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rydale Ridge",
        "suburb_slug": "rydale-ridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Sunningdale",
        "suburb_slug": "sunningdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Snake Park",
        "suburb_slug": "snake-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Tafara",
        "suburb_slug": "tafara",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Warren Park",
        "suburb_slug": "warren-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Crowborough",
        "suburb_slug": "crowborough",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Adelaide Park",
        "suburb_slug": "adelaide-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rugare",
        "suburb_slug": "rugare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Granary Park",
        "suburb_slug": "granary-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Highlands",
        "suburb_slug": "highlands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Chisipite",
        "suburb_slug": "chisipite",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Avondale",
        "suburb_slug": "avondale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Alexandra Park",
        "suburb_slug": "alexandra-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ballantyne Park",
        "suburb_slug": "ballantyne-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Belgravia",
        "suburb_slug": "belgravia",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Borrowdale West",
        "suburb_slug": "borrowdale-west",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Borrowdale Brooke",
        "suburb_slug": "borrowdale-brooke",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Charlotte Brooke",
        "suburb_slug": "charlotte-brooke",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Colray",
        "suburb_slug": "colray",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Colne Valley",
        "suburb_slug": "colne-valley",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Dandaro",
        "suburb_slug": "dandaro",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Crowhill Views",
        "suburb_slug": "crowhill-views",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Groom Bridge",
        "suburb_slug": "groom-bridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Gunhill",
        "suburb_slug": "gunhill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Glen Lorne",
        "suburb_slug": "glen-lorne",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Glen Forest",
        "suburb_slug": "glen-forest",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Gletwin Park",
        "suburb_slug": "gletwin-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Greystone Park",
        "suburb_slug": "greystone-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Helensvale",
        "suburb_slug": "helensvale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Hogerty Hill",
        "suburb_slug": "hogerty-hill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Kambanji",
        "suburb_slug": "kambanji",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Lewisam",
        "suburb_slug": "lewisam",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mount Pleasant",
        "suburb_slug": "mount-pleasant",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Newlands",
        "suburb_slug": "newlands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Northwood",
        "suburb_slug": "northwood",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Philadelphia",
        "suburb_slug": "philadelphia",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Pomona",
        "suburb_slug": "pomona",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Quinnington",
        "suburb_slug": "quinnington",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rolf Valley",
        "suburb_slug": "rolf-valley",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ryelands",
        "suburb_slug": "ryelands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Shawasha Hills",
        "suburb_slug": "shawasha-hills",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Sally Mugabe Heights",
        "suburb_slug": "sally-mugabe-heights",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "The Grange",
        "suburb_slug": "the-grange",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Umwinsidale",
        "suburb_slug": "umwinsidale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Vainona",
        "suburb_slug": "vainona",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Greendale North",
        "suburb_slug": "greendale-north",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mt Pleasant Heights",
        "suburb_slug": "mt-pleasant-heights",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Teviotdale",
        "suburb_slug": "teviotdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Carrick Creagh Estate",
        "suburb_slug": "carrick-creagh-estate",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Glenwood",
        "suburb_slug": "glenwood",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Borrowdale",
        "suburb_slug": "borrowdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Airport",
        "suburb_slug": "airport",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Arcadia",
        "suburb_slug": "arcadia",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ardbennie",
        "suburb_slug": "ardbennie",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Braeside",
        "suburb_slug": "braeside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Chadcombe",
        "suburb_slug": "chadcombe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Cranborne",
        "suburb_slug": "cranborne",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Graniteside",
        "suburb_slug": "graniteside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Hatfield",
        "suburb_slug": "hatfield",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Hillside",
        "suburb_slug": "hillside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Houghton Park",
        "suburb_slug": "houghton-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Logan Park",
        "suburb_slug": "logan-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Msasa Park",
        "suburb_slug": "msasa-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mainway Meadows",
        "suburb_slug": "mainway-meadows",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Parktown",
        "suburb_slug": "parktown",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Park Meadowlands",
        "suburb_slug": "park-meadowlands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Prospect",
        "suburb_slug": "prospect",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Queensdale",
        "suburb_slug": "queensdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Southerton",
        "suburb_slug": "southerton",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "St. Martins",
        "suburb_slug": "st-martins",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Waterfalls",
        "suburb_slug": "waterfalls",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Willowvale",
        "suburb_slug": "willowvale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Workington",
        "suburb_slug": "workington",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Southlea Park",
        "suburb_slug": "southlea-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Arlington",
        "suburb_slug": "arlington",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Exelsior",
        "suburb_slug": "exelsior",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Southview Park",
        "suburb_slug": "southview-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Stoneridge",
        "suburb_slug": "stoneridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Lochinvar",
        "suburb_slug": "lochinvar",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Retreat",
        "suburb_slug": "retreat",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ushewokunze",
        "suburb_slug": "ushewokunze",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Graylands Park",
        "suburb_slug": "graylands-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Adylinn",
        "suburb_slug": "adylinn",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ashbrittle",
        "suburb_slug": "ashbrittle",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ashdown Park",
        "suburb_slug": "ashdown-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Avondale - The Ridge",
        "suburb_slug": "avondale-the-ridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Avondale West",
        "suburb_slug": "avondale-west",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Avonlea",
        "suburb_slug": "avonlea",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Belvedere",
        "suburb_slug": "belvedere",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Bluff Hill",
        "suburb_slug": "bluff-hill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Cold Comfort",
        "suburb_slug": "cold-comfort",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Cotswold Hills",
        "suburb_slug": "cotswold-hills",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Dawnview Park",
        "suburb_slug": "dawnview-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Emerald Hill",
        "suburb_slug": "emerald-hill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Greencroft",
        "suburb_slug": "greencroft",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Haig Park",
        "suburb_slug": "haig-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Kensington",
        "suburb_slug": "kensington",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Marlborough",
        "suburb_slug": "marlborough",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mabelreign",
        "suburb_slug": "mabelreign",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Matidoda",
        "suburb_slug": "matidoda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Meyrick Park",
        "suburb_slug": "meyrick-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Milton Park",
        "suburb_slug": "milton-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Monavale",
        "suburb_slug": "monavale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Nkwisi Gardens",
        "suburb_slug": "nkwisi-gardens",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mt Hampden",
        "suburb_slug": "mt-hampden",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Ridgeview",
        "suburb_slug": "ridgeview",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rydale Ridge Park",
        "suburb_slug": "rydale-ridge-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Sentosa",
        "suburb_slug": "sentosa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Spitzkop",
        "suburb_slug": "spitzkop",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Strathaven",
        "suburb_slug": "strathaven",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Sunridge",
        "suburb_slug": "sunridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Tynwald",
        "suburb_slug": "tynwald",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Warren Hills",
        "suburb_slug": "warren-hills",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Westgate",
        "suburb_slug": "westgate",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Westlea Hre",
        "suburb_slug": "westlea-hre",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Whitecliff",
        "suburb_slug": "whitecliff",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Glaudina",
        "suburb_slug": "glaudina",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rainham",
        "suburb_slug": "rainham",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Bloomingdale",
        "suburb_slug": "bloomingdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Madokero Estates",
        "suburb_slug": "madokero-estates",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Sandton Park",
        "suburb_slug": "sandton-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Aspindale Park",
        "suburb_slug": "aspindale-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Fairview",
        "suburb_slug": "fairview",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Goodhope",
        "suburb_slug": "goodhope",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Falcon Park",
        "suburb_slug": "falcon-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Bulawayo City Centre",
        "suburb_slug": "bulawayo-city-centre",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Westondale",
        "suburb_slug": "westondale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Steeldale",
        "suburb_slug": "steeldale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Westgate Byo",
        "suburb_slug": "westgate-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Belmont",
        "suburb_slug": "belmont",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Donnington",
        "suburb_slug": "donnington",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Donnington West",
        "suburb_slug": "donnington-west",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Thorngrove",
        "suburb_slug": "thorngrove",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Kelvin",
        "suburb_slug": "kelvin",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Kelvin West",
        "suburb_slug": "kelvin-west",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Spezini",
        "suburb_slug": "spezini",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Fortunes Gate",
        "suburb_slug": "fortunes-gate",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Riverside South",
        "suburb_slug": "riverside-south",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Willsgrove",
        "suburb_slug": "willsgrove",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Manningdale",
        "suburb_slug": "manningdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Waterford",
        "suburb_slug": "waterford",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Douglasdale",
        "suburb_slug": "douglasdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Riverside North",
        "suburb_slug": "riverside-north",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Sunning Hill",
        "suburb_slug": "sunning-hill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Matsheumhlope",
        "suburb_slug": "matsheumhlope",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Selbourne Park",
        "suburb_slug": "selbourne-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Woodlands",
        "suburb_slug": "woodlands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Kumalo",
        "suburb_slug": "kumalo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Parklands",
        "suburb_slug": "parklands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Killarney",
        "suburb_slug": "killarney",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Hume Park",
        "suburb_slug": "hume-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Burnside",
        "suburb_slug": "burnside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Ilanda",
        "suburb_slug": "ilanda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Gumtree",
        "suburb_slug": "gumtree",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Kensington Byo",
        "suburb_slug": "kensington-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Lakeside",
        "suburb_slug": "lakeside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Ascot",
        "suburb_slug": "ascot",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Worringham",
        "suburb_slug": "worringham",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Suburbs",
        "suburb_slug": "suburbs",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Lochview",
        "suburb_slug": "lochview",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Home Fountain",
        "suburb_slug": "home-fountain",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Barbour Fields",
        "suburb_slug": "barbour-fields",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Mzilikazi",
        "suburb_slug": "mzilikazi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Makokoba",
        "suburb_slug": "makokoba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Matshombana",
        "suburb_slug": "matshombana",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Nguboyenja",
        "suburb_slug": "nguboyenja",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "West Somerton",
        "suburb_slug": "west-somerton",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Emganwini",
        "suburb_slug": "emganwini",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Umganin",
        "suburb_slug": "umganin",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Bubi Umguza",
        "suburb_slug": "bubi-umguza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Upper Rangemore",
        "suburb_slug": "upper-rangemore",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Nkulumane",
        "suburb_slug": "nkulumane",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Nketa",
        "suburb_slug": "nketa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Tshabalala",
        "suburb_slug": "tshabalala",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Tshabalala Extension",
        "suburb_slug": "tshabalala-extension",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Sizinda",
        "suburb_slug": "sizinda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Cowdray Park",
        "suburb_slug": "cowdray-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Enqotsheni",
        "suburb_slug": "enqotsheni",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "New Luveve",
        "suburb_slug": "new-luveve",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Luveve North",
        "suburb_slug": "luveve-north",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Luveve",
        "suburb_slug": "luveve",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Emakhandeni",
        "suburb_slug": "emakhandeni",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Pelandaba",
        "suburb_slug": "pelandaba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Lobengula",
        "suburb_slug": "lobengula",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Magwegwe",
        "suburb_slug": "magwegwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Mpopoma",
        "suburb_slug": "mpopoma",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Mpopoma South",
        "suburb_slug": "mpopoma-south",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Pumula",
        "suburb_slug": "pumula",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Pumula South",
        "suburb_slug": "pumula-south",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Paddonhurst",
        "suburb_slug": "paddonhurst",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Sunnyside",
        "suburb_slug": "sunnyside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Tegela",
        "suburb_slug": "tegela",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Romney Park",
        "suburb_slug": "romney-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Queens Park East",
        "suburb_slug": "queens-park-east",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Queens Park West",
        "suburb_slug": "queens-park-west",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Northgate",
        "suburb_slug": "northgate",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Orange Grove",
        "suburb_slug": "orange-grove",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Woodville Park",
        "suburb_slug": "woodville-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Jacaranda",
        "suburb_slug": "jacaranda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Northlea Byo",
        "suburb_slug": "northlea-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Woodville",
        "suburb_slug": "woodville",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Kingsdale",
        "suburb_slug": "kingsdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Queensdale Byo",
        "suburb_slug": "queensdale-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Lobenvale",
        "suburb_slug": "lobenvale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "The Jungle",
        "suburb_slug": "the-jungle",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Umguza Byo",
        "suburb_slug": "umguza-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "North Trenance",
        "suburb_slug": "north-trenance",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Richmond",
        "suburb_slug": "richmond",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Upper Glenville",
        "suburb_slug": "upper-glenville",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Glenville",
        "suburb_slug": "glenville",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Windsor Park Byo",
        "suburb_slug": "windsor-park-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Trenance",
        "suburb_slug": "trenance",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Entumbane",
        "suburb_slug": "entumbane",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Glengarry",
        "suburb_slug": "glengarry",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Northend",
        "suburb_slug": "northend",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Mahatshula",
        "suburb_slug": "mahatshula",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Rangemore",
        "suburb_slug": "rangemore",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Sauerstown",
        "suburb_slug": "sauerstown",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Highmount",
        "suburb_slug": "highmount",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Arundel",
        "suburb_slug": "arundel",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "North End",
        "suburb_slug": "north-end",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Hopeville",
        "suburb_slug": "hopeville",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Hillside Byo",
        "suburb_slug": "hillside-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Greenhill",
        "suburb_slug": "greenhill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Southwold",
        "suburb_slug": "southwold",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Barham Green",
        "suburb_slug": "barham-green",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Morningside Byo",
        "suburb_slug": "morningside-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Hillcrest",
        "suburb_slug": "hillcrest",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Montrose Byo",
        "suburb_slug": "montrose-byo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Bellevue",
        "suburb_slug": "bellevue",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Newton",
        "suburb_slug": "newton",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Newton West",
        "suburb_slug": "newton-west",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Four Winds",
        "suburb_slug": "four-winds",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Eloana",
        "suburb_slug": "eloana",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "South Riding",
        "suburb_slug": "south-riding",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Malindela",
        "suburb_slug": "malindela",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Munda",
        "suburb_slug": "munda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Intini",
        "suburb_slug": "intini",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Southdale",
        "suburb_slug": "southdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Bradfield",
        "suburb_slug": "bradfield",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Belmont East",
        "suburb_slug": "belmont-east",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Famona",
        "suburb_slug": "famona",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "buhera",
        "suburb_name": "Buhera",
        "suburb_slug": "buhera",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "chimanimani",
        "suburb_name": "Chimanimani",
        "suburb_slug": "chimanimani",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "chimanimani",
        "suburb_name": "Chimanimani",
        "suburb_slug": "chimanimani",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "chipinge",
        "suburb_name": "Chipinge",
        "suburb_slug": "chipinge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "headlands",
        "suburb_name": "Headlands",
        "suburb_slug": "headlands",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "juliasdale",
        "suburb_name": "Juliasdale",
        "suburb_slug": "juliasdale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "makoni",
        "suburb_name": "Makoni",
        "suburb_slug": "makoni",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "musikavanhu",
        "suburb_name": "Musikavanhu",
        "suburb_slug": "musikavanhu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Chikanga",
        "suburb_slug": "chikanga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Mutare CBD",
        "suburb_slug": "mutare-cbd",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Fairbridge Park",
        "suburb_slug": "fairbridge-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Murambi",
        "suburb_slug": "murambi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Morningside",
        "suburb_slug": "morningside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Tiger's Kloof",
        "suburb_slug": "tigers-kloof",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Palmerston",
        "suburb_slug": "palmerston",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Avenues Mutare",
        "suburb_slug": "avenues-mutare",
        "approved": 0
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Utopia",
        "suburb_slug": "utopia",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Darlington",
        "suburb_slug": "darlington",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Greenside",
        "suburb_slug": "greenside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Yeovil",
        "suburb_slug": "yeovil",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Westlea",
        "suburb_slug": "westlea",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Florida",
        "suburb_slug": "florida",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Toronto",
        "suburb_slug": "toronto",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Sakubva",
        "suburb_slug": "sakubva",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Dangamvura",
        "suburb_slug": "dangamvura",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Weirmouth",
        "suburb_slug": "weirmouth",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Fern Valley",
        "suburb_slug": "fern-valley",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Zimunya",
        "suburb_slug": "zimunya",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Bordervale",
        "suburb_slug": "bordervale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Muchena",
        "suburb_slug": "muchena",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Chisamba",
        "suburb_slug": "chisamba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Mazhambe",
        "suburb_slug": "mazhambe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Maonde Dangare",
        "suburb_slug": "maonde-dangare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Muneni",
        "suburb_slug": "muneni",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Madanza",
        "suburb_slug": "madanza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Park Cottages",
        "suburb_slug": "park-cottages",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Nyakamete",
        "suburb_slug": "nyakamete",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "nyanga",
        "suburb_name": "Nyanga",
        "suburb_slug": "nyanga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "rusape",
        "suburb_name": "Rusape",
        "suburb_slug": "rusape",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "vumba",
        "suburb_name": "Vumba",
        "suburb_slug": "vumba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "penhalonga",
        "suburb_name": "Penhalonga",
        "suburb_slug": "penhalonga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "bikita",
        "suburb_name": "Bikita",
        "suburb_slug": "bikita",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "chiredzi",
        "suburb_name": "Chiredzi",
        "suburb_slug": "chiredzi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "gutu",
        "suburb_name": "Gutu",
        "suburb_slug": "gutu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "masvingo",
        "suburb_name": "Masvingo",
        "suburb_slug": "masvingo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "mwenezi",
        "suburb_name": "Mwenezi",
        "suburb_slug": "mwenezi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "rutenga",
        "suburb_name": "Rutenga",
        "suburb_slug": "rutenga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "triangle",
        "suburb_name": "Triangle",
        "suburb_slug": "triangle",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "masvingo",
        "city_slug": "zaka",
        "suburb_name": "Zaka",
        "suburb_slug": "zaka",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "arcturus",
        "suburb_name": "Arcturus",
        "suburb_slug": "arcturus",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "beatrice",
        "suburb_name": "Beatrice",
        "suburb_slug": "beatrice",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "chikomba",
        "suburb_name": "Chikomba",
        "suburb_slug": "chikomba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "chivhu",
        "suburb_name": "Chivhu",
        "suburb_slug": "chivhu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "damofalls",
        "suburb_name": "Damofalls",
        "suburb_slug": "damofalls",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "goromonzi",
        "suburb_name": "Goromonzi",
        "suburb_slug": "goromonzi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "marondera",
        "suburb_name": "Marondera",
        "suburb_slug": "marondera",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "mudzi",
        "suburb_name": "Mudzi",
        "suburb_slug": "mudzi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "murehwa",
        "suburb_name": "Murehwa",
        "suburb_slug": "murehwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "mutoko",
        "suburb_name": "Mutoko",
        "suburb_slug": "mutoko",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "seke",
        "suburb_name": "Seke",
        "suburb_slug": "seke",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "wedza",
        "suburb_name": "Wedza",
        "suburb_slug": "wedza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "domboshawa",
        "suburb_name": "Domboshawa",
        "suburb_slug": "domboshawa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "dema",
        "suburb_name": "Dema",
        "suburb_slug": "dema",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-east",
        "city_slug": "macheke",
        "suburb_name": "Macheke",
        "suburb_slug": "macheke",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "bindura",
        "suburb_name": "Bindura",
        "suburb_slug": "bindura",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "centenary",
        "suburb_name": "Centenary",
        "suburb_slug": "centenary",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "christon",
        "suburb_name": "Christon",
        "suburb_slug": "christon",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "concession",
        "suburb_name": "Concession",
        "suburb_slug": "concession",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "guruve",
        "suburb_name": "Guruve",
        "suburb_slug": "guruve",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "mazowe",
        "suburb_name": "Mazowe",
        "suburb_slug": "mazowe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "mt-darwin",
        "suburb_name": "Mt Darwin",
        "suburb_slug": "mt-darwin",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "mvurwi",
        "suburb_name": "Mvurwi",
        "suburb_slug": "mvurwi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "rushinga",
        "suburb_name": "Rushinga",
        "suburb_slug": "rushinga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "shamva",
        "suburb_name": "Shamva",
        "suburb_slug": "shamva",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "mbire",
        "suburb_name": "Mbire",
        "suburb_slug": "mbire",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-central",
        "city_slug": "centenary",
        "suburb_name": "Centenary",
        "suburb_slug": "centenary",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "banket",
        "suburb_name": "Banket",
        "suburb_slug": "banket",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "chegutu",
        "suburb_name": "Chegutu",
        "suburb_slug": "chegutu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "chinhoyi",
        "suburb_name": "Chinhoyi",
        "suburb_slug": "chinhoyi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "chirundu",
        "suburb_name": "Chirundu",
        "suburb_slug": "chirundu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "darwendale",
        "suburb_name": "Darwendale",
        "suburb_slug": "darwendale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "hurungwe",
        "suburb_name": "Hurungwe",
        "suburb_slug": "hurungwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "kadoma",
        "suburb_name": "Kadoma",
        "suburb_slug": "kadoma",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "kariba",
        "suburb_name": "Kariba",
        "suburb_slug": "kariba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "kariba",
        "suburb_name": "Milibizi",
        "suburb_slug": "milibizi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "kariba",
        "suburb_name": "Matusadona National Park",
        "suburb_slug": "matusadona-national-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "karoi",
        "suburb_name": "Karoi",
        "suburb_slug": "karoi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "lake",
        "suburb_name": "Lake",
        "suburb_slug": "lake",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "lower",
        "suburb_name": "Lower",
        "suburb_slug": "lower",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "makonde",
        "suburb_name": "Makonde",
        "suburb_slug": "makonde",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "mazvikadei",
        "suburb_name": "Mazvikadei",
        "suburb_slug": "mazvikadei",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "norton",
        "suburb_name": "Norton",
        "suburb_slug": "norton",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "zambezi",
        "suburb_name": "Zambezi",
        "suburb_slug": "zambezi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "zvimba",
        "suburb_name": "Zvimba",
        "suburb_slug": "zvimba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "selous",
        "suburb_name": "Selous",
        "suburb_slug": "selous",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "raffingora",
        "suburb_name": "Raffingora",
        "suburb_slug": "raffingora",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "mashonaland-west",
        "city_slug": "mhangura",
        "suburb_name": "Mhangura",
        "suburb_slug": "mhangura",
        "approved": 0
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "chirumhanzu",
        "suburb_name": "Chirumhanzu",
        "suburb_slug": "chirumhanzu",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gokwe",
        "suburb_name": "Gokwe",
        "suburb_slug": "gokwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Mkoba",
        "suburb_slug": "mkoba",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Southdowns",
        "suburb_slug": "southdowns",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Northlea",
        "suburb_slug": "northlea",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Lundi Park",
        "suburb_slug": "lundi-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Riverside",
        "suburb_slug": "riverside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Harben park",
        "suburb_slug": "harben-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "St Annes drive",
        "suburb_slug": "st-annes-drive",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Kopje",
        "suburb_slug": "kopje",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Brackenhurst",
        "suburb_slug": "brackenhurst",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Windsor Park",
        "suburb_slug": "windsor-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Shamrock Park",
        "suburb_slug": "shamrock-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Nashville",
        "suburb_slug": "nashville",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Daylesford",
        "suburb_slug": "daylesford",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Senga",
        "suburb_slug": "senga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Nehosho",
        "suburb_slug": "nehosho",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Gweru CBD",
        "suburb_slug": "gweru-cbd",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Gweru East",
        "suburb_slug": "gweru-east",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Athlone",
        "suburb_slug": "athlone",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Mambo",
        "suburb_slug": "mambo",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Mtapa",
        "suburb_slug": "mtapa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Cliffton Park",
        "suburb_slug": "cliffton-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Montrose",
        "suburb_slug": "montrose",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Woodlands Park",
        "suburb_slug": "woodlands-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Ridgemont",
        "suburb_slug": "ridgemont",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Hertfordshire",
        "suburb_slug": "hertfordshire",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Greenvale",
        "suburb_slug": "greenvale",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Northgate Heights",
        "suburb_slug": "northgate-heights",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Ivene",
        "suburb_slug": "ivene",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Southview",
        "suburb_slug": "southview",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Adelaide Pk Gweru",
        "suburb_slug": "adelaide-pk-gweru",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Kingston Park",
        "suburb_slug": "kingston-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Mtausi Park",
        "suburb_slug": "mtausi-park",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Pattergonia",
        "suburb_slug": "pattergonia",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Bradeleys Plots",
        "suburb_slug": "bradeleys-plots",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Lynfield",
        "suburb_slug": "lynfield",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Coolmoreen",
        "suburb_slug": "coolmoreen",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "gweru",
        "suburb_name": "Hertifordshire",
        "suburb_slug": "hertifordshire",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "kwekwe",
        "suburb_name": "Kwekwe",
        "suburb_slug": "kwekwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "mberengwa",
        "suburb_name": "Mberengwa",
        "suburb_slug": "mberengwa",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "redcliff",
        "suburb_name": "Redcliff",
        "suburb_slug": "redcliff",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "shurugwi",
        "suburb_name": "Shurugwi",
        "suburb_slug": "shurugwi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "zvishavane",
        "suburb_name": "Zvishavane",
        "suburb_slug": "zvishavane",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "midlands",
        "city_slug": "mvuma",
        "suburb_name": "Mvuma",
        "suburb_slug": "mvuma",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "binga",
        "suburb_name": "Binga",
        "suburb_slug": "binga",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "bubi",
        "suburb_name": "Bubi",
        "suburb_slug": "bubi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "deka",
        "suburb_name": "Deka",
        "suburb_slug": "deka",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "hwange",
        "suburb_name": "Hwange",
        "suburb_slug": "hwange",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "lupane",
        "suburb_name": "Lupane",
        "suburb_slug": "lupane",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "msuna",
        "suburb_name": "Msuna",
        "suburb_slug": "msuna",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "nkayi",
        "suburb_name": "Nkayi",
        "suburb_slug": "nkayi",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "tsholotsho",
        "suburb_name": "Tsholotsho",
        "suburb_slug": "tsholotsho",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "umguza",
        "suburb_name": "Umguza",
        "suburb_slug": "umguza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-north",
        "city_slug": "victoria-falls",
        "suburb_name": "Victoria Falls",
        "suburb_slug": "victoria-falls",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "beitbridge",
        "suburb_name": "Beitbridge",
        "suburb_slug": "beitbridge",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "bulilimamangwe",
        "suburb_name": "Bulilimamangwe",
        "suburb_slug": "bulilimamangwe",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "figtree",
        "suburb_name": "Figtree",
        "suburb_slug": "figtree",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "gwanda",
        "suburb_name": "Gwanda",
        "suburb_slug": "gwanda",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "insiza",
        "suburb_name": "Insiza",
        "suburb_slug": "insiza",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "matobo",
        "suburb_name": "Matobo",
        "suburb_slug": "matobo",
        "approved": 0
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "plumtree",
        "suburb_name": "Plumtree",
        "suburb_slug": "plumtree",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "shangani",
        "suburb_name": "Shangani",
        "suburb_slug": "shangani",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "matebeleland-south",
        "city_slug": "umzingwane",
        "suburb_name": "Umzingwane",
        "suburb_slug": "umzingwane",
        "approved": 1
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "gauteng",
        "city_slug": "johannesburg",
        "suburb_name": "Sandton",
        "suburb_slug": "sandton",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "gauteng",
        "city_slug": "johannesburg",
        "suburb_name": "Bryanston",
        "suburb_slug": "bryanston",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "gauteng",
        "city_slug": "pretoria",
        "suburb_name": "Pretoria",
        "suburb_slug": "pretoria",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "western-cape",
        "city_slug": "cape-town",
        "suburb_name": "Cape Town",
        "suburb_slug": "cape-town",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "hillcrest",
        "suburb_name": "Hillcrest",
        "suburb_slug": "hillcrest",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "kloof",
        "suburb_name": "Kloof",
        "suburb_slug": "kloof",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "waterfall",
        "suburb_name": "Waterfall",
        "suburb_slug": "waterfall",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "gillitts",
        "suburb_name": "Gillitts",
        "suburb_slug": "gillitts",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "assagay",
        "suburb_name": "Assagay",
        "suburb_slug": "assagay",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "bothas-hill",
        "suburb_name": "Bothas Hill",
        "suburb_slug": "bothas-hill",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "crestholme",
        "suburb_name": "Crestholme",
        "suburb_slug": "crestholme",
        "approved": 0
    },
    {
        "country_code": "ZAF", # South Africa
        "province_slug": "kwazulu-natal",
        "city_slug": "summerveld",
        "suburb_name": "Summerveld",
        "suburb_slug": "summerveld",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "mangochi",
        "suburb_name": "Mangochi",
        "suburb_slug": "mangochi",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "mangochi-town-center",
        "suburb_name": "Mangochi Town Center",
        "suburb_slug": "mangochi-town-center",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "mangochi-township",
        "suburb_name": "Mangochi Township",
        "suburb_slug": "mangochi-township",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "mponda",
        "suburb_name": "Mponda",
        "suburb_slug": "mponda",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "maldeco",
        "suburb_name": "Maldeco",
        "suburb_slug": "maldeco",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "mbwadzulu",
        "suburb_name": "Mbwadzulu",
        "suburb_slug": "mbwadzulu",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "chiponde",
        "suburb_name": "Chiponde",
        "suburb_slug": "chiponde",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "nankumba",
        "suburb_name": "Nankumba",
        "suburb_slug": "nankumba",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "chilipa",
        "suburb_name": "Chilipa",
        "suburb_slug": "chilipa",
        "approved": 0
    },
    {
        "country_code": "MWI", # Malawi
        "province_slug": "blantyre",
        "city_slug": "mangochi-boma",
        "suburb_name": "Mangochi Boma",
        "suburb_slug": "mangochi-boma",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "pemba",
        "suburb_name": "Pemba",
        "suburb_slug": "pemba",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "montepuez",
        "suburb_name": "Montepuez",
        "suburb_slug": "montepuez",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mocimboa-da-praia",
        "suburb_name": "Mocímboa da Praia",
        "suburb_slug": "mocimboa-da-praia",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "palma",
        "suburb_name": "Palma",
        "suburb_slug": "palma",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "macomia",
        "suburb_name": "Macomia",
        "suburb_slug": "macomia",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "quissanga",
        "suburb_name": "Quissanga",
        "suburb_slug": "quissanga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "metuge",
        "suburb_name": "Metuge",
        "suburb_slug": "metuge",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "chiure",
        "suburb_name": "Chiúre",
        "suburb_slug": "chiure",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "ancuabe",
        "suburb_name": "Ancuabe",
        "suburb_slug": "ancuabe",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "ibo",
        "suburb_name": "Ibo",
        "suburb_slug": "ibo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mueda",
        "suburb_name": "Mueda",
        "suburb_slug": "mueda",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "meluco",
        "suburb_name": "Meluco",
        "suburb_slug": "meluco",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "centro",
        "suburb_name": "Centro",
        "suburb_slug": "centro",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "paquitequete",
        "suburb_name": "Paquitequete",
        "suburb_slug": "paquitequete",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "murrebue",
        "suburb_name": "Murrebue",
        "suburb_slug": "murrebue",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "chali",
        "suburb_name": "Chali",
        "suburb_slug": "chali",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "cimento",
        "suburb_name": "Cimento",
        "suburb_slug": "cimento",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "ponta-vermelha",
        "suburb_name": "Ponta Vermelha",
        "suburb_slug": "ponta-vermelha",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "bairro-novo",
        "suburb_name": "Bairro Novo",
        "suburb_slug": "bairro-novo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "nanhime",
        "suburb_name": "Nanhime",
        "suburb_slug": "nanhime",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "murrupula",
        "suburb_name": "Murrupula",
        "suburb_slug": "murrupula",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "muapula",
        "suburb_name": "Muapula",
        "suburb_slug": "muapula",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mutiva",
        "suburb_name": "Mutiva",
        "suburb_slug": "mutiva",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "muiuane",
        "suburb_name": "Muiuane",
        "suburb_slug": "muiuane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mussoromosso",
        "suburb_name": "Mussoromosso",
        "suburb_slug": "mussoromosso",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "alto-da-manga",
        "suburb_name": "Alto da Manga",
        "suburb_slug": "alto-da-manga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mia-couto",
        "suburb_name": "Mia Couto",
        "suburb_slug": "mia-couto",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "baixa",
        "suburb_name": "Baixa",
        "suburb_slug": "baixa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mucojo",
        "suburb_name": "Mucojo",
        "suburb_slug": "mucojo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "manilha",
        "suburb_name": "Manilha",
        "suburb_slug": "manilha",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "areias",
        "suburb_name": "Areias",
        "suburb_slug": "areias",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "quibuidine",
        "suburb_name": "Quibuidine",
        "suburb_slug": "quibuidine",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "zona-verde",
        "suburb_name": "Zona Verde",
        "suburb_slug": "zona-verde",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "nova-vida",
        "suburb_name": "Nova Vida",
        "suburb_slug": "nova-vida",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "quelimane",
        "suburb_name": "Quelimane",
        "suburb_slug": "quelimane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "muxungue",
        "suburb_name": "Muxúnguè",
        "suburb_slug": "muxungue",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "pangane",
        "suburb_name": "Pangane",
        "suburb_slug": "pangane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "matemo",
        "suburb_name": "Matemo",
        "suburb_slug": "matemo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "quionga",
        "suburb_name": "Quionga",
        "suburb_slug": "quionga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mecufi",
        "suburb_name": "Mecufi",
        "suburb_slug": "mecufi",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "nacotuco",
        "suburb_name": "Nacotuco",
        "suburb_slug": "nacotuco",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mecula",
        "suburb_name": "Mecula",
        "suburb_slug": "mecula",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "meza",
        "suburb_name": "Meza",
        "suburb_slug": "meza",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "nairoto",
        "suburb_name": "Nairoto",
        "suburb_slug": "nairoto",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "mpunga",
        "suburb_name": "M'punga",
        "suburb_slug": "mpunga",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "cobaia",
        "suburb_name": "Cobaia",
        "suburb_slug": "cobaia",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "napupa",
        "suburb_name": "Napupa",
        "suburb_slug": "napupa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "napapa",
        "suburb_name": "Napapa",
        "suburb_slug": "napapa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "nacujo",
        "suburb_name": "Nacujo",
        "suburb_slug": "nacujo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "napome",
        "suburb_name": "Napome",
        "suburb_slug": "napome",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "nagaze",
        "suburb_name": "Nagaze",
        "suburb_slug": "nagaze",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "porto",
        "suburb_name": "Porto",
        "suburb_slug": "porto",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "fortaleza",
        "suburb_name": "Fortaleza",
        "suburb_slug": "fortaleza",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "cabo",
        "suburb_name": "Cabo",
        "suburb_slug": "cabo",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "makuti",
        "suburb_name": "Makuti",
        "suburb_slug": "makuti",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "administrative-center",
        "suburb_name": "Administrative Center",
        "suburb_slug": "administrative-center",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "local-villages",
        "suburb_name": "Local Villages",
        "suburb_slug": "local-villages",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "rural-communities",
        "suburb_name": "Rural Communities",
        "suburb_slug": "rural-communities",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "agricultural-areas",
        "suburb_name": "Agricultural Areas",
        "suburb_slug": "agricultural-areas",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "market-centers",
        "suburb_name": "Market Centers",
        "suburb_slug": "market-centers",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "cabo-delgado",
        "city_slug": "traditional-communal-areas",
        "suburb_name": "Traditional Communal Areas",
        "suburb_slug": "traditional-communal-areas",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Machava",
        "suburb_slug": "machava",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Mavalane",
        "suburb_slug": "mavalane",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Polana",
        "suburb_slug": "polana",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Sommerschield",
        "suburb_slug": "sommerschield",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Costa do Sol",
        "suburb_slug": "costa-do-sol",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Baixa",
        "suburb_slug": "baixa",
        "approved": 0
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Museu",
        "suburb_slug": "museu",
        "approved": 1
    },
    {
        "country_code": "MOZ", # Mozambique
        "province_slug": "maputo",
        "city_slug": "maputo",
        "suburb_name": "Central A",
        "suburb_slug": "central-a",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Rietfontein",
        "suburb_slug": "rietfontein",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Avenues (Harare)",
        "suburb_slug": "avenues-harare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "manicaland",
        "city_slug": "mutare",
        "suburb_name": "Avenues (Mutare)",
        "suburb_slug": "avenues-mutare",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Bluff Hill",
        "suburb_slug": "bluff-hill",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Nyabira",
        "suburb_slug": "nyabira",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "bulawayo",
        "city_slug": "bulawayo",
        "suburb_name": "Burnside",
        "suburb_slug": "burnside",
        "approved": 1
    },
    {
        "country_code": "ZW", # Zimbabwe
        "province_slug": "harare",
        "city_slug": "harare",
        "suburb_name": "Mount Hampden",
        "suburb_slug": "mount-hampden",
        "approved": 1
    },
]

