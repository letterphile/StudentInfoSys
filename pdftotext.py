import PyPDF2 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
def ptot(file):
    filename =  file
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    if text != "":
        text = text
    else:
        text = textract.process(file, method='tesseract', language='eng')

    #pattern = re.compile(r'(\w{3}\d{2}\w{2}\d{3})(\w+\(\w+[+]?\))((,\s\w+\(\w+[+]?\))*)')
    #matches = pattern.finditer(text)
    #return matches
    return text

