from setuptools import setup, find_packages
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='LughaatNLP',
    version='1.2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'LughaatNLP': ['Urdu_Lemma.json', 'stopwords.json', 'tokenizer.json' , 'pos_model.pth' , 'vocabularies.pkl' , 'tag2index.pkl' ,'ner_model.pt' , 'word2index.pkl']},
    entry_points={
        'console_scripts': [
            'lughaatnlp = LughaatNLP.LughaatNLP:main'
        ]
    },
    install_requires=[
        'python-Levenshtein',
        'numpy',
        'scikit-learn',
        'scipy',
        'gtts',
        'SpeechRecognition',
        'pydub',
        'torch==2.5.1'
    ],
    project_urls = {
    'Source': 'https://github.com/MuhammadNoman76/LughaatNLP',
    'Issue Tracker': 'https://github.com/MuhammadNoman76/LughaatNLP/issues',
    'LinkedIn': 'https://www.linkedin.com/in/muhammad-noman76',
    'YouTube Channel': 'https://www.youtube.com/playlist?list=PL4tcmUwDtJEIHZhAZ3XP9U6ZJzaS4RFbd',
    'Google Colab': 'https://colab.research.google.com/drive/1lLaUBiFq61-B7GyQ0wdNg9FyLCraAcDU?usp=sharing',
    'Geeksforgeeks': 'https://www.geeksforgeeks.org/lughaatnlp-a-powerful-urdu-language-preprocessing-library/',
    'LughaatNLP Blog': 'https://lughaatnlp.blogspot.com/2024/04/mastering-urdu-text-processing.html',
    'Medium': 'https://medium.com/@muhammadnomanshafiq76/introducing-lughaatnlp-a-powerful-urdu-language-preprocessing-library-488af74d3dde'
    },
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Text Processing :: Linguistic',
    'Natural Language :: Urdu',
    ],
    author='Muhammad Noman',
    author_email='muhammadnomanshafiq76@gmail.com',
    description='A Python package for natural language processing tasks for the Urdu language, including normalization, part-of-speech (POS) tagging, named entity recognition (NER), stemming, lemmatization, tokenization, and stopword removal , text-to-speech , speech-to-text, summarization.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    license_files=['LICENSE'],
    keywords='urdu nlp natural language processing text processing tokenization stemming lemmatization stopwords morphological-analysis nlp urdu LughaatNLP urdunlp UrduNLP urduhack stanza natural-language-processing text-processing language-processing preprocessing stemming lemmatization tokenization stopwords',
    url='https://github.com/MuhammadNoman76/LughaatNLP'
)