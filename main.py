from fastapi import FastAPI
from pydantic import BaseModel
from xgboost import XGBClassifier
import pickle
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

# インスタンス化
app = FastAPI()

# 入力するデータ型の定義
class Smiles(BaseModel):
    smiles: str

# 学習済みのモデルの読み込み
model = pickle.load(open('XGBoost_model.pkl', 'rb'))

# トップページ
@app.get('/')
async def index():
    return {"influ": 'influ_prediction'}

# POST が送信された時（入力）と予測値（出力）の定義
@app.post('/make_predictions')
async def make_predictions(smiles: Smiles):
    if not smiles.smiles:
        return({'prediction':1})
    mol = Chem.MolFromSmiles(smiles.smiles)
    fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048, useFeatures=True)
    result=model.predict([np.array(fingerprint)])
    result=result[0]
    return({'prediction':int(result)})