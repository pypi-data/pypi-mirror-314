from rdkit import Chem
from rdkit.Chem import AllChem

from urllib.request import urlopen
from urllib.parse import quote

from Bio.KEGG import REST


x = REST.kegg_find(database='drug', query='D03136')
y = x.read()
print(x)
def CIRconvert(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(ids) + '/smiles'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'Did not work'

# identifiers  = ['3-Methylheptane', 'Aspirin', 'Diethylsulfate', 'Diethyl sulfate', '50-78-2', 'Adamant']

# smiles = []

# for ids in identifiers :
#     smiles.append(CIRconvert(ids))
#     # print(ids, CIRconvert(ids))


# from rdkit.Chem import SaltRemover

# remover = SaltRemover(defnData="[Na+]\\nCC(=O)O", defnFormat=SaltRemover.InputFormat.SMILES)
# len(remover)

# remover = SaltRemover(defnFormat=SaltRemover.InputFormat.SMILES, defnData="[Cl]")
# mol = Chem.MolFromSmiles(smiles[0])

# morgan_hashed = AllChem.GetMorganFingerprintAsBitVect(mol,2,nBits=881)
# print(morgan_hashed.ToBitString())

#https://go.drugbank.com/structures/small_molecule_drugs/DB01076.smiles

# targets -> target -> polypeptide
# enzymes -> enzyme -> polypeptide
smiles = {'DB001075':'[H][C@]12OC[C@@H](O[N+]([O-])=O)[C@@]1([H])OC[C@@H]2O',
          'DB001076':'CC(C)C1=C(C(=O)NC2=CC=CC=C2)C(=C(N1CC[C@@H](O)C[C@@H](O)CC(O)=O)C1=CC=C(F)C=C1)C1=CC=CC=C1',
          'DB001077':'CC(C)C1=C(C(=O)NC2=CC=CC=C2)C(=C(N1CC[C@@H](O)C[C@@H](O)CC(O)=O)C1=CC=C(F)C=C1)C1=CC=CC=C1',
          }
morgan_hashed_dict = {}
# smile = '[H][C@]12OC[C@@H](O[N+]([O-])=O)[C@@]1([H])OC[C@@H]2O'
# smile = 'CC(C)C1=C(C(=O)NC2=CC=CC=C2)C(=C(N1CC[C@@H](O)C[C@@H](O)CC(O)=O)C1=CC=C(F)C=C1)C1=CC=CC=C1'

for drugbank_id, smile in smiles.items():
    mol = Chem.MolFromSmiles(smile)
    morgan_hashed = AllChem.GetMorganFingerprintAsBitVect(mol,2,nBits=881)
    morgan_hashed_dict.update({drugbank_id: morgan_hashed.ToList()})
    # print(morgan_hashed.ToBitString())


import pandas as pd
df = pd.DataFrame(morgan_hashed_dict.values())

from scipy.spatial.distance import pdist, squareform

jaccard_dist = 1 - pdist(df.values, metric='jaccard')
jaccard_dist_matrix = squareform(jaccard_dist)

print(jaccard_dist_matrix)



import numpy as np
import pandas as pd

# df = pd.DataFrame({'sample':[np.array(range(99999, 99999 + 1000))]}) 
df = pd.DataFrame({'sample':[np.random.random_sample((1000,))]}) 

df['sample'] = df['sample'].apply(lambda x: str(x).replace('\n', ''))

df.to_csv('sample.csv', index=False)


from ast import literal_eval
new_df = pd.read_csv('sample.csv')
def fnc(x):
     return np.array(literal_eval(x.replace('[ ', '[').replace(' ', ',')))
# new_df['array_col'] = new_df['sample'].apply(lambda x: np.array(literal_eval(x.replace('[ ', '[').replace(' ', ','))))
new_df['array_col'] = new_df['sample'].apply(lambda x: fnc(x))



print(new_df.loc[0, 'array_col'][0:10])

