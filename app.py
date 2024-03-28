import streamlit as st
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
import requests

from pathlib import Path
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
from rdkit.Chem import inchi
from rdkit.Chem import Draw

st.title('インフルエンザ 効果判定')  

smiles = st.text_input(' smiles を入力後、判定ボタンを押す')
# print(response.status_code)


if st.button('判定'):
    response = requests.post(url='https://influenza-classifer-app.onrender.com/make_predictions', json={'smiles': smiles})

    mol = Chem.MolFromSmiles(smiles)
    img = Chem.Draw.MolToImage(mol)
    st.image(img)

    #plt.imshow(img)

    target = ['効果あり', '不明', '効果なし']

    prediction = response.json()['prediction']

    st.write('## 予測結果')
    st.write('#### この化合物はインフルエンザに対して「', str(target[int(prediction)]),'」です')
