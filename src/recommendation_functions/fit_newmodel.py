import numpy as np
import pandas as pd
import pickle
import argparse

import sys
sys.path.append('../')
from spotlight.cross_validation import random_train_test_split
from spotlight.interactions import Interactions
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel 

def main():
    parser = argparse.ArgumentParser(description='REQUIREMENTS: pandas,spotlight,,pickle,sys')
    parser.add_argument('--input', dest = 'input', type = str, help='Path to the folder that contains spotlight',default='None')
    parser.add_argument('--in_dataset', dest = 'in_dataset', type = str, help='Input path of the dataset (csv file)',default='None')
    parser.add_argument('--niter', dest='niter', type = int, help = 'Number of iterations of the fit', default = 3)
    parser.add_argument('--out_model', dest = 'out_model', type = str, help='Output path of the model (binary pkl file',default='None')
    parser.add_argument('--out_predictions', dest = 'out_predictions', type = str, help='Output path of the predictions (csv file',default='None')
    
    args = parser.parse_args()
    
    process (args.input,args.in_dataset,args.niter,args.out_model,args.out_predictions)

def process(folder,in_dataset,niter,out_model,out_predictions):
    
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
        print ('Dataset required')
        exit()
            
    #print (interactions.user_ids)

    train, test = random_train_test_split(interactions,test_percentage=0.2) 
    
    model = ExplicitFactorizationModel(n_iter=niter)
    model.fit(train)
            
    predictions = model.predict(test.user_ids,test.item_ids)


    df_predictions = pd.DataFrame({
    		'user_id': test.user_ids,
    		'item_id': test.item_ids,
    		'prediction': predictions
    		})

    print (df_predictions)

    
    if out_predictions != 'None':
        # Guardar el DataFrame en un archivo CSV
        try: 
            df_predictions.to_csv(out_predictions,index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
    
    if out_model != 'None':
        with open(out_model, 'wb') as f:
            try:
                pickle.dump(model, f) 
                print ('Modelo exportado correctamente')
            except:
                print ('No se ha podido exportar el modelo')
                exit()
    
    rmse = rmse_score(model, test)
    
    print (rmse)


if __name__ == '__main__':
    main()
