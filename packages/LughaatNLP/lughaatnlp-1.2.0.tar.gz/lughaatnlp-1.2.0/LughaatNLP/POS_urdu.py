import logging
import re
import torch
import torch.nn as nn
import pickle
import pkg_resources
import warnings
warnings.filterwarnings('ignore')

class BiLSTMTagger(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, tagset_size, n_layers, dropout):
        super(BiLSTMTagger, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, 
                           num_layers=n_layers, 
                           bidirectional=True,
                           dropout=dropout if n_layers > 1 else 0,
                           batch_first=True)
        self.hidden2tag = nn.Linear(hidden_dim * 2, tagset_size)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        lstm_out, _ = self.lstm(embedded)
        lstm_out = self.dropout(lstm_out)
        return self.hidden2tag(lstm_out)

class POS_urdu:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.max_sequence_length = 281
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_path = pkg_resources.resource_filename(__name__, 'pos_model.pth')
        word2index_file = pkg_resources.resource_filename(__name__, 'word2index.pkl')
        tag2index_file = pkg_resources.resource_filename(__name__, 'tag2index.pkl')
        with open(word2index_file, 'rb') as f:
            self.word2index = pickle.load(f)
        with open(tag2index_file, 'rb') as f:
            self.tag2index = pickle.load(f)
        checkpoint = torch.load(model_path, map_location=self.device)
        config = checkpoint['model_config']
        self.model = BiLSTMTagger(
            vocab_size=config['vocab_size'],
            embedding_dim=config['embedding_dim'],
            hidden_dim=config['hidden_dim'],
            tagset_size=config['tagset_size'],
            n_layers=config['n_layers'],
            dropout=config['dropout']
        ).to(self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

    def remove_whitespace(self, text: str) -> str:
        return ' '.join(text.split())

    def preserve_special_characters(self, text: str) -> str:
        special_characters_pattern = r'(?<=[!@#$&*=_+,.؟۔-])|(?=[!@#$&*=_+,.؟۔-])'
        text = re.sub(special_characters_pattern, ' ', text)
        return self.remove_whitespace(text)

    def urdu_tokenize(self, text: str) -> str:
        text = self.remove_whitespace(text)
        text = self.preserve_special_characters(text)
        pattern = '[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+|\d+|[^\w\s]'
        tokens = re.findall(pattern, text)
        return tokens

    def pos_tags_urdu(self, sentence):
        sentence_tokens = self.urdu_tokenize(sentence)
        sentence_indices = [self.word2index.get(word, self.word2index['-OOV-']) for word in sentence_tokens]
        if len(sentence_indices) < self.max_sequence_length:
            padded_sequence = sentence_indices + [self.word2index['-PAD-']] * (self.max_sequence_length - len(sentence_indices))
        else:
            padded_sequence = sentence_indices[:self.max_sequence_length]
        tensor_input = torch.LongTensor([padded_sequence]).to(self.device)
        with torch.no_grad():
            output = self.model(tensor_input)
            predictions = torch.argmax(output, dim=-1)
        idx2tag = {idx: tag for tag, idx in self.tag2index.items()}
        predicted_tags = [idx2tag[idx.item()] for idx in predictions[0][:len(sentence_tokens)]]
        result = []
        for word, pos_tag in zip(sentence_tokens, predicted_tags):
            result.append({'Word': word, 'POS_Tag': pos_tag})
        
        return result