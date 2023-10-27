import os
import time
import openai
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

start_time = time.time()

load_dotenv()
openai_api_key = os.environ['OPENAI_API_KEY']

# ファイル選択ダイアログ
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
with open(file_path, 'r') as f:
    long_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500)
texts = text_splitter.split_text(long_text)
docs = [Document(page_content=t) for t in texts]

# docs リストの上から5つを見やすく表示
# for i, doc in enumerate(docs[:5]):
#     print(f"Document {i + 1}: {doc.page_content[:50]}...")  # 最初の50文字だけ表示
 
prompt1='''
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

prompt2=f'''
Take a deep breath and work on this problem step-by-step.

#Role.
You are able to see through the overall structure and are a genius at summarizing sentences to order.
#Conditions
The following sentences are text data transcribed from audio that has been divided into multiple chunks.
Please understand the content of (one previous summary result) and summarize only the sentences that follow.
Please be sure to cut out any overlap between the content of the previous summary and the content of the following sentences.
The final output should be based on the output of all chunks of the summary results as they will be combined.
Please make sure to output the data in Japanese.
Please output only the summary content and do not speak any other language.
#One previous summary result:
{summaries[-1]}

#Order
Please summarize the following sentences in Japanese without any missing content.

#Continued sentences:
'''

summaries = []
usages = 0
    
for i, doc in enumerate(docs[:5]):
    if i == 0:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": prompt1},
                {"role": "user", "content": doc.page_content}        
            ]
        )
        usage = response["usage"]["total_tokens"]
        print(usage)
        usages += usage
        
        summary_piece = response["choices"][0]["message"]["content"]
        print(summary_piece)
        summaries.append(summary_piece)
        
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": prompt2},
                {"role": "user", "content": doc.page_content}          
            ]
        )
        print(summaries[-1])
        
        usage = response["usage"]["total_tokens"]
        print(usage)
        usages += usage
        
        summary_piece = response["choices"][0]["message"]["content"]
        print(summary_piece)
        summaries.append(summary_piece)
        

        
print(summaries)
print(usages)

print(f"{time.time() - start_time}")
