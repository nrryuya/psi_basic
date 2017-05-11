from django.shortcuts import render
from readability.readability import Document
import re
from bs4 import BeautifulSoup
import requests


def get_content(url):
    try:
        response = requests.get(url)
        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), 'lxml')
        content = soup.text
        pattern = r'　+$|\s+$'
        repatter = re.compile(pattern)
        print("try:" + url)
        if not (content == "" or repatter.match(content)):
            print("readability worked")
            print("content: " + content)
            return content
        else:
            print("not worked like: " + content)
            content = get_body(response)
            print("content: " + content)
            return content
    except:
        return "error"
