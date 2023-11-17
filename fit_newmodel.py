import argparse

def main():
    parser = argparse.ArgumentParser(description='REQUIREMENTS: pandas,spotlight,,pickle,sys')
    parser.add_argument('--input', dest = 'input', type = str, help='Path to the folder that contains spotlight',default='None')
    parser.add_argument('--in_dataset', dest = 'in_dataset', type = str, help='Input path of the dataset (csv file)',default='None')
    parser.add_argument('--nusers', dest = 'nusers', type = int, help='Number of users in the dataset',default = 100)
    parser.add_argument('--nitems', dest ='nitems',type = int, help='Number of items in the dataset',default = 1000)
    parser.add_argument('--ninteractions', dest = 'ninteractions', help='Number of interactions in the dataset',default = 10000)
    parser.add_argument('--concentration', dest = 'concentration', type = float, help='Concentration rate', default = 0.05)
    parser.add_argument('--order', dest = 'order', type = int, help='Order of the dataset', default = 3)
    parser.add_argument('--niter', dest = 'niter', type = int, help='Number of iterations of the fit',default = 3)
    parser.add_argument('--out_dataset', dest = 'out_dataset', type = str, help='Output path of the dataset (csv file',default='None')
    parser.add_argument('--out_model', dest = 'out_model', type = str, help='Output path of the model (binary pkl file',default='None')
    parser.add_argument('--out_predictions', dest = 'out_predictions', type = str, help='Output path of the predictions (csv file',default='None')
    
    args = parser.parse_args()
    
    process (args.input,args.in_dataset,args.nusers,args.nitems,args.ninteractions,args.concentration,args.order,args.niter,args.out_dataset,args.out_model,args.out_predictions)

def process(folder,in_dataset,nusers,nitems,ninteractions,concentration,order,niter,out_dataset,out_model,out_predictions):
    
    if folder != 'None':
        import sys  
        sys.path.insert(0, folder)
    import numpy as np
    from spotlight.cross_validation import user_based_train_test_split
    from spotlight.interactions import Interactions
    from spotlight.evaluation import sequence_mrr_score
    from spotlight.factorization.explicit import ExplicitFactorizationModel 
    from spotlight.datasets.synthetic import generate_sequential
    import pandas as pd
    import pickle
    
    
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
        
        dataset = interactions.to_sequence()
    
    else:
        interactions = generate_sequential(num_users=nusers,
                              num_items=nitems,
                              num_interactions=ninteractions,
                              concentration_parameter=concentration,
                              order=order)
        
        dataset = interactions.to_sequence()
        
    if out_dataset != 'None':
        
        # Convertir a DataFrame de pandas y guardar en CSV
        df = pd.DataFrame({'user_id': interactions.user_ids,
                           'item_id': interactions.item_ids,
                           'rating': interactions.ratings})
        try: 
            df.to_csv(out_dataset, index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
            
    print (dataset.user_ids)

    train, test = user_based_train_test_split(dataset) 
    
    model = ExplicitFactorizationModel(n_iter=niter)
    model.fit(train)
            
    predictions = model.predict(test.user_ids,test.item_ids)
    print (predictions)

        
    df_predictions = pd.DataFrame({
    'user_id': test.user_ids,
    'item_id': test.item_ids,
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
    
    if out_model != 'None':
        with open(out_model, 'wb') as f:
            try:
                pickle.dump(model, f) 
                print ('Modelo exportado correctamente')
            except:
                print ('No se ha podido exportar el modelo')
                exit()
    
    mrr = sequence_mrr_score(model, test)
     
    print (mrr)


if __name__ == '__main__':
    main()