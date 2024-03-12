import nltk
from commonregex import CommonRegex
import pyap
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize
import re
import spacy
# nlp = spacy.load("en_core_web_lg")
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

def censor_names(data):
    words = nltk.word_tokenize(data)
    tag = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tag)
    names_list = [ent[0][0] for ent in list(tree.subtrees()) if ent.label() in ['PERSON','GPE']]
    for item in names_list:
        data = data.replace(item, '\u2588'* len(item))
    return data, names_list


def censor_dates(data):
    data1 = nlp(data)
    dates_ent_list = []
    for i in [ent.text.split('\n') for ent in data1.ents if ent.label_ == "DATE"]:
        for j in i:
            dates_ent_list.append(j)
    pattern = r'(\d{1,4}/\d{1,2}/\d{1,4})'
    dates_re_list = re.findall(pattern,data)
    dates_list = set(dates_ent_list + dates_re_list)
    list_to_excluded = ["day", "Day","today","Today","tomorrow","Tomorrow","yesterday","Yesterday","century","Century","week","Week","weeks","Weeks","week's","Week's","year", "Year","year's","Year's","month","Month","month's","Month's","months","Months"]
    for i in list_to_excluded:
        if i in dates_list:
            dates_list.remove(i)
    for items in dates_list:
        data = data.replace(items,'\u2588'* len(items))
    return data,dates_list

    
def censor_phones(data):
    data1 = CommonRegex(data)
    phones_list = data1.phones
    for item in phones_list:
        data = data.replace(item,'\u2588'* len(item))
    return data, phones_list

def censor_genders(data):
    genders_list = []
    list_gender = ['mr', 'ms', 'mrs','miss','mister','missus','maiden', 'boy', 'girl','man', 'woman','lady','ladies','men',
        'daughter', 'male', 'female', 'son','manly', 'manful', 'manlike', 'guy','gal','women', 
        'dad', 'mom','mommy','mummy', 'daddy', 'wife', 'husband', 'ladylike','womanly', 'mother','father',
        'sister', 'brother', 'aunt','uncle', 'mama', 'queen', 'king', 'wives','prince','nephew','neice',
        'waiter','widower','heroine', 'hero','aunt','bride','groom','goddess','granddaughter','grandson','grandmother',
        'grandfather','grandma','grandpa','gentleman','gentlemen','gay','transgender',
        'cisgender','transsexual','he','him','she','her','herself','himself','his']
    
    tokens = word_tokenize(data)
    lemmaterizer = WordNetLemmatizer()
    for tok in tokens:
        if lemmaterizer.lemmatize(tok.lower()).replace('.', '') in list_gender:
            genders_list = genders_list + [tok]
            data = re.sub(r'\b{0}(\'s)?\b'.format(tok.replace('.', '')), '\u2588'* len(tok), data)

    return data, genders_list

def censor_address(data):
    address_list = []
    addresses = pyap.parse(data,country = 'US')
    for address in addresses:
        start_index = data.index(str(address).split(',')[0].strip())
        end_index = data.index(str(address).split(',')[-1].strip()) + len(str(address).split(',')[-1].strip())
        address_list.append(data[start_index:end_index])
        data = data[:start_index] + '\u2588'* len(str(address)) + data[end_index:]
    return data, address_list

def censor_concept(data,concepts):
    synonyms = []
    concept_censored_list = []
    for concept in concepts:
        for syn in wordnet.synsets(concept.lower()):
            synonyms += [l.name() for l in syn.lemmas()]
    l = WordNetLemmatizer()
    sentences = sent_tokenize(data)
    for s in sentences:    
        tokens = word_tokenize(s)
        list2 = []
        for words1 in tokens:
            list2.append(words1.lower())
        tok_lemmas = [l.lemmatize(token) for token in list2]
        
        for tok_lemma in tok_lemmas:
            if tok_lemma.lower() in synonyms:
                concept_censored_list = concept_censored_list + [s]
                data = data.replace(s, '\u2588'* len(s))
                continue    
    
    return data, concept_censored_list 