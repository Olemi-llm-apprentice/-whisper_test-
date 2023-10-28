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
    
    #usage = response["usage"]["total_tokens"]
    input_token = response["usage"]["prompt_tokens"]
    output_token = response["usage"]["completion_tokens"]


    summary_piece = response["choices"][0]["message"]["content"]
    summaries.append(summary_piece)
    
    print(f"Document {i + 1}: {summary_piece}...\n\n")
    
    return input_token,output_token

def calculate_cost(tokens, rate_per_1k):
    return (tokens / 1000) * rate_per_1k

if __name__ == '__main__':
    start_time = time.time()
    load_dotenv()
    openai_api_key = os.environ['OPENAI_API_KEY']
    
    selected_file_path = select_file()
    input_filename = os.path.basename(selected_file_path)
    output_filename = os.path.splitext(input_filename)[0] + "_summaries.txt"

    with open(selected_file_path, 'r') as f:
        long_text = f.read()
        
    chunk_size=2000
    chunk_overlap=int(chunk_size * 0.2)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,)
    texts = text_splitter.split_text(long_text)
    docs = [Document(page_content=t) for t in texts]

    prompt1 = '''
    Take a deep breath and work on this problem step-by-step.

    #Role.
    You are able to see through the overall structure and are a genius at summarizing sentences to order.
    #Conditions
    The following sentences are text data transcribed from audio that has been divided into multiple chunks.
    Please make sure to output the data in Japanese.
    Please output only the summary content and no other remarks.
    Users only send long sentences, so make sure to output a summary statement in response to them.
    
    #Order
    Please summarize the following sentences in Japanese without any missing content.

    #First sentence:
    '''


    summaries = []
    #usages = 0
    input_token = 0
    output_token = 0
    
    for i, doc in enumerate(docs):
        prompt_to_use = prompt1
       
        input_tokens, output_tokens = generate_summary(doc, prompt_to_use, summaries)
        input_token += input_tokens
        output_token += output_tokens
        
    with open(output_filename, 'w') as f:
        for summary in summaries:
            f.write(f"{summary}\n")
    
    input_rate_per_1k = 0.0015
    output_rate_per_1k = 0.002
    

    input_cost = calculate_cost(input_token, input_rate_per_1k)
    output_cost = calculate_cost(output_token, output_rate_per_1k)
    total_cost_usd = input_cost + output_cost
    
    # 仮の為替レート（1ドル = 150円と仮定）
    exchange_rate = 150.0
    total_cost_jpy = total_cost_usd * exchange_rate
     
    
    # print(f"Input tokens: {input_token}")
    # print(f"Output tokens: {output_token}")
    # print(f"Input cost: ${input_cost:.4f}")
    # print(f"Output cost: ${output_cost:.4f}")
    print(f"この要約に${total_cost_usd:.4f} ({total_cost_jpy:.2f}円)かかりました。")
    
    print(f"処理時間：{time.time() - start_time:.2f}sec")
