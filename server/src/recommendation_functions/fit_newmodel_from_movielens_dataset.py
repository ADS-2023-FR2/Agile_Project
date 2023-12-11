import pandas as pd
import pickle
import argparse

import os
import sys

current_script_directory = os.path.dirname(os.path.abspath(__file__))
module_directory = os.path.join(current_script_directory, '..', 'splotlight')
sys.path.append(module_directory)

from cross_validation import random_train_test_split
from datasets.movielens import get_movielens_dataset
from evaluation import rmse_score
from factorization.explicit import ExplicitFactorizationModel


def main():
    parser = argparse.ArgumentParser(description='REQUIREMENTS: pandas,spotlight,,pickle,sys')
    parser.add_argument('--input', dest='input', type = str, help='Path to the folder that contains spotlight',default='None')
    parser.add_argument('--variant', dest = 'variant', type = str, help='Variant of movielens model',default = '100K')
    parser.add_argument('--niter', dest = 'niter', type = int, help='Number of iterations of the fit',default = 3)
    parser.add_argument('--out_model', dest = 'out_model', type = str, help='Output path of the model (binary pkl file)',default = 'None')
    parser.add_argument('--out_dataset', dest = 'out_dataset', type = str, help='Output path of the dataset (csv file)',default='None')
    parser.add_argument('--out_predictions', dest = 'out_predictions', type = str, help='Output path of the predictions (csv file)',default='None')
    
    args = parser.parse_args()
    
    process (args.input,args.variant, args.niter,args.out_model, args.out_dataset,args.out_predictions)

def process(folder, var, niter, out_model, out_dataset, out_predictions):
    
    if folder != 'None':
        import sys  
        sys.path.insert(0, folder)
    
    possible_variants = ['100K','1M','10M','20M']
    
    if var not in possible_variants:
        print ('No existe esta variante de movielens')
        exit()
    
    dataset = get_movielens_dataset(variant=var)
    
    #print (dataset.sequences.user_ids)
    
    train, test = random_train_test_split(dataset,test_percentage=0.2)
    
    #interactions = Interactions(dataset)
    # ... (cargar o crear el conjunto de datos)
    
    # Convertir a DataFrame de pandas y guardar en CSV
    

    if out_dataset != 'None':
        
        df = pd.DataFrame({'user_id': dataset.user_ids,
                           'item_id': dataset.item_ids,
                           'rating': dataset.ratings})
        
        # Convertir a DataFrame de pandas y guardar en CSV
        try: 
            df.to_csv(out_dataset, index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
    
    model = ExplicitFactorizationModel(n_iter=niter)
    model.fit(train)
    
    if out_model != 'None':
        with open(out_model, 'wb') as f:
            try:
                pickle.dump(model, f) 
                print ('Modelo exportado correctamente')
            except:
                print ('No se ha podido exportar el modelo')
                exit()
            
    predictions = model.predict(test.user_ids,test.item_ids)
    
    if out_predictions != 'None':
        
        df_predictions = pd.DataFrame({
        'user_id': test.user_ids,
        'item_id': test.item_ids,
        'prediction': predictions
        })
        # Guardar el DataFrame en un archivo CSV
        try: 
            df_predictions.to_csv(out_predictions,index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
    
    rmse = rmse_score(model, test)
    
    print (rmse)


if __name__ == '__main__':
    main()