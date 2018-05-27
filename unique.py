import re


def getCountOfUniqueWords(text):
    ''' Returns count of unique words in message
        support: emails; 
                 words with: \'; 
                 words splitted by: "_";
                 words with nums inside;
        not support: words splitted by: "-";
                     words splitted by special symbols.
    '''
    text = text.lower().replace('_', '')
    text = set(re.findall(r"[\w.-]+@\w+\.\w+|\w+\'\w+|\w+|", text))
    text.remove('')
    return len(text)
