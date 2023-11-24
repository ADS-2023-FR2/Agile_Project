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
    parser.add_argument('--user',dest='user', type=int, help='user that we are going to predict their ratings')
    parser.add_argument('--out_predictions', dest = 'out_predictions', type = str, help='Output path of the predictions (csv file)',default='None')
    
    args = parser.parse_args()
    
    process (args.input,args.in_model,args.in_dataset,args.user,args.out_predictions)

def process(folder,in_model,in_dataset,user,out_predictions):
    
    import numpy as np
    if folder != 'None':
        import sys  
        sys.path.insert(0, folder)
    
    if np.isnan(user) == True:
        print ('No user provided')
        exit()
        
    print ('User: ', user)
    
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
    
    list_items = list(np.unique(interactions.item_ids))
    
    print ('LEN LIST ITEMS:', len(list_items))
    
    ratings =list (np.zeros(len(list_items)))
    for i in range (len(interactions.user_ids)):
        if interactions.user_ids[i] == user:
            ratings[interactions.item_ids[i]] = int (interactions.ratings[i])  
        
    df_user = pd.DataFrame ({'user_id':[user]*len(list_items), 'item_id': list_items, 'ratings':ratings})
    
    df_user = df_user[df_user['ratings']==0]
    
    with open(in_model, 'rb') as f:
        try:
            model = pickle.load(f)
            print ('Modelo importado')
        except:
            print ('No se ha obtenido el modelo')
            exit()
            
    interactions_user = Interactions(user_ids=df_user['user_id'].values,
                                     item_ids=df_user['item_id'].values,
                                     ratings=df_user['ratings'].values)
    print (interactions_user)
    predictions = model.predict(interactions_user.user_ids,interactions_user.item_ids)
    print (predictions)
        
    df_user['predictions'] = predictions
    
    print (df_user)
    
    if out_predictions != 'None':
        # Guardar el DataFrame en un archivo CSV
        try: 
            df_user.to_csv(out_predictions,index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
    
    return df_user


if __name__ == '__main__':
    main()

