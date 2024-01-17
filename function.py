import numpy as np
import pandas as pd
import re
import torch
import requests
#from vncorenlp import VnCoreNLP
from underthesea import word_tokenize
from bs4 import BeautifulSoup as bs
from datetime import datetime


'''
(1)
Mở file chứa các từ stop word lưu vào 1 list
'''
#STOPWORDS = 'vietnamese-stopwordsv3.txt'
with open("./data/vietnamese-stopwordsv3.txt", "rb") as ins:
    '''
    ''' 
    stopwords = []
    for line in ins:
        dd = line.strip()#Xóa khoảng trắng ở đầu và cuối chuổi
        #dd = line.strip("\n")
        stopwords.append(dd)
    stopwords = set(stopwords)

# dict_sent = pd.read_csv('data/dict_sentiment_v2.csv')
#vncorenlp = VnCoreNLP("VnCoreNLP-master/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

def check_spam(text):
    '''
    phương thức kiểm tra text spam
    ???????????????????????????
    '''
    temp = text
    word = ''
    a = temp.split(" ")#Với mỗi white space tách thành từng word riêng lẻ
    for i in range(0, len(a)):
        if len(a[i])>8 and (a[i] != 'a' or a[i]!='o' or a[i]!='e' or a[i]!='u' or a[i]!='i'):
            a[i] = ' '
        word = word +' '+ str(a[i])
    return word

def check_space(text):
    '''
    check comment toàn là khoảng trắng
    '''
    if text == '' or text.isspace() == True:
        text = None
    return text

def filter_vt(train_sentences, dict_sent):
    """
    """
    for i in range(len(dict_sent)):
        for word in train_sentences.split():
            if (word == dict_sent.iloc[i, 0]):
                train_sentences = train_sentences.replace(dict_sent.iloc[i, 0], dict_sent.iloc[i, 1])
    return train_sentences


def filter_stop_words(train_sentences, stop_words):
    """
    """
    new_sent = [word for word in train_sentences.split() if word not in stop_words]
    train_sentences = ' '.join(new_sent)

    return train_sentences


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def negation_handling(text):
    negation = False
    delims = "?.,!:;"
    result = []
    words = text.split()
    for word in words:
        stripped = word.strip(delims).lower()
        negated = "không_" + stripped if negation else stripped
        if negation == True:
            negation = not negation
        result.append(negated)
        if any(neg in word for neg in ["không", "chưa", "chẳng", 'có chắc']):
            negation = not negation
    for word in result:
        if word in ['không', 'chẳng', 'chưa', 'có chắc']:
            result.remove(word)
    result = ' '.join(result)
    return result


def intensification_handling(text):
    """
    tạo intensification:
    ví dụ câu: Tôi rất thích đi học -> Tôi rất_thích đi học
    """
    negation = False
    delims = "?.,!:;"
    result = []
    words = text.split()
    for word in words:
        stripped = word.strip(delims).lower()
        negated = "rất_" + stripped if negation else stripped
        if negation == True:
            negation = not negation
        result.append(negated)
        if any(neg in word for neg in ["rất", "khá", "hơi"]):
            negation = not negation
    for word in result:
        if word in ['rất', 'hơi', 'khá']:
            result.remove(word)
    result = ' '.join(result)
    return result


def preprocess(text, tokenized = True, lowercased = True):
    # text = ViTokenizer.tokenize(text)
    # text = ' '.join(vncorenlp.tokenize(text)[0])
    #text = filter_vt(text, dict_sent)
    text = filter_stop_words(text, stopwords)
    text = deEmojify(text)
    text = text.lower() if lowercased else text
    text = negation_handling(text)
    text = intensification_handling(text)
    """
    if tokenized:
        pre_text = ""
        sentences = vncorenlp.tokenize(text)
        for sentence in sentences:
            pre_text += " ".join(sentence)
        text = pre_text
    """
    text = word_tokenize(text, format='text')
    return text

def pre_process_features(X, y, tokenized=True, lowercased=True):
    X = [preprocess(str(p), tokenized=tokenized, lowercased=lowercased) for p in list(X)]
    for idx, ele in enumerate(X):
        if not ele:
            np.delete(X, idx)
            np.delete(y, idx)
    return X, y


def clean_tags(soup):
    '''
    Xóa các <span> tag trong html
    '''
    for tag in soup.find_all(["span"]):
        tag.decompose()#Delete tag

        
def delete_block(comment):
    '''
    Xóa tất cả các <blockquote> tag (dùng để trích dẫn comment)
    '''
    if comment.find('blockquote') != None:
        com_full = comment.get_text(strip = True)
        com_full = com_full.replace('\t','')
        com_full = com_full.replace('\n','')
        a = len(com_full)
        com_block=comment.find('blockquote').get_text()
        com_block=com_block.replace('\t','')
        com_block=com_block.replace('\n','')
        b = len(com_block)
        com = com_full[(b-1):]
    else:
        com = comment.get_text(strip=True)
        com = com.replace('\t','')
        com = com.replace('\n','')
    return com


def get_comment(url):
    '''
    Lấy các bình luận từ url (thông qua class của html)
    '''
    r = requests.get(url).text
    soup = bs(r,'html.parser')#chuyển đổi định dạng sang soup
    get_com = soup.find_all(class_='bbWrapper')#class bbWrapper chứa comment
    clean_tags(soup)#Bỏ tag không cần sử dụng
    comment_info = []
    for i in get_com:
        comment_info.append(delete_block(i))
    return comment_info


def get_time(url):
    '''
    lấy thời gian bình luận thông qua class
    '''
    r = requests.get(url).text
    soup = bs(r,'html.parser')
    get_time = soup.find_all(class_='message-attribution-main')
    time_info = []
    for i in get_time:
        i = i.get_text()
        i = i.replace('\n','')
        time_info.append(i)
    return time_info


def get_list(list_full):
    '''
    Tách nhở từng chữ đơn
    '''
    list_com=[]
    for i in list_full:#full thread
        for a in i:#full page
            com = a
            for co in com:#full comment
                list_com.append(co)
    return list_com#full single word 


def get_url_com(url):
    '''
    lấy url của thread theo từng page 
    và lấy tất cả comment từ mỗi page của thread
    '''
    # list_=[]
    nums = (np.arange(1, 20))#create numpy array 1->19 elements
    Pages = []
    comment_full=[]
    
    for num in nums:
        Pages.append('page-' + str(num))

    for i in Pages:
        if i == 'page-1':
            rela_url = url
        else:
            try:
                rela_url = url + i
            except Exception as e:
                print(None)
        #print(rela_url)
        comment_full.append(get_comment(rela_url))
    return comment_full


def get_url_time(url):
    '''
    lấy url của thread theo từng page 
    và lấy tất cả thời gian comment từ mỗi page của thread
    '''
    # list_=[]
    nums = (np.arange(1, 20))
    Pages = []
    for num in nums:
        Pages.append('page-' + str(num))

    time_full=[]
    for i in Pages:
        if i == 'page-1':
            rela_url=url
        else:
            try:
                rela_url = url + i
            except Exception as e:
                print(None)
        #print(rela_url)
        time_full.append(get_time(rela_url))
    return time_full


def convert(data):
    '''
    Chuyển đổi dữ liệu craw được
    '''
    for index, i in enumerate(data.comment):
        if type(i) == list:
            a =' '.join(i)
            data.comment[index]= a
    for index, i in enumerate(data.time):
        i = i.replace(',','')
        date = datetime.strptime(i, '%b %d %Y')
        data.time[index]=date
        
        
def clean_comment(com):
    '''
    remove \w bằng " "
    '''
    com = re.sub("\W"," ",com)
    REGEX2 = re.compile(r"[\"']")
    com = REGEX2.sub('',com)
    return com


class BuildDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

