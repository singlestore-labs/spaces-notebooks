import json
import time
from concurrent.futures import ThreadPoolExecutor

import openai
import torch
from flask import Flask
from flask import request
from openai import OpenAI
from transformers import AutoModel
from transformers import AutoTokenizer

# Set up OpenAI
api_key = 'add your openai key'
client = OpenAI(api_key=api_key)

# Load Hugging Face model
model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
hf_model = AutoModel.from_pretrained(model_name)
hf_tokenizer = AutoTokenizer.from_pretrained(model_name)

# Hugging Face embedding function


def get_hf_embedding(texts):
    embeddings = []
    for text in texts:
        inputs = hf_tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            embedding = hf_model(**inputs).last_hidden_state.mean(dim=1)
            norm = torch.linalg.vector_norm(embedding, ord=2, dim=1, keepdim=True)
            normalized_embedding = embedding / norm
            embeddings.append(normalized_embedding.squeeze().tolist())
    return embeddings

# OpenAI embedding function


def get_ada_002_embedding(texts, model='text-embedding-ada-002'):
    responses = openai.embeddings.create(input=texts, model=model)
    return [response.embedding for response in responses.data]


def process_batch(batch, model_name):
    texts = [text for text in batch if isinstance(text, str) and text.strip()]
    if not texts:
        return []
    if model_name == 'openai_embedding':
        try:
            return get_ada_002_embedding(texts, 'text-embedding-ada-002')
        except Exception as e:
            print(f'Error in OpenAI processing: {e}')
            return []
    elif model_name == 'hf_embedding':
        return get_hf_embedding(texts)
    else:
        print(f'Invalid model name: {model_name}')
        return []


app = Flask(__name__)


@app.route('/functions/get_embedding', methods=['POST'])
def get_embedding():
    """ incoming data is this format :
    {"data":
    [[<row id>, <data string >, <model_name string>],
    [<row id>, <data string >, <model_name string>],
    ... ]}
     """
    start_time = time.time()
    row_ids, args, model_names = [], [], []
    for row_id, data, model_name in request.json['data']:
        row_ids.append(row_id)
        args.append(data)
        model_names.append(model_name)

    batch_size = 1024
    futures = []
    with ThreadPoolExecutor(max_workers=len(args) // batch_size) as executor:
        for i in range(0, len(args), batch_size):
            batch = args[i:i + batch_size]
            # Assuming all texts in the batch use the same model
            model_name = model_names[i]
            futures.append(executor.submit(process_batch, batch, model_name))

    flat_results = [future.result() for future in futures]
    time_taken = time.time() - start_time
    app.logger.info(f'Time taken: {time_taken} seconds')
    res = map(json.dumps, flat_results)
    return dict(data=list(zip(row_ids, res)))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
