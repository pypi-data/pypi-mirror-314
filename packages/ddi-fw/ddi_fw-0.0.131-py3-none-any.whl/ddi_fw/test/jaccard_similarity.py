import pandas as pd

# data = {'A': [1, 1, 1, 0, 0],
#         'B': [0, 1, 1, 1, 0],
#         'C': [0, 0, 1, 1, 1]}

# df = pd.DataFrame(data)


# from scipy.spatial.distance import pdist, squareform

# jaccard_dist = pdist(df.values, metric='jaccard')
# jaccard_dist_matrix = squareform(jaccard_dist)

# print(jaccard_dist_matrix)


# import pandas as pd
# from scipy.spatial.distance import euclidean, pdist, squareform


# def similarity_func(u, v):
#     return 1/(1+euclidean(u,v))

# DF_var = pd.DataFrame.from_dict({"s1":[1.2,3.4,10.2],"s2":[1.4,3.1,10.7],"s3":[2.1,3.7,11.3],"s4":[1.5,3.2,10.9]})
# DF_var.index = ["g1","g2","g3"]

# dists = pdist(DF_var, similarity_func)
# DF_euclid = pd.DataFrame(squareform(dists), columns=DF_var.index, index=DF_var.index)

# print(DF_euclid)


from sklearn.metrics import jaccard_score
import seaborn as sns
import matplotlib.pyplot as plt

data = [[0, 1, 0], [0, 1, 1], [0, 1, 0], [1, 1, 1], [1, 0, 1]]

similarity_matrix = []
for i in range(len(data)):
        row = []
        for j in range(len(data)):
          row.append(jaccard_score(data[i], data[j]))
        similarity_matrix.append(row)

sns.heatmap(pd.DataFrame(similarity_matrix), annot=True, cmap="YlGnBu")
plt.show()


# https://stackoverflow.com/questions/35639571/python-pandas-distance-matrix-using-jaccard-similarity
import pandas as pd
entries = [
    {'id':'1', 'category1':'100', 'category2': '0', 'category3':'100'},
    {'id':'2', 'category1':'100', 'category2': '0', 'category3':'100'},
    {'id':'3', 'category1':'0', 'category2': '100', 'category3':'100'},
    {'id':'4', 'category1':'100', 'category2': '100', 'category3':'100'},
    {'id':'5', 'category1':'100', 'category2': '0', 'category3':'100'}
           ]
df = pd.DataFrame(entries)

from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist, jaccard

res = 1 - pdist(df[['category1','category2','category3']], 'jaccard')
# squareform(res)
distance = pd.DataFrame(squareform(res), index=df.index, columns= df.index)
print(distance)

entries2 = [
    {'id':'1', 'cat':['p1','p2','p3']},
    {'id':'2', 'cat':['p3','p4','p5']},
    {'id':'3', 'cat':['p5','p6','p7']},
           ]
df2 = pd.DataFrame(entries2)

c = df2['cat']

y = set()

for x in c:
  for k in x:
    y.add(k)

print(y)