from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

#Replicando a classe Transformer para realizar pré-processamento das infos do cliente
class Transformer(BaseEstimator, TransformerMixin):
  def __init__(self, quant_columns, cat_columns):
    self.quant_columns = quant_columns
    self.cat_columns = cat_columns
    self.enc = OneHotEncoder()
    self.scaler = MinMaxScaler()

  def fit(self, x, y=None): #funções da classe devem ter o mesmo nome do método usado
    self.enc.fit(x[self.cat_columns])
    self.scaler.fit(x[self.quant_columns])
    return self

  def transform(self, x, y=None): #funções da classe devem ter o mesmo nome do método usado
    x_categoricals = pd.DataFrame(data=self.enc.transform(x[self.cat_columns]).toarray(),
                                  columns=self.enc.get_feature_names(self.cat_columns))
    
    x_quants = pd.DataFrame(data=self.scaler.transform(x[self.quant_columns]),
                            columns=self.quant_columns)
    
    x = pd.concat([x_quants , x_categoricals], axis=1)

    return x

