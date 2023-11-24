import pandas as pd
import argparse

import sys
sys.path.append('../')
from spotlight.datasets.synthetic import generate_sequential

def main():
    parser = argparse.ArgumentParser(description='REQUIREMENTS: pandas,spotlight,sys')
    parser.add_argument('--input', dest = 'input', type = str, help='Path to the folder that contains spotlight',default='None')
    parser.add_argument('--nusers', dest = 'nusers', type = int, help='Number of users in the dataset',default = 100)
    parser.add_argument('--nitems', dest ='nitems',type = int, help='Number of items in the dataset',default = 1000)
    parser.add_argument('--ninteractions', dest = 'ninteractions', help='Number of interactions in the dataset',default = 10000)
    parser.add_argument('--concentration', dest = 'concentration', type = float, help='Concentration rate', default = 0.05)
    parser.add_argument('--order', dest = 'order', type = int, help='Order of the dataset', default = 3)
    parser.add_argument('--out_dataset', dest = 'out_dataset', type = str, help='Output path of the dataset (csv file)',default='None')
    
    args = parser.parse_args()
    
    process (args.input,args.nusers,args.nitems,args.ninteractions,args.concentration,args.order, args.out_dataset)

def process(folder,nusers,nitems,ninteractions,concentration,order,out_dataset):
    
    if folder != 'None':
        import sys  
        sys.path.insert(0, folder)
    
    import pandas as pd
    
    
    dataset = generate_sequential(num_users=nusers,
                              num_items=nitems,
                              num_interactions=ninteractions,
                              concentration_parameter=concentration,
                              order=order)
    
    # Convertir a DataFrame de pandas y guardar en CSV
    df = pd.DataFrame({'user_id': dataset.user_ids,
                       'item_id': dataset.item_ids,
                       'rating': dataset.ratings})

    if out_dataset != 'None':
        try:
            df.to_csv(out_dataset, index=False)
            print ('Documento creado')
        except:
            print ('No se puede crear documento')
            exit()


if __name__ == '__main__':
    main()
