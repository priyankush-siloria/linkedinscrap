import os

base_dir1 = os.getcwd()
print(type(base_dir1))
print(base_dir1)


base_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
print(type(base_dir))
print(base_dir)