# !pip install -U sentence-transformers

# from transformers import BertTokenizer,BertForPreTraining,BertModel
# from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import nltk
from nltk import sent_tokenize
from tqdm import tqdm


nltk.download('punkt')

import os
def check_file_exists(path):
  return os.path.isdir(path)

def get_model_name_or_local_path(model_local_path, model_name):
  if check_file_exists(model_local_path):
    return model_local_path
  return model_name

import re
def process_text(text):
  text = re.sub("\[L\d*\]", "",text)
  text = text.replace("[","")
  text = text.replace("]","")
  return text



from collections import defaultdict
from functools import partial

# NOT modelden input size'ı anlama,
def create_embeddings(model, data, column, drop_column=True):
  # model._modules['1'].get_sentence_embedding_dimension()
  # shape = (1,model._modules['0'].get_word_embedding_dimension())
  shape = model._modules['0'].get_word_embedding_dimension()
  column_embeddings_dict = defaultdict(lambda: np.zeros(shape))
  for index, row in tqdm(data.iterrows()):
    # if index == 10:
    #   break
    text = data[column][index]
    # else'de zero
    if text == None or type(text) != str:
      embeddings = None
    else:
      sentences = sent_tokenize(text)
      embeddings = model.encode(sentences)

  #TODO benzer olan ilacın embedding değerini vererek dene
    if embeddings is None or len(embeddings) == 0: #embedding check none type
      sum_of_embeddings = np.zeros(shape)
    else:
      sum_of_embeddings = np.sum(embeddings, axis = 0)
    # column_embeddings_dict[row['id']] = sum_of_embeddings.reshape(1, -1) # 2d
    column_embeddings_dict[row['id']] = sum_of_embeddings
    # data.iloc[index][column+'_embedding']=sum_of_embeddings
  
  data[column+'_embedding'] = pd.Series(column_embeddings_dict.values())
  if(drop_column):
    data.drop([column], axis = 1, inplace = True)
  # data[column+'_embedding'] = [column_embeddings_dict[row['name']] for index, row in data.iterrows()]
  return column_embeddings_dict

