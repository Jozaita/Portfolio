###
if __name__ == "__main__":
	import os
	import Cleaning_scripts.Basic_functions as b_f
	
	session = input("Introduce treatment:")
	
	base_dir = os.getcwd()
	 
	b_f.create_global_dataframe(session)
	os.chdir(base_dir)
	

	
	print("Generated!  :)")
