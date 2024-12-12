import os


def chdir_root(root_name = "app"):
	current_path = os.getcwd()
	origin_path = current_path
	current_path_basename = os.path.basename(current_path)

	if current_path_basename == root_name :
		return current_path

	if os.path.isdir(root_name):
		os.chdir(root_name)
		current_path = os.getcwd()
		return current_path

	while True :
		os.chdir("..")
		current_path = os.getcwd()
		current_path_basename = os.path.basename(current_path)
		if current_path_basename == root_name:
			return current_path
		if current_path_basename == "":
			os.chdir(origin_path)
			raise Exception("No path")