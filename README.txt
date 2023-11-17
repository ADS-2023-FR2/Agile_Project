This README contains information about the scripts of the spotlight deployment. These four scripts are designed in order to be executed in the command libe, providing arguments that can vary depending on the situation.

1.- fit_newmodel_from_movielens_dataset.py

This script fits a Explicit Factorization Model based on one of movielens dataset. 
Arguments:
	--input: Path to the folder that contains spotlight. By the moment, I can not import spotlight from the github repo, so I just copied to the same directory the spotlight repository. Default = 'None'.
	--variant: Variant of movielens model. Accepted values: '100K','1M','10M','20M'. Default = '100K'.
	--niter: Number of iterations of the fit. Default = 3.
	--out_model: Output path of the model (binary pkl file). Note that this model is a Explicit Factorization Model. Default = 'None'.
	--out_dataset: Output path of the dataset (csv file). Default = 'None'.


2.- create_sequencial_dataset.py

Creates a sequencial dataset, using parameters that the user can introduce.
Arguments:
	--input: Path to the folder that contains spotlight. By the moment, I can not import spotlight from the github repo, so I just copied to the same directory the spotlight repository. Default = 'None'.
	--nusers: Number of users in the dataset. Default = 100.
	--nitems: Number of items in the dataset. Default = 1000.
	--niteractions: Number of interactions in the dataset. Default = 10000
	--concentration: Concentration rate. Default = 0.05
	--order: Order of the dataset. Default = 3
	--out_dataset: Output path of the dataset (csv file). Default = 'None'.

3.- fit_newmodel.py
Creates a new Explicit Factorization Model using a previous dataset.
Arguments:
	--input: Path to the folder that contains spotlight. By the moment, I can not import spotlight from the github repo, so I just copied to the same directory the spotlight repository. Default = 'None'.
	--in_dataset: Input path of the dataset (csv file). If not provided, the script will created and if you want, you can export it. Default = 'None'.
	--niter: Number of iterations of the fit. Default = 3.	
	--out_model: Output path of the model (binary pkl file). Default = 'None'.
	--out_predictions: Output path of the predictions of the test set (csv file). Default = 'None'.

4.- predict_previousmodel.py
Makes a prediction of a dataset using a previously fitted model. The dataset must be imported and the model is a Explicit Factorization Model.
Arguments:
	--input: Path to the folder that contains spotlight. By the moment, I can not import spotlight from the github repo, so I just copied to the same directory the spotlight repository. Default = 'None'.
	--in_model: Input path of the pretrained model (binary pkl file). If not provided, exit().
	--in_dataset: Input path of the dataset (csv file). If not provided, the script will created and if you want, you can export it. Default = 'None'.
	--out_predictions: Output path of the predictions of the test set (csv file). Default = 'None'.
