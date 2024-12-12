# Module: NLP
# # Author: satish kumar <sathishsriram999@gmail.com>
# # License: MIT
# Release: Trinity-Neo 1.0
# Last modified : 11/12/2024

import langid
import json
import re
from multi_rake import Rake
#nlp = spacy.load('en_core_web_sm')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia_obj = SentimentIntensityAnalyzer()

lang_data = {
    "ab":{
        "name":"Abkhaz",
        "nativeName":"аҧсуа"
    },
    "aa":{
        "name":"Afar",
        "nativeName":"Afaraf"
    },
    "af":{
        "name":"Afrikaans",
        "nativeName":"Afrikaans"
    },
    "ak":{
        "name":"Akan",
        "nativeName":"Akan"
    },
    "sq":{
        "name":"Albanian",
        "nativeName":"Shqip"
    },
    "am":{
        "name":"Amharic",
        "nativeName":"አማርኛ"
    },
    "ar":{
        "name":"Arabic",
        "nativeName":"العربية"
    },
    "an":{
        "name":"Aragonese",
        "nativeName":"Aragonés"
    },
    "hy":{
        "name":"Armenian",
        "nativeName":"Հայերեն"
    },
    "as":{
        "name":"Assamese",
        "nativeName":"অসমীয়া"
    },
    "av":{
        "name":"Avaric",
        "nativeName":"авар мацӀ, магӀарул мацӀ"
    },
    "ae":{
        "name":"Avestan",
        "nativeName":"avesta"
    },
    "ay":{
        "name":"Aymara",
        "nativeName":"aymar aru"
    },
    "az":{
        "name":"Azerbaijani",
        "nativeName":"azərbaycan dili"
    },
    "bm":{
        "name":"Bambara",
        "nativeName":"bamanankan"
    },
    "ba":{
        "name":"Bashkir",
        "nativeName":"башҡорт теле"
    },
    "eu":{
        "name":"Basque",
        "nativeName":"euskara, euskera"
    },
    "be":{
        "name":"Belarusian",
        "nativeName":"Беларуская"
    },
    "bn":{
        "name":"Bengali",
        "nativeName":"বাংলা"
    },
    "bh":{
        "name":"Bihari",
        "nativeName":"भोजपुरी"
    },
    "bi":{
        "name":"Bislama",
        "nativeName":"Bislama"
    },
    "bs":{
        "name":"Bosnian",
        "nativeName":"bosanski jezik"
    },
    "br":{
        "name":"Breton",
        "nativeName":"brezhoneg"
    },
    "bg":{
        "name":"Bulgarian",
        "nativeName":"български език"
    },
    "my":{
        "name":"Burmese",
        "nativeName":"ဗမာစာ"
    },
    "ca":{
        "name":"Catalan; Valencian",
        "nativeName":"Català"
    },
    "ch":{
        "name":"Chamorro",
        "nativeName":"Chamoru"
    },
    "ce":{
        "name":"Chechen",
        "nativeName":"нохчийн мотт"
    },
    "ny":{
        "name":"Chichewa; Chewa; Nyanja",
        "nativeName":"chiCheŵa, chinyanja"
    },
    "zh":{
        "name":"Chinese",
        "nativeName":"中文 (Zhōngwén), 汉语, 漢語"
    },
    "cv":{
        "name":"Chuvash",
        "nativeName":"чӑваш чӗлхи"
    },
    "kw":{
        "name":"Cornish",
        "nativeName":"Kernewek"
    },
    "co":{
        "name":"Corsican",
        "nativeName":"corsu, lingua corsa"
    },
    "cr":{
        "name":"Cree",
        "nativeName":"ᓀᐦᐃᔭᐍᐏᐣ"
    },
    "hr":{
        "name":"Croatian",
        "nativeName":"hrvatski"
    },
    "cs":{
        "name":"Czech",
        "nativeName":"česky, čeština"
    },
    "da":{
        "name":"Danish",
        "nativeName":"dansk"
    },
    "dv":{
        "name":"Divehi; Dhivehi; Maldivian;",
        "nativeName":"ދިވެހި"
    },
    "nl":{
        "name":"Dutch",
        "nativeName":"Nederlands, Vlaams"
    },
    "en":{
        "name":"English",
        "nativeName":"English"
    },
    "eo":{
        "name":"Esperanto",
        "nativeName":"Esperanto"
    },
    "et":{
        "name":"Estonian",
        "nativeName":"eesti, eesti keel"
    },
    "ee":{
        "name":"Ewe",
        "nativeName":"Eʋegbe"
    },
    "fo":{
        "name":"Faroese",
        "nativeName":"føroyskt"
    },
    "fj":{
        "name":"Fijian",
        "nativeName":"vosa Vakaviti"
    },
    "fi":{
        "name":"Finnish",
        "nativeName":"suomi, suomen kieli"
    },
    "fr":{
        "name":"French",
        "nativeName":"français, langue française"
    },
    "ff":{
        "name":"Fula; Fulah; Pulaar; Pular",
        "nativeName":"Fulfulde, Pulaar, Pular"
    },
    "gl":{
        "name":"Galician",
        "nativeName":"Galego"
    },
    "ka":{
        "name":"Georgian",
        "nativeName":"ქართული"
    },
    "de":{
        "name":"German",
        "nativeName":"Deutsch"
    },
    "el":{
        "name":"Greek, Modern",
        "nativeName":"Ελληνικά"
    },
    "gn":{
        "name":"Guaraní",
        "nativeName":"Avañeẽ"
    },
    "gu":{
        "name":"Gujarati",
        "nativeName":"ગુજરાતી"
    },
    "ht":{
        "name":"Haitian; Haitian Creole",
        "nativeName":"Kreyòl ayisyen"
    },
    "ha":{
        "name":"Hausa",
        "nativeName":"Hausa, هَوُسَ"
    },
    "he":{
        "name":"Hebrew",
        "nativeName":"עברית"
    },
    "iw":{
        "name":"Hebrew",
        "nativeName":"עברית"
    },
    "hz":{
        "name":"Herero",
        "nativeName":"Otjiherero"
    },
    "hi":{
        "name":"Hindi",
        "nativeName":"हिन्दी, हिंदी"
    },
    "ho":{
        "name":"Hiri Motu",
        "nativeName":"Hiri Motu"
    },
    "hu":{
        "name":"Hungarian",
        "nativeName":"Magyar"
    },
    "ia":{
        "name":"Interlingua",
        "nativeName":"Interlingua"
    },
    "id":{
        "name":"Indonesian",
        "nativeName":"Bahasa Indonesia"
    },
    "ie":{
        "name":"Interlingue",
        "nativeName":"Originally called Occidental; then Interlingue after WWII"
    },
    "ga":{
        "name":"Irish",
        "nativeName":"Gaeilge"
    },
    "ig":{
        "name":"Igbo",
        "nativeName":"Asụsụ Igbo"
    },
    "ik":{
        "name":"Inupiaq",
        "nativeName":"Iñupiaq, Iñupiatun"
    },
    "io":{
        "name":"Ido",
        "nativeName":"Ido"
    },
    "is":{
        "name":"Icelandic",
        "nativeName":"Íslenska"
    },
    "it":{
        "name":"Italian",
        "nativeName":"Italiano"
    },
    "iu":{
        "name":"Inuktitut",
        "nativeName":"ᐃᓄᒃᑎᑐᑦ"
    },
    "ja":{
        "name":"Japanese",
        "nativeName":"日本語 (にほんご／にっぽんご)"
    },
    "jv":{
        "name":"Javanese",
        "nativeName":"basa Jawa"
    },
    "kl":{
        "name":"Kalaallisut, Greenlandic",
        "nativeName":"kalaallisut, kalaallit oqaasii"
    },
    "kn":{
        "name":"Kannada",
        "nativeName":"ಕನ್ನಡ"
    },
    "kr":{
        "name":"Kanuri",
        "nativeName":"Kanuri"
    },
    "ks":{
        "name":"Kashmiri",
        "nativeName":"कश्मीरी, كشميري‎"
    },
    "kk":{
        "name":"Kazakh",
        "nativeName":"Қазақ тілі"
    },
    "km":{
        "name":"Khmer",
        "nativeName":"ភាសាខ្មែរ"
    },
    "ki":{
        "name":"Kikuyu, Gikuyu",
        "nativeName":"Gĩkũyũ"
    },
    "rw":{
        "name":"Kinyarwanda",
        "nativeName":"Ikinyarwanda"
    },
    "ky":{
        "name":"Kirghiz, Kyrgyz",
        "nativeName":"кыргыз тили"
    },
    "kv":{
        "name":"Komi",
        "nativeName":"коми кыв"
    },
    "kg":{
        "name":"Kongo",
        "nativeName":"KiKongo"
    },
    "ko":{
        "name":"Korean",
        "nativeName":"한국어 (韓國語), 조선말 (朝鮮語)"
    },
    "ku":{
        "name":"Kurdish",
        "nativeName":"Kurdî, كوردی‎"
    },
    "kj":{
        "name":"Kwanyama, Kuanyama",
        "nativeName":"Kuanyama"
    },
    "la":{
        "name":"Latin",
        "nativeName":"latine, lingua latina"
    },
    "lb":{
        "name":"Luxembourgish, Letzeburgesch",
        "nativeName":"Lëtzebuergesch"
    },
    "lg":{
        "name":"Luganda",
        "nativeName":"Luganda"
    },
    "li":{
        "name":"Limburgish, Limburgan, Limburger",
        "nativeName":"Limburgs"
    },
    "ln":{
        "name":"Lingala",
        "nativeName":"Lingála"
    },
    "lo":{
        "name":"Lao",
        "nativeName":"ພາສາລາວ"
    },
    "lt":{
        "name":"Lithuanian",
        "nativeName":"lietuvių kalba"
    },
    "lu":{
        "name":"Luba-Katanga",
        "nativeName":""
    },
    "lv":{
        "name":"Latvian",
        "nativeName":"latviešu valoda"
    },
    "gv":{
        "name":"Manx",
        "nativeName":"Gaelg, Gailck"
    },
    "mk":{
        "name":"Macedonian",
        "nativeName":"македонски јазик"
    },
    "mg":{
        "name":"Malagasy",
        "nativeName":"Malagasy fiteny"
    },
    "ms":{
        "name":"Malay",
        "nativeName":"bahasa Melayu, بهاس ملايو‎"
    },
    "ml":{
        "name":"Malayalam",
        "nativeName":"മലയാളം"
    },
    "mt":{
        "name":"Maltese",
        "nativeName":"Malti"
    },
    "mi":{
        "name":"Māori",
        "nativeName":"te reo Māori"
    },
    "mr":{
        "name":"Marathi (Marāṭhī)",
        "nativeName":"मराठी"
    },
    "mh":{
        "name":"Marshallese",
        "nativeName":"Kajin M̧ajeļ"
    },
    "mn":{
        "name":"Mongolian",
        "nativeName":"монгол"
    },
    "na":{
        "name":"Nauru",
        "nativeName":"Ekakairũ Naoero"
    },
    "nv":{
        "name":"Navajo, Navaho",
        "nativeName":"Diné bizaad, Dinékʼehǰí"
    },
    "nb":{
        "name":"Norwegian Bokmål",
        "nativeName":"Norsk bokmål"
    },
    "nd":{
        "name":"North Ndebele",
        "nativeName":"isiNdebele"
    },
    "ne":{
        "name":"Nepali",
        "nativeName":"नेपाली"
    },
    "ng":{
        "name":"Ndonga",
        "nativeName":"Owambo"
    },
    "nn":{
        "name":"Norwegian Nynorsk",
        "nativeName":"Norsk nynorsk"
    },
    "no":{
        "name":"Norwegian",
        "nativeName":"Norsk"
    },
    "ii":{
        "name":"Nuosu",
        "nativeName":"ꆈꌠ꒿ Nuosuhxop"
    },
    "nr":{
        "name":"South Ndebele",
        "nativeName":"isiNdebele"
    },
    "oc":{
        "name":"Occitan",
        "nativeName":"Occitan"
    },
    "oj":{
        "name":"Ojibwe, Ojibwa",
        "nativeName":"ᐊᓂᔑᓈᐯᒧᐎᓐ"
    },
    "cu":{
        "name":"Old Church Slavonic, Church Slavic, Church Slavonic, Old Bulgarian, Old Slavonic",
        "nativeName":"ѩзыкъ словѣньскъ"
    },
    "om":{
        "name":"Oromo",
        "nativeName":"Afaan Oromoo"
    },
    "or":{
        "name":"Oriya",
        "nativeName":"ଓଡ଼ିଆ"
    },
    "os":{
        "name":"Ossetian, Ossetic",
        "nativeName":"ирон æвзаг"
    },
    "pa":{
        "name":"Panjabi, Punjabi",
        "nativeName":"ਪੰਜਾਬੀ, پنجابی‎"
    },
    "pi":{
        "name":"Pāli",
        "nativeName":"पाऴि"
    },
    "fa":{
        "name":"Persian",
        "nativeName":"فارسی"
    },
    "pl":{
        "name":"Polish",
        "nativeName":"polski"
    },
    "ps":{
        "name":"Pashto, Pushto",
        "nativeName":"پښتو"
    },
    "pt":{
        "name":"Portuguese",
        "nativeName":"Português"
    },
    "qu":{
        "name":"Quechua",
        "nativeName":"Runa Simi, Kichwa"
    },
    "rm":{
        "name":"Romansh",
        "nativeName":"rumantsch grischun"
    },
    "rn":{
        "name":"Kirundi",
        "nativeName":"kiRundi"
    },
    "ro":{
        "name":"Romanian, Moldavian, Moldovan",
        "nativeName":"română"
    },
    "ru":{
        "name":"Russian",
        "nativeName":"русский язык"
    },
    "sa":{
        "name":"Sanskrit (Saṁskṛta)",
        "nativeName":"संस्कृतम्"
    },
    "sc":{
        "name":"Sardinian",
        "nativeName":"sardu"
    },
    "sd":{
        "name":"Sindhi",
        "nativeName":"सिन्धी, سنڌي، سندھی‎"
    },
    "se":{
        "name":"Northern Sami",
        "nativeName":"Davvisámegiella"
    },
    "sm":{
        "name":"Samoan",
        "nativeName":"gagana faa Samoa"
    },
    "sg":{
        "name":"Sango",
        "nativeName":"yângâ tî sängö"
    },
    "sr":{
        "name":"Serbian",
        "nativeName":"српски језик"
    },
    "gd":{
        "name":"Scottish Gaelic; Gaelic",
        "nativeName":"Gàidhlig"
    },
    "sn":{
        "name":"Shona",
        "nativeName":"chiShona"
    },
    "si":{
        "name":"Sinhala, Sinhalese",
        "nativeName":"සිංහල"
    },
    "sk":{
        "name":"Slovak",
        "nativeName":"slovenčina"
    },
    "sl":{
        "name":"Slovene",
        "nativeName":"slovenščina"
    },
    "so":{
        "name":"Somali",
        "nativeName":"Soomaaliga, af Soomaali"
    },
    "st":{
        "name":"Southern Sotho",
        "nativeName":"Sesotho"
    },
    "es":{
        "name":"Spanish; Castilian",
        "nativeName":"español, castellano"
    },
    "su":{
        "name":"Sundanese",
        "nativeName":"Basa Sunda"
    },
    "sw":{
        "name":"Swahili",
        "nativeName":"Kiswahili"
    },
    "ss":{
        "name":"Swati",
        "nativeName":"SiSwati"
    },
    "sv":{
        "name":"Swedish",
        "nativeName":"svenska"
    },
    "ta":{
        "name":"Tamil",
        "nativeName":"தமிழ்"
    },
    "te":{
        "name":"Telugu",
        "nativeName":"తెలుగు"
    },
    "tg":{
        "name":"Tajik",
        "nativeName":"тоҷикӣ, toğikī, تاجیکی‎"
    },
    "th":{
        "name":"Thai",
        "nativeName":"ไทย"
    },
    "ti":{
        "name":"Tigrinya",
        "nativeName":"ትግርኛ"
    },
    "bo":{
        "name":"Tibetan Standard, Tibetan, Central",
        "nativeName":"བོད་ཡིག"
    },
    "tk":{
        "name":"Turkmen",
        "nativeName":"Türkmen, Түркмен"
    },
    "tl":{
        "name":"Tagalog",
        "nativeName":"Wikang Tagalog, ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔"
    },
    "tn":{
        "name":"Tswana",
        "nativeName":"Setswana"
    },
    "to":{
        "name":"Tonga (Tonga Islands)",
        "nativeName":"faka Tonga"
    },
    "tr":{
        "name":"Turkish",
        "nativeName":"Türkçe"
    },
    "ts":{
        "name":"Tsonga",
        "nativeName":"Xitsonga"
    },
    "tt":{
        "name":"Tatar",
        "nativeName":"татарча, tatarça, تاتارچا‎"
    },
    "tw":{
        "name":"Twi",
        "nativeName":"Twi"
    },
    "ty":{
        "name":"Tahitian",
        "nativeName":"Reo Tahiti"
    },
    "ug":{
        "name":"Uighur, Uyghur",
        "nativeName":"Uyƣurqə, ئۇيغۇرچە‎"
    },
    "uk":{
        "name":"Ukrainian",
        "nativeName":"українська"
    },
    "ur":{
        "name":"Urdu",
        "nativeName":"اردو"
    },
    "uz":{
        "name":"Uzbek",
        "nativeName":"zbek, Ўзбек, أۇزبېك‎"
    },
    "ve":{
        "name":"Venda",
        "nativeName":"Tshivenḓa"
    },
    "vi":{
        "name":"Vietnamese",
        "nativeName":"Tiếng Việt"
    },
    "vo":{
        "name":"Volapük",
        "nativeName":"Volapük"
    },
    "wa":{
        "name":"Walloon",
        "nativeName":"Walon"
    },
    "cy":{
        "name":"Welsh",
        "nativeName":"Cymraeg"
    },
    "wo":{
        "name":"Wolof",
        "nativeName":"Wollof"
    },
    "fy":{
        "name":"Western Frisian",
        "nativeName":"Frysk"
    },
    "xh":{
        "name":"Xhosa",
        "nativeName":"isiXhosa"
    },
    "yi":{
        "name":"Yiddish",
        "nativeName":"ייִדיש"
    },
    "yo":{
        "name":"Yoruba",
        "nativeName":"Yorùbá"
    },
    "za":{
        "name":"Zhuang, Chuang",
        "nativeName":"Saɯ cueŋƅ, Saw cuengh"
    }
}

                                        ## detecting language ##

def lang_detection(text):
    testing_text = text
    lang_id = langid.classify(testing_text)
    #print(lang_id)
    lang_code = lang_id[0]
    #print(lang_code)
    map_lang = lang_data[lang_code]['name']
    #print(map_lang)
    return map_lang

def language_detection(text):
    testing_text = text
    # detecting the given language
    lang = lang_detection(testing_text)
    language = {"language": lang}
    return language


                                   ## sentiment analysis ##

def sentiment_scores(text):
    sentiment_dict = sia_obj.polarity_scores(text)
    if sentiment_dict['compound'] >= 0.05:
        sentiment = "Positive"
    elif sentiment_dict['compound'] <= - 0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment

def sentiment_analysis(summary):
    text = summary
    # sentiment analysis
    sentiment = sentiment_scores(text)
    sentiment = {"sentiment": sentiment}
    return sentiment

                                 ## extracting top key words ##

def pre_process(text):
    text = text
    # lowercase
    text = text.lower()
    # remove tags
    text = re.sub("</?.*?>", " <> ", text)
    # removing single characters
    text = re.sub(r"\s+[a-zA-Z]\s+", " ", text)
    # remove special characters
    text = re.sub("(\\W)+", " ", text)
    # count_vectorizer
    docs=[text]
    # eliminate stop words
    cv = CountVectorizer(stop_words=stop_words)
    word_count_vector=cv.fit_transform(docs)
    # tf_idf_transformer
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    doc = text
    tfidf_vector = tfidf_transformer.transform(cv.transform([doc]))
    feature_names = cv.get_feature_names()
    return tfidf_vector, feature_names

def sort_keywords(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    sorted_items = sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
    return sorted_items

def extract_topn_keywords(feature_names, sorted_items, topn=10):
    # use only topn items from vector
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 2))
        feature_vals.append(feature_names[idx])
    # create a tuples of feature,score
    key_words = {}
    for idx in range(len(feature_vals)):
        key_words[feature_vals[idx]] = score_vals[idx]
    return key_words

def top_keywords(text):
    # keyword extraction
    tfidf_vector, feature_names =  pre_process(text)
    sorted_items = sort_keywords(tfidf_vector.tocoo())
    key_words = extract_topn_keywords(feature_names, sorted_items, topn=10)
    keywords = {'keywords':key_words}
    return keywords


                                ## extracting top key phrases ##

def extract_topn_keyphrases(text):
    rake = Rake(min_chars=5, max_words=10, min_freq=1, stopwords=stop_words)
    # To get keyword phrases ranked highest to lowest.
    keyphrases = rake.apply(text=text)
    a = []
    b = []
    for i in keyphrases:
        phrases = i[0]
        scores = i[1]
        a.append(phrases)
        b.append(round(scores,4))
    top_keyphrases = dict(zip(a, b))
    return top_keyphrases

def top_keyphrases(text):
    # key phrase extraction
    keyphrases = extract_topn_keyphrases(text)
    keyphrases = {"keyphrases":keyphrases}
    return keyphrases

                                ## extracting url's and emails ##


def extract_url(text):
    # lowercase
    text_lower = text.lower()
    # url tag
    url = re.findall(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", text_lower)
    url = {"detected_url": url}
    return url

def extract_email(text):
    text_lower = text.lower()
    # email tag
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text_lower)
    email = {"detected_email": email}
    return email
