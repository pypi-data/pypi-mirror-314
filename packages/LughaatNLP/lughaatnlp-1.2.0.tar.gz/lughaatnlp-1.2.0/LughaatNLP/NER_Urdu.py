from typing import List
import logging
import re
import pickle
import pkg_resources
import torch
import torch.nn as nn
import warnings
warnings.filterwarnings('ignore')


class UrduBiLSTMNER(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_tags, num_layers=2, dropout=0.5):
        super(UrduBiLSTMNER, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim, 
            hidden_dim, 
            num_layers=num_layers, 
            bidirectional=True, 
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, num_tags)
        
    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        lstm_out, _ = self.lstm(embedded)
        lstm_out = self.dropout(lstm_out)
        tag_scores = self.fc(lstm_out)
        return torch.log_softmax(tag_scores, dim=2)


class NER_Urdu:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        word2index_path = pkg_resources.resource_filename(__name__, 'ner_word2index.pkl')
        with open(word2index_path, 'rb') as f:
            self.word2index = pickle.load(f)

        tag2index_path = pkg_resources.resource_filename(__name__, 'ner_tag2index.pkl')
        with open(tag2index_path, 'rb') as f:
            self.tag2index = pickle.load(f)

        max_length_path = pkg_resources.resource_filename(__name__, 'max_length.pkl')
        with open(max_length_path, 'rb') as f:
            self.max_length = pickle.load(f)

        self.tag2label = {v: k for k, v in self.tag2index.items()}

        model_path = pkg_resources.resource_filename(__name__, 'urdu_ner_model.pth')
        self.model = UrduBiLSTMNER(
            vocab_size=len(self.word2index),
            embedding_dim=300,
            hidden_dim=256,
            num_tags=len(self.tag2index)
        )
        checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

    def preprocess_sentence(self, sentence):
        sentence_indices = [self.word2index.get(word, self.word2index['-OOV-']) for word in sentence]
        if len(sentence_indices) < self.max_length:
            sentence_indices.extend([self.word2index['-PAD-']] * (self.max_length - len(sentence_indices)))
        else:
            sentence_indices = sentence_indices[:self.max_length]
        return torch.tensor(sentence_indices).unsqueeze(0)

    def remove_whitespace(self, text: str) -> str:
        return ' '.join(text.split())

    def preserve_special_characters(self, text: str) -> str:  
        special_characterspattern = r'(?<=[!@#$&*=+,.؟۔-])|(?=[!@#$&*=_+,.؟۔-])'
        text = re.sub(special_characterspattern, ' ', text)
        return self.remove_whitespace(text)

    def urdu_tokenize(self, text: str) -> List[str]:
        text = self.remove_whitespace(text)
        text = self.preserve_special_characters(text) 
        pattern = r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+|\\d+|[^\w\s]'
        tokens = re.findall(pattern, text)
        return tokens

    def ner_tags_urdu(self, sentence):
        tokenized_sentence = self.urdu_tokenize(sentence)
        input_tensor = self.preprocess_sentence(tokenized_sentence)
        with torch.no_grad():
            outputs = self.model(input_tensor)
            predictions = outputs.argmax(dim=2).squeeze(0)
        result = {word: self.tag2label[predictions[i].item()] 
                 for i, word in enumerate(tokenized_sentence) 
                 if i < len(predictions)}
        return result