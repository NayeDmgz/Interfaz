#Alumno: Nayeli Itzel Dominguez Avila
#Grupo: A
import requests
import re
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

with open('urls.txt', 'r', encoding="utf-8") as urls:
    document = urls.read()
    document_list = document.split()
urls.close()

def write_txt(frequency_dict):
    output = open("raiz_ind_inv.txt","w", encoding="utf-8")
    output.write(str(frequency_dict))
    output.close()

def create_corpus(frequency_dict):
    corpus = []

    for url in frequency_dict:
        for item in frequency_dict[url]:
            corpus.append(item[0])
    
    corpus = list(set(corpus))
    
    return corpus

def inverse_index(word, frequency_dict):
    frequencies_list = []
    for url in frequency_dict:
        for item in frequency_dict[url]:
           if (word == item[0]):
                frequency_tuple = (url, item[1])
                frequencies_list.append(frequency_tuple)
                break
    
    return frequencies_list


def scraping_html(url):
    ps = PorterStemmer()
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'lxml')
    html = soup.text

    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleanr = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
                      "]+", re.UNICODE)
    clean_html = re.sub(cleanr, '', html)

    html_tokens = word_tokenize(clean_html)

    stop_words = set(stopwords.words('english'))
    filtered_words = []
    punc = '''!–—()--``==[]{};–:'"\,<>....//?@#$%^&*_~'''''
 
    for w in html_tokens:
        w = w.lower()
        if w not in stop_words:
            if w not in punc:
                if w != "''":
                    root_word = ps.stem(w)
                    filtered_words.append(root_word)

    unique_words = set(filtered_words)

    frecuency_list = []
    for words in unique_words:
        frecuency_tuple = (words, filtered_words.count(words))
        frecuency_list.append(frecuency_tuple)
    
    return frecuency_list

def main():
    frequency_dict={}
    for doc in document_list:
        frequency_dict.update({doc:scraping_html(doc)})

    inverted_dict={}
    corpus = create_corpus(frequency_dict)

    for word in corpus:
        inverted_dict.update({word:inverse_index(word, frequency_dict)})
    

    write_txt(inverted_dict)

if __name__ == "__main__":
    main()
