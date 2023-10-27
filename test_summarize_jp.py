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

def generate_summary(doc, prompt, summaries):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": doc.page_content}
        ]
    )
    usage = response["usage"]["total_tokens"]
    summary_piece = response["choices"][0]["message"]["content"]
    summaries.append(summary_piece)
    
    print(f"Document {i + 1}: {summary_piece}...\n\n")
    
    return usage

if __name__ == '__main__':
    start_time = time.time()
    load_dotenv()
    openai_api_key = os.environ['OPENAI_API_KEY']

    with open(select_file(), 'r') as f:
        long_text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=0,)
    texts = text_splitter.split_text(long_text)
    docs = [Document(page_content=t) for t in texts]

    prompt1 = '''
    Take a deep breath and work on this problem step-by-step.

    #Role.
    You are able to see through the overall structure and are a genius at summarizing sentences to order.
    #Conditions
    The following sentences are text data transcribed from audio that has been divided into multiple chunks.
    The first chunk of text is the first sentence.
    Please make sure to output the data in Japanese.
    Please output only the summary content and do not speak any other language.
    #Order
    Please summarize the following sentences in Japanese without any missing content.

    #First sentence:
    '''
    prompt2 = '''
    深呼吸をして、この問題に一歩一歩取り組んでください。

    #役割
    あなたは全体の構造を見抜くことができ、文章を順序立ててまとめる天才です。
    #条件
    以下の文章は、音声から文字起こしをし、さらに複数のチャンクに分割されたテキストデータです。
    (一つ前の要約結果）の内容を理解し、それに続く文章のみを要約してください。
    前の要約の内容と、それに続く文章の内容の重複は必ずカットしてください。
    必ず日本語で出力してください。
    要約内容のみを出力し、それ以外の言語はご遠慮ください。
    #一つ前の要約結果:
    {prev_summary}

    #命令
    以下の文章を情報欠落のないように日本語で要約してください。

    #続きの文章：
    '''

    summaries = []
    usages = 0
    
    for i, doc in enumerate(docs[:5]):
        if i == 0:
            prompt_to_use = prompt1
        else:
            prompt_to_use = prompt2.format(prev_summary=summaries[-1])
        
        usage = generate_summary(doc, prompt_to_use, summaries)
        usages += usage

    # print(summaries)
    print(usages)
    print(f"{time.time() - start_time}")
