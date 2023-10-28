import os
import time
import openai
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

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
        
    prompt='''
    Take a deep breath and work on this problem step-by-step.

    #Role.
    You are able to see through the overall structure and are a genius at summarizing sentences to order.
    #Conditions
    The following text data is a summary of the transcribed audio, which was into multiple chunks.
    Please make sure to output the data in Japanese.
    Please output only  content and no other remarks.
    Please understand the following sentences and note the paragraphs and turns in the story
    
    #Order
    Please convert the following text into a markdown format for posting on your blog.
    Please do not lose any of the content.

    #sentence:
    '''


    summaries = []
    #usages = 0
    input_token = 0
    output_token = 0
    
    for i, doc in enumerate(docs):
        prompt_to_use = prompt
       
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
     
    
    print(f"この要約に${total_cost_usd:.4f} ({total_cost_jpy:.2f}円)かかりました。")
    
    print(f"処理時間：{time.time() - start_time:.2f}sec")

