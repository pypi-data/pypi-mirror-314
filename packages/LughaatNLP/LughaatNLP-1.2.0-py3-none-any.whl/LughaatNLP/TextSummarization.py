from collections import defaultdict
from itertools import combinations
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from math import log
from LughaatNLP import LughaatNLP  
import re
import pkg_resources
import logging
import warnings
warnings.filterwarnings('ignore')

class TextSummarization:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.urdu_text_processing = LughaatNLP()
        self.nodes = set()
        self.edges = defaultdict(int)

    def add_edge(self, node1, node2, weight=1):
        self.nodes.update([node1, node2])
        self.edges[(node1, node2)] += weight
        if node1 != node2:
            self.edges[(node2, node1)] += weight

    def build_adjacency_matrix(self):
        nodes = list(self.nodes)
        node_to_index = {node: index for index, node in enumerate(nodes)}
        size = len(nodes)
        row, col, data = [], [], []
        for (node1, node2), weight in self.edges.items():
            index1, index2 = node_to_index[node1], node_to_index[node2]
            row.append(index1)
            col.append(index2)
            data.append(weight)
        return csr_matrix((data, (row, col)), shape=(size, size))

    def bm25_weighted(self, sentences, text):
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(sentences)
        transformer = TfidfTransformer()
        tfidf_matrix = transformer.fit_transform(X)

        N = len(sentences)
        idf = defaultdict(int)
        for word in vectorizer.vocabulary_:
            df = sum(1 for sentence in sentences if word in sentence)
            idf[word] = log((N - df + 0.5) / (df + 0.5) + 1)

        scores = defaultdict(int)
        for i, sentence in enumerate(sentences):
            for word in sentence.split():
                if word in vectorizer.vocabulary_:
                    scores[i] += idf[word] * tfidf_matrix[i, vectorizer.vocabulary_[word]]
        return scores

    def clean_text(self, text):
        tokens = self.urdu_text_processing.urdu_tokenize(text)
        return tokens

    def get_sentences(self, text):
        # Define the custom split pattern using regular expressions
        sentences = re.split(r'[۔،.؟\'٬]', text)
        # Remove empty strings resulting from consecutive delimiters
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences

    def summarize(self, text, ratio):
        sentences = self.get_sentences(text)
        for sentence in sentences:
            sentence_words = self.clean_text(sentence)
            for word1, word2 in combinations(sentence_words, 2):
                self.add_edge(word1, word2)

        sentences_without_stopwords = [self.urdu_text_processing.remove_stopwords(sentence) for sentence in sentences]
        scores = self.bm25_weighted(sentences_without_stopwords, text)

        sentence_scores = [(sentence, scores[i]) for i, sentence in enumerate(sentences)]
        sentence_scores.sort(key=lambda x: x[1], reverse=True)

        num_sentences = max(1, int(len(sentences) * ratio))
        top_sentences = [sentence for sentence, score in sentence_scores[:num_sentences]]
        return '۔ '.join(top_sentences) + '۔'

    def add_sentence_end(self, text):
        end_words = [
            'تھا', 'تھی', 'تھے', 'تھیں', 'ہوا', 'ہوئی', 'ہوئے', 'ہوئیں', 'ہو', 'ہیں', 'ہے', 'ہوں', 'ہوگا', 'ہوگی', 'ہوگے',
            'ہوگی', 'ہوں گے', 'ہوں گی', 'ہوں گا', 'ہوں گی', 'رہا', 'رہی', 'رہے', 'رہیں', 'ہوگئے', 'ہوگئی', 'ہوگئیں', 'ہوگیا',
            'ہونگے', 'ہونگی', 'ہونگا', 'ہونگیں', 'ہوں', 'جائے', 'جائیں', 'جائیں گے', 'جائیں گی', 'گئے', 'گئی', 'گئیں', 'گیا',
            'چکا', 'چکی', 'چکے', 'چکیں', 'لیا', 'لی', 'لیے', 'لیں', 'دیا', 'دی', 'دیے', 'دیں', 'کیا', 'کی', 'کیے', 'کیں', 'ہے',
            'ہیں', 'تھا', 'تھی', 'تھے', 'تھیں', 'گیا', 'گئی', 'گئے', 'گئیں', 'لیا', 'لی', 'لیے', 'لیں', 'دیا', 'دی', 'دیے', 'دیں',
            'کیا', 'کی', 'کیے', 'کیں'
        ]
        sentences = []
        current_sentence = ""

        for word in text.split():
            current_sentence += word + " "
            if any(word.endswith(end_word) for end_word in end_words) or word.endswith('۔'):
                if len(current_sentence.split()) > 3:
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
        if current_sentence:
            sentences.append(current_sentence.strip())

        corrected_sentences = [sentence + '۔' if not sentence.endswith('۔') and len(sentence.split()) > 3 else sentence for sentence in sentences]
        corrected_text = ' '.join(corrected_sentences)
        return corrected_text.strip()
    def summarize_unstructured_text(self, text, ratio):
        corrected_text = self.add_sentence_end(text)
        summarized_text = self.summarize(corrected_text, ratio)
        
        return summarized_text