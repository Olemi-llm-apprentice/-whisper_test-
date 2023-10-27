import os
import time
import openai
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

if __name__ == '__main__':
    start_time = time.time()
    load_dotenv()
    openai_api_key = os.environ['OPENAI_API_KEY']

    with open(select_file(), 'r') as f:
        long_text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=0,)
    texts = text_splitter.split_text(long_text)
    docs = [Document(page_content=t) for t in texts]
    
    # docs リストの上から5つを見やすく表示
    for i, doc in enumerate(docs[:5]):
        print(f"Document {i + 1}: {doc.page_content}\n\n")  # 最初の50文字だけ表示