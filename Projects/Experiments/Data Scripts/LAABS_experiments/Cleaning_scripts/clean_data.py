###
if __name__ == "__main__":
	import os
	import Cleaning_scripts.Basic_functions as b_f
	import Cleaning_scripts.Dataframe_functions as d_f
	
	session = input("Introduce session date:")
	
	base_dir = os.getcwd()
	 
	b_f.create_dataframe_player(session)
	os.chdir(base_dir)
	
	b_f.create_dataframe_experiment(session)
	os.chdir(base_dir)
	
	d_f.create_dataframe_active(session)
	os.chdir(base_dir)
	
	print("Cleaned!  :)")
