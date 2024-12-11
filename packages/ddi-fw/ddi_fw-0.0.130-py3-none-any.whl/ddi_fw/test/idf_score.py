import pandas as pd
import numpy as np

# from ddi_fw.datasets.feature_vector_generation import find_distinct_elements
def find_distinct_elements(frame):
    y = set()
    for x in frame:
        if x is not None:
            for k in x:
                  y.add(k)
    return y

def calculate_idf(series):
    idf_scores = {}
    distinct_items = find_distinct_elements(series)
    sorted_distinct_items = sorted(distinct_items)
    total_document_number = len(all_data)
    for item in sorted_distinct_items:
       document_freq = series.map(set([item]).issubset).sum()
       idf = np.log(total_document_number/document_freq)
       idf_scores[item] = idf
    return idf_scores


item1 = 'T001|T002|T001|T001'
item2 = 'T002|T003'
item3 = 'T004|T005'


all_data = [item1, item2, item3]

df = pd.DataFrame(all_data, columns=['tui_description'])

df['tui_description'] = df['tui_description'].apply(
            lambda x: x.split('|') if x is not None else [])

print(df.head())

idf_scores = calculate_idf(df['tui_description'])
idf_scores_sorted_desc = sorted(idf_scores.items(), key=lambda x:x[1], reverse=True)
threshold = 1
keys_over_threshold = [k for k,v in idf_scores.items() if v > threshold]

print(idf_scores_sorted_desc)
print(keys_over_threshold)


def remove_items_by_idf_score(items):
    return [item for item in items if item in keys_over_threshold]

df['tui_description'] = df['tui_description'].apply(
            remove_items_by_idf_score)

print(df)