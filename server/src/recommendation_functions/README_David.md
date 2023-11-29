This README contains information about the scripts of the spotlight
deployment. These four scripts are designed in order to be executed in
the command libe, providing arguments that can vary depending on the
situation.

1.- fit_newmodel_from_movielens_dataset.py

This script fits a model based on one of movielens dataset. Arguments:
\--input: Path to the folder that contains spotlight. By the moment, I
can not import spotlight from the github repo, so I just copied to the
same directory the spotlight repository. Default = \'None\'. \--variant:
Variant of movielens model. Accepted values:
\'100K\',\'1M\',\'10M\',\'20M\'. Default = \'100K\'. \--niter: Number of
iterations of the fit. Default = 3. \--out_model: Output path of the
model (binary pkl file). Note that this model is a Explicit
Factorization Model. Default = \'None\'. \--out_dataset: Output path of
the dataset (csv file). Default = \'None\'. Return: Nothing

2.- create_sequencial_dataset.py

Creates a sequencial dataset, using parameters that the user can
introduce. Arguments: \--input: Path to the folder that contains
spotlight. By the moment, I can not import spotlight from the github
repo, so I just copied to the same directory the spotlight repository.
Default = \'None\'. \--nusers: Number of users in the dataset. Default =
100. \--nitems: Number of items in the dataset. Default = 1000.
\--niteractions: Number of interactions in the dataset. Default = 10000
\--concentration: Concentration rate. Default = 0.05 \--order: Order of
the dataset. Default = 3 \--out_dataset: Output path of the dataset (csv
file). Default = \'None\'. Return: Nothing

3.- fit_newmodel.py Creates a new Implicit Sequence Model using a
sequential dataset, that can be imported or created in this script.
Arguments: \--input: Path to the folder that contains spotlight. By the
moment, I can not import spotlight from the github repo, so I just
copied to the same directory the spotlight repository. Default =
\'None\'. \--in_dataset: Input path of the dataset (csv file). If not
provided, exit(). Default = \'None\'. \--niter: Number of iterations of
the fit. Default = 3. \--out_model: Output path of the model (binary pkl
file). Default = \'None\'. \--out_predictions: Output path of the
predictions of the test set (csv file). Default = \'None\'. Return:
Nothing

4.- predict_previousmodel.py Makes a prediction of a dataset using a
previously fitted model. The dataset is a sequential dataset and the
model is a Implicit Sequence Model. Arguments: \--input: Path to the
folder that contains spotlight. By the moment, I can not import
spotlight from the github repo, so I just copied to the same directory
the spotlight repository. Default = \'None\'. \--in_model: Input path of
the pretrained model (binary pkl file). If not provided, exit().
\--in_dataset: Input path of the dataset (csv file). If not provided,
exit(). Default = \'None\'. \--out_predictions: Output path of the
predictions of the test set (csv file). Default = \'None\'. Return:
DataFrame with columns user_id,item_id,rating,predictions

5.- predict_1user.py Makes a prediction of films only for 1 user with
items that the user hasn\'t rated yet. Arguments: \--input: Path to the
folder that contains spotlight. By the moment, I can not import
spotlight from the github repo, so I just copied to the same directory
the spotlight repository. Default = \'None\'. \--in_model: Input path of
the pretrained model (binary pkl file). If not provided, exit().
\--in_dataset: Input path of the dataset (csv file). If not provided,
exit(). Used to get the list of item_ids and those not rated by user.
Default = \'None\'. \--user: User that is going to be predicted. If not
provided, exit (). Default: None \--out_predictions: Output path of the
predictions of the test set (csv file). Default = \'None\'. Return:
DataFrame with columns user_id,item_id,predictions

5.- predict_1user.py Makes a prediction of films only for 1 user with
items that the user hasn\'t rated yet. Arguments: \--input: Path to the
folder that contains spotlight. By the moment, I can not import
spotlight from the github repo, so I just copied to the same directory
the spotlight repository. Default = \'None\'. \--in_model: Input path of
the pretrained model (binary pkl file). If not provided, exit().
\--in_dataset: Input path of the dataset (csv file). If not provided,
exit(). Used to get the list of item_ids and those not rated by user.
Default = \'None\'. \--user: User that is going to be predicted. If not
provided, exit (). Default: None \--out_predictions: Output path of the
predictions of the test set (csv file). Default = \'None\'. \--top: top
items that will be returned. If not provided, returns the full list of
items sorted by predictions. Return: dict{item:prediction}, list with
top
