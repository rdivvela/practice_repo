

############ENVIRONMENT#################
create_environment:
	conda env create -f environment.yaml --force

export_environment:
	conda env export > environment.yaml

destroy_environment:
	conda remove --name $(ENV_NAME) --all
