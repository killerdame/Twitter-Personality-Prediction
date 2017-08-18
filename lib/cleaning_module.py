from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_text(text):
    new_text = text.str.replace('\(', '').str.replace('\)', '').str.replace('@', '').str.replace('https://.?', '')
    new_text = re.sub("['http\S+''\''%'':''#'')''('';''\n''/''.''!''*''-''+''$'',''?''~''&''@''``']", "", new_text)
    corpus = set(stopwords.new_text('english'))
    word_tokens = word_tokenize(corpus.lower())
    filtered_text = [w for w in word_tokens if not w in stop_words]
    filtered_text = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_text.append(w)
    return text
 
    