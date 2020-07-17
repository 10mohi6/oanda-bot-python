import os

os.system("rm dist/*")
os.system("python setup.py sdist bdist_wheel")
os.system("twine upload dist/*")
