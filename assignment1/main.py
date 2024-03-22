import nltk
from commonregex import CommonRegex
import pyap
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize
import re
import spacy

try:
    nlp = spacy.load("en_core_web_lg")
except IOError:
    print("SpaCy model not found. Downloading...")
    spacy.cli.download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

from nltk.corpus import wordnet

nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)

def censor_names(text):
    words = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tagged_words)
    names_list = [entity[0][0] for entity in list(tree.subtrees()) if entity.label() in ['PERSON','GPE']]
    for name in names_list:
        text = text.replace(name, '\u2588'* len(name))
    return text, names_list

def censor_dates(text):
    doc = nlp(text)
    dates_entities_list = []
    for date_entities in [entity.text.split('\n') for entity in doc.ents if entity.label_ == "DATE"]:
        for date in date_entities:
            dates_entities_list.append(date)
    pattern = r'(\d{1,4}/\d{1,2}/\d{1,4})'
    dates_regex_list = re.findall(pattern, text)
    dates_list = set(dates_entities_list + dates_regex_list)
    excluded_words = ["day", "today", "tomorrow", "yesterday", "century", "week", "weeks", "year", "years", "month", "months"]
    dates_list = [date for date in dates_list if date.lower() not in excluded_words]
    for item in dates_list:
        text = text.replace(item, '\u2588'* len(item))
    return text, dates_list

def censor_phones(text):
    parser = CommonRegex(text)
    phones_list = parser.phones
    for phone in phones_list:
        text = text.replace(phone, '\u2588'* len(phone))
    return text, phones_list

def censor_genders(text):
    genders_list = []
    gender_keywords = ['mr', 'ms', 'mrs', 'miss', 'mister', 'missus', 'maiden', 'boy', 'girl', 'man', 'woman', 'lady', 'ladies', 'men',
        'daughter', 'male', 'female', 'son', 'manly', 'manful', 'manlike', 'guy', 'gal', 'women', 
        'dad', 'mom', 'mommy', 'mummy', 'daddy', 'wife', 'husband', 'ladylike', 'womanly', 'mother', 'father',
        'sister', 'brother', 'aunt', 'uncle', 'mama', 'queen', 'king', 'wives', 'prince', 'nephew', 'neice',
        'waiter', 'widower', 'heroine', 'hero', 'aunt', 'bride', 'groom', 'goddess', 'granddaughter', 'grandson', 'grandmother',
        'grandfather', 'grandma', 'grandpa', 'gentleman', 'gentlemen', 'gay', 'transgender',
        'cisgender', 'transsexual', 'he', 'him', 'she', 'her', 'herself', 'himself', 'his']
    
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    for token in tokens:
        if lemmatizer.lemmatize(token.lower()).replace('.', '') in gender_keywords:
            genders_list.append(token)
            text = re.sub(r'\b{0}(\'s)?\b'.format(token.replace('.', '')), '\u2588'* len(token), text)

    return text, genders_list

def censor_addresses(text):
    addresses_list = []
    addresses = pyap.parse(text, country='US')
    for address in addresses:
        start_index = text.index(str(address).split(',')[0].strip())
        end_index = text.index(str(address).split(',')[-1].strip()) + len(str(address).split(',')[-1].strip())
        addresses_list.append(text[start_index:end_index])
        text = text[:start_index] + '\u2588'* len(str(address)) + text[end_index:]
    return text, addresses_list

def censor_concepts(text, concepts):
    synonyms = []
    censored_concepts_list = []
    for concept in concepts:
        for syn in wordnet.synsets(concept.lower()):
            synonyms += [lemma.name() for lemma in syn.lemmas()]
    
    lemmatizer = WordNetLemmatizer()
    sentences = sent_tokenize(text)
    for sentence in sentences:    
        tokens = word_tokenize(sentence)
        lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
        
        for lemma_token in lemmatized_tokens:
            if lemma_token.lower() in synonyms:
                censored_concepts_list.append(sentence)
                text = text.replace(sentence, '\u2588'* len(sentence))
                continue    
    
    return text, censored_concepts_list
