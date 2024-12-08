import json
import Levenshtein
from typing import Mapping
import logging
import re
import json
import pkg_resources
import warnings
warnings.filterwarnings('ignore')

class LughaatNLP:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        lemma_data = pkg_resources.resource_string(__name__, 'Urdu_Lemma.json')
        self.lemmatization_dict = json.loads(lemma_data)

        stopwords_data = pkg_resources.resource_string(__name__, 'stopwords.json')
        self.stopwords_data = json.loads(stopwords_data)

        tokenizer_data = pkg_resources.resource_string(__name__, 'tokenizer.json')
        self.tokenizer_word_index = json.loads(tokenizer_data)
        self.all_words = self.tokenizer_word_index.keys()
        
        self.rules = {
            'ں$': '', 
            'یوں$': 'ی', 
            'یاں$': 'ی',  
            'ات$': 'ه', 
            'وں$': 'ا', 
            'یں$': 'ا',  
            'ان$': '',  
            'ے$': 'ہ', 
            'ؤں$': 'ا',  
            '^میں$': 'میں',  
            '^ہمیں$': 'ہم',  
            'فرائض': 'فرض',  
            'تا': 'ت',  
            'با': 'ب',  
            r'یاں\b': 'ی', 
            '^کھڑکی$': 'کھڑکی', 
            r'ے\b': 'ہ', 
            '^پڑھ.*$': 'پڑھ'  
        }
        
        self.URDU_PUNCTUATIONS = ['-', '؟', '۔', '،' , '.' , ',' , '!']

        self.SPACE_AFTER_PUNCTUATIONS_RE = re.compile(
            r"(?<=[" + "".join(self.URDU_PUNCTUATIONS) + r"])(?=[^" + "".join(self.URDU_PUNCTUATIONS) + r"0-9\n])",
            flags=re.U | re.M | re.I)

        self.REMOVE_SPACE_BEFORE_PUNCTUATIONS_RE = re.compile(
            r'\s+([' + re.escape("".join(self.URDU_PUNCTUATIONS)) + r'\-])',
            flags=re.U | re.M | re.I)

   
        self.CORRECT_URDU_CHARACTERS_MAPPING: Mapping[str, str] = {
            'آ': 'ا', 'أ': 'ا', 'ا': 'ا', 'ب': 'ب', 'پ': 'پ', 'ت': 'ت', 'ٹ': 'ٹ',
            'ث': 'ث', 'ج': 'ج', 'چ': 'چ', 'ح': 'ح', 'خ': 'خ', 'د': 'د', 'ڈ': 'ڈ',
            'ذ': 'ذ', 'ر': 'ر', 'ڑ': 'ڑ', 'ز': 'ز', 'ژ': 'ژ', 'س': 'س', 'ش': 'ش',
            'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع', 'غ': 'غ', 'ف': 'ف',
            'ق': 'ق', 'ک': 'ک', 'گ': 'گ', 'ل': 'ل', 'م': 'م', 'ن': 'ن', 'ں': 'ں',
            'و': 'و', 'ہ': 'ہ', 'ھ': 'ھ', 'ء': 'ء', 'ی': 'ی', 'ئ': 'ئ', 'ے': 'ے',
            'ۓ': 'ے', '۰': '۰', '۱': '۱', '۲': '۲', '۳': '۳', '۴': '۴', '۵': '۵',
            '۶': '۶', '۷': '۷', '۸': '۸', '۹': '۹'
        }

        self.COMBINE_URDU_CHARACTERS = self.COMBINE_URDU_CHARACTERS = {
                            "آ": "آ",
                            "أ": "أ",
                            "ۓ": "ۓ",
                            "اً": "اً",
                            "اٌ": "اٌ",
                            "اٍ": "اٍ",
                            "بً": "بً",
                            "بٌ": "بٌ",
                            "بٍ": "بٍ",
                            "تً": "تً",
                            "تٌ": "تٌ",
                            "تٍ": "تٍ",
                            "ثً": "ثً",
                            "ثٌ": "ثٌ",
                            "ثٍ": "ثٍ",
                            "جً": "جً",
                            "جٌ": "جٌ",
                            "جٍ": "جٍ",
                            "حً": "حً",
                            "حٌ": "حٌ",
                            "حٍ": "حٍ",
                            "خً": "خً",
                            "خٌ": "خٌ",
                            "خٍ": "خٍ",
                            "دً": "دً",
                            "دٌ": "دٌ",
                            "دٍ": "دٍ",
                            "ذً": "ذً",
                            "ذٌ": "ذٌ",
                            "ذٍ": "ذٍ",
                            "رً": "رً",
                            "رٌ": "رٌ",
                            "رٍ": "رٍ",
                            "زً": "زً",
                            "زٌ": "زٌ",
                            "زٍ": "زٍ",
                            "سً": "سً",
                            "سٌ": "سٌ",
                            "سٍ": "سٍ",

        }

        self.URDU_ENG_DIGITS_MAP: Mapping[str, str] = {
            '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
            '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
        }

        self.ENG_URDU_DIGITS_MAP: Mapping[str, str] = {v: k for k, v in self.URDU_ENG_DIGITS_MAP.items()}

    def normalize_characters(self, text: str) -> str:
        return text.translate(self.CORRECT_URDU_CHARACTERS_MAPPING)

    def normalize_combine_characters(self, text: str) -> str:
        pattern = '|'.join(map(re.escape, self.COMBINE_URDU_CHARACTERS.keys()))
        replacements = {k: v for k, v in self.COMBINE_URDU_CHARACTERS.items()}
        return re.sub(pattern, lambda m: replacements[m.group()], text)

    def remove_diacritics(self, text: str) -> str:
        pattern = re.compile(r'آ')
        text = pattern.sub('ا', text)
        diacritics_pattern = r'[\u0617-\u061A\u064B-\u0652]'
        return re.sub(diacritics_pattern, '', text)

    def punctuations_space(self, text: str) -> str:
        text = text.replace('-', '۔')
        text = self.SPACE_AFTER_PUNCTUATIONS_RE.sub(' ', text)
        text = self.REMOVE_SPACE_BEFORE_PUNCTUATIONS_RE.sub(r'\1', text)
        return text

    def replace_digits(self, text: str, with_english: bool = True) -> str:
        digits_map = self.ENG_URDU_DIGITS_MAP if with_english else self.URDU_ENG_DIGITS_MAP
        translator = {}
        for key, value in digits_map.items():
            translator[ord(key)] = value
        return text.translate(translator)

    def remove_whitespace(self, text: str) -> str:
        return ' '.join(text.split())

    def preserve_special_characters(self, text: str) -> str:
        special_characters_pattern = r'(?<=[!@#$&*=_+,.؟۔-])|(?=[!@#$&*=_+,.؟۔-])'
        text = re.sub(special_characters_pattern, ' ', text)
        return self.remove_whitespace(text)

    def normalize(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Text must be str type.")
        self.logger.info("Normalizing the text.")
        text = self.normalize_characters(text)
        text = self.normalize_combine_characters(text)
        text = self.remove_diacritics(text)
        text = self.punctuations_space(text)
        text = self.replace_digits(text)
        text = self.preserve_special_characters(text)
        text = self.remove_whitespace(text)

        return text

    def remove_stopwords(self, sentence):
        sentence = self.preserve_special_characters(sentence)
        sentence = self.remove_whitespace(sentence)
        stopwords = self.stopwords_data["stopwords"]

        words = sentence.split()
        filtered_words = [word for word in words if word not in stopwords]

        return ' '.join(filtered_words)
    
    def add_stopword(self, word):
        if word not in self.stopwords_data["stopwords"]:
            self.stopwords_data["stopwords"].append(word)
            self.save_stopwords()
    
    def remove_stopword(self, word):
        if word in self.stopwords_data["stopwords"]:
            self.stopwords_data["stopwords"].remove(word)
            self.save_stopwords()

    def save_stopwords(self):
        stopwords_path = pkg_resources.resource_filename(__name__, 'stopwords.json')
        with open(stopwords_path, 'w') as stopwords_file:
            json.dump(self.stopwords_data, stopwords_file, indent=4)

    def show_all_stopwords(self):
        stopwords = self.stopwords_data.get("stopwords", [])
        return stopwords
        
    def remove_english(self, text: str) -> str:
        text = re.sub(r'[a-zA-Z]+', '', text)
        return self.remove_whitespace(text)

    def remove_numbers(self, text: str) -> str:
        text = re.sub(r'\d+', '', text)  
        text = re.sub(r'[۰-۹]+', '', text) 
        return self.remove_whitespace(text)
        
    def remove_numbers_english(self, text: str) -> str:
        english_numbers_pattern = r'\b[0-9]+\b'
        text = re.sub(english_numbers_pattern, '', text)
        return self.remove_whitespace(text)
        
    def remove_numbers_urdu(self, text: str) -> str: 
        urdu_numbers_pattern = r'[۰-۹]+'  
        text = re.sub(urdu_numbers_pattern, '', text)
        return self.remove_whitespace(text)

    def remove_special_characters(self, text: str) -> str:
        text = text.replace( '۔' , '-')
        text = text.replace( '؟' , '?')
        text = text.replace( '،' , ',')
        special_chars_pattern = r'[^0-9\u0600-\u06FF\u0750-\u077F\s]'
        text = re.sub(special_chars_pattern, '', text)
        return self.remove_whitespace(text)
        
    def remove_special_characters_exceptUrdu(self, text: str) -> str:
        special_chars_pattern = r'[^0-9\u0600-\u06FF\u0750-\u077F\s]'
        text = re.sub(special_chars_pattern, '', text)
        return self.remove_whitespace(text)
        
    def remove_urls(self,text: str) -> str:
        url_pattern = r'https?://\S+|www\.\S+'
        return re.sub(url_pattern, '', text)
        
    def just_urdu(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Text must be str type.")
        self.logger.info("Normalizing the text.")
        text = self.normalize_characters(text)
        text = self.normalize_combine_characters(text)
        text = self.remove_diacritics(text)
        text = self.replace_digits(text)
        text = self.preserve_special_characters(text)
        text = self.remove_english(text)
        text = self.remove_numbers(text)
        text = self.remove_special_characters(text)
        text = self.remove_whitespace(text)
        return text
        
    def pure_urdu(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Text must be str type.")
        self.logger.info("Normalizing the text.")
        text = text.replace( '-' , '۔')
        text = text.replace( '?' , '؟')
        text = text.replace( ',' , '،')
        text = self.normalize_characters(text)
        text = self.normalize_combine_characters(text)
        text = self.remove_diacritics(text)
        text = self.replace_digits(text)
        text = self.preserve_special_characters(text)
        text = self.remove_english(text)
        text = self.remove_special_characters_exceptUrdu(text)
        text = self.remove_whitespace(text)
        return text

        
    def urdu_tokenize(self, text: str) -> str:
        text = self.remove_whitespace(text)
        text = self.preserve_special_characters(text)
        pattern = r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+|\d+|[^\w\s]'
        tokens = re.findall(pattern, text)
        return tokens
        
    def lemmatize_sentence(self, sentence):
        words = sentence.split()
        lemmatized_words = [self.lemmatization_dict.get(word, word) for word in words]
        return ' '.join(lemmatized_words)
        
    def urdu_stemmer(self,sentence):
        rules = {
            'ة$': 'ه',    
            'وں$': 'ا',    
            'یں$': 'ا',    
            'ات$': 'ه',  
            'ویں$': '',    
            '^میں$': 'میں',
            '^ہمیں$': 'ہم',
            'فرائض' :  'فرض',
            'تا' : 'ت',
            'تا' : 'ت',
            'با':'ب',
            r'یاں\b': 'ی',
            '^کھڑکی$' : 'کھڑکی',
            r'ے\b': 'ہ',
            '^پڑھ.*$': 'پڑھ'
        }

        def stem_word(word):
            for pattern, sub in rules.items():
                regex = re.compile(pattern)
                word = regex.sub(sub, word)
            return word

        tokens = sentence.split()
        stemmed_tokens = [stem_word(token) for token in tokens]
        stemmed_sentence = ' '.join(stemmed_tokens)
        return stemmed_sentence
        
    def corrected_sentence_spelling(self, input_word, threshold):
        corrected_sentence = []
        for word in input_word.split():
            max_similarity = (word, 0)
            for vocab_word in self.all_words:
                edit_distance = Levenshtein.distance(word, vocab_word)
                max_length = max(len(word), len(vocab_word))
                similarity_percentage = ((max_length - edit_distance) / max_length) * 100
                if similarity_percentage > threshold and similarity_percentage > max_similarity[1]:
                    max_similarity = (vocab_word, similarity_percentage)
            corrected_sentence.append(max_similarity[0])
        return ' '.join(corrected_sentence)

    def most_similar_word(self, input_word, threshold):
        similarities = []
        for word in self.all_words:
            edit_distance = Levenshtein.distance(input_word, word)
            max_length = max(len(input_word), len(word))
            similarity_percentage = ((max_length - edit_distance) / max_length) * 100
            if similarity_percentage > threshold:
                similarities.append((word, similarity_percentage))
        similarities.sort(key=lambda x: x[1], reverse=True)
        if not similarities:
            return input_word
        else:
            return similarities[0][0]


    def get_similar_words_percentage(self, input_word, threshold):
        similarities = []
        for word in self.all_words:
            edit_distance = Levenshtein.distance(input_word, word)
            max_length = max(len(input_word), len(word))
            similarity_percentage = ((max_length - edit_distance) / max_length) * 100
            if similarity_percentage > threshold:
                similarities.append((word, similarity_percentage))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def get_similar_words(self, input_word, threshold):
        similarities = []
        for word in self.all_words:
            edit_distance = Levenshtein.distance(input_word, word)
            max_length = max(len(input_word), len(word))
            similarity_percentage = ((max_length - edit_distance) / max_length) * 100
            if similarity_percentage > threshold:
                similarities.append((word, similarity_percentage))
        similarities.sort(key=lambda x: x[1], reverse=True)
        similar_words = [word for word, _ in similarities]
        return similar_words

