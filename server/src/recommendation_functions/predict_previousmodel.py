import pandas as pd
import pickle
import argparse

import sys
sys.path.append('../')
from spotlight.interactions import Interactions
from spotlight.evaluation import rmse_score

def main():
    parser = argparse.ArgumentParser(description='REQUIREMENTS: pandas,spotlight,,pickle,sys,numpy')
    parser.add_argument('--input', dest = 'input', type = str, help='Path to the folder that contains spotlight',default='None')
    parser.add_argument('--in_model', dest = 'in_model', type = str, help='Input path of the model (binary pkl file',default='None')
    parser.add_argument('--in_dataset', dest = 'in_dataset', type = str, help='Input path of the dataset (csv file)',default='None')
    parser.add_argument('--out_predictions', dest = 'out_predictions', type = str, help='Output path of the predictions (csv file)',default='None')
    
    args = parser.parse_args()
    
    process (args.input,args.in_model,args.in_dataset,args.out_predictions)

def process(folder,in_model,in_dataset,out_predictions):
    
    import numpy as np
    if folder != 'None':
        import sys  
        sys.path.insert(0, folder)
    
    if in_dataset != 'None':
        try:
            df = pd.read_csv(in_dataset)
            print ('Documento de entrada de dataset leido')
        except:
            print ('No se puede leer el documento de entrada del dataset')
            exit()
        
        # Crear un objeto Interactions desde el DataFrame
        interactions = Interactions(user_ids=df['user_id'].values.astype(np.int32),
                                    item_ids=df['item_id'].values.astype(np.int32),
                                    ratings=df['rating'].values)
    
    else:
        print ('No dataset provided')
        exit()
    
    with open(in_model, 'rb') as f:
        try:
            model = pickle.load(f)
            print ('Modelo importado')
        except:
            print ('No se ha obtenido el modelo')
            exit()
    
    predictions = model.predict(interactions.user_ids,interactions.item_ids)
        
    df_predictions = pd.DataFrame({
    'user_id': interactions.user_ids,
    'item_id': interactions.item_ids,
    'prediction': predictions
    })
    
    if out_predictions != 'None':
        # Guardar el DataFrame en un archivo CSV
        try: 
            df_predictions.to_csv(out_predictions,index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
    
    print (df_predictions)
    
    rmse = rmse_score(model, interactions)
    
    print (rmse)
    
    return df_predictions


if __name__ == '__main__':
    main()
