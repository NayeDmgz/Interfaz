#Alumno: Nayeli Itzel Dominguez Avila
#Grupo: A

import re
import ast
import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from bs4 import BeautifulSoup 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

with open('raiz_ind_inv.txt', 'r', encoding="utf-8") as f:
    data = f.read()
    inverted_dict = ast.literal_eval(data)

def get_urls():
    urls = []

    for w in inverted_dict:
        for item in inverted_dict[w]:
            urls.append(item[0])
    
    urls = list(set(urls))
    return urls

def rank(k):
    for w in inverted_dict:
        if k == w:
            return inverted_dict[w] 

def get_titles(url):
    soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
    return soup.title.text

def normalize_text(text):
    ps = PorterStemmer()

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
    clean_text = re.sub(cleanr, '', text)
    

    tokens = word_tokenize(clean_text)

    stop_words = set(stopwords.words('english'))
    filtered_words = []
    punc = '''!–—()--``==[]{};–:'"\,<>....//?@#$%^&*_~'''''
 
    for w in tokens:
        w = w.lower()
        if w not in stop_words:
            if w not in punc:
                if w != "''":
                    root_word = ps.stem(w)
                    filtered_words.append(root_word)
    
    return filtered_words
       

def search(keywords):
    keywords_roots = normalize_text(keywords)
    matched_list = []
    frequency_list = []

    document_list = get_urls()

    for k in keywords_roots:
        matched_list.append(rank(k))

    for doc in document_list:    
        counter = 0
        for url in matched_list:
            for item in url:
                if item[0] == doc:
                    counter = counter + item[1]
                    break
        frequency_tuple = (doc, counter)
        frequency_list.append(frequency_tuple)     

    print(frequency_list)
    ranked_list = sorted(frequency_list, key=lambda tup: tup[1], reverse=True)
    print (ranked_list)
    return ranked_list

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.title = 'Buscador'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        
        # Create a button in the window
        self.button = QPushButton('Buscar', self)
        self.button.move(20,80)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        global keywords
        keywords = self.textbox.text()
        if self.w == None:
            self.w = ranking()
        self.w.show()
        #self.textbox.setText("")

class ranking(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.setStyleSheet('font-size: 18px')
        self.initUI()

    def initUI(self):
        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()
    
    def createTable(self):
       # Create table
        ranked_list = search(keywords)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(len(get_urls()))
        i = 0
        for item in ranked_list:
            title = get_titles(item[0])
            self.tableWidget.setItem(i,0, QTableWidgetItem(title))
            self.tableWidget.setItem(i,1, QTableWidgetItem(item[0]))
            self.tableWidget.setItem(i,2, QTableWidgetItem(str(item[1])))
            i = i + 1

        self.tableWidget.move(0,0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())