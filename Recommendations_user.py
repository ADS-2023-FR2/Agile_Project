import argparse

def main():
    parser = argparse.ArgumentParser(description='REQUIREMENTS: pandas,spotlight,,pickle,sys,numpy')
    parser.add_argument('--input', dest = 'input', type = str, help='Path to the folder that contains spotlight',default='None')
    parser.add_argument('--in_model', dest = 'in_model', type = str, help='Input path of the model (binary pkl file',default='None')
    parser.add_argument('--in_dataset', dest = 'in_dataset', type = str, help='Input path of the dataset (csv file)',default='None')
    parser.add_argument('--user',dest='user', type=int, help='user that we are going to predict their ratings')
    parser.add_argument('--out_predictions', dest = 'out_predictions', type = str, help='Output path of the predictions (csv file)',default='None')
    parser.add_argument('--top', dest='top', type=int, help='Top recommendations that want to be shown',default=0)
    args = parser.parse_args()
    
    get_ratings (args.input,args.in_model,args.in_dataset,args.user,args.out_predictions,args.top)

def get_ratings (folder,in_model,in_dataset,user,out_predictions,top):
    
    import pandas as pd
    if folder != 'None':
        import sys  
        sys.path.insert(0, folder)
    import predict_1user
          
    df_no_watched = predict_1user.process(folder,in_model,in_dataset,user,'None')
    
    dic = {it:pred for it,pred in zip(df_no_watched['item_id'],df_no_watched['predictions'])}
    
    df_no_watched = df_no_watched.sort_values(by='predictions', ascending=False)
    
    df_no_watched = df_no_watched.drop ('ratings', axis=1) 
    
    print (df_no_watched)
    
    if out_predictions != 'None':
        # Guardar el DataFrame en un archivo CSV
        try: 
            df_no_watched.to_csv(out_predictions,index=False)
            print ('Documento de salia del dataset creado')
        except:
            print ('No se puede crear el documento de salida del dataset')
            exit()
    
    if top != 0:
        out = df_no_watched['item_id'][:top].values
    else:
        out = df_no_watched['item_id'].values
    print (out)
    return dic,out
        
if __name__ == '__main__':
    main()
