from os import listdir, rename
from os.path import splitext
from sys import argv, exit

if len(argv) < 2:
    print("Usage:",argv[0],"directory")
    exit()

for fname in listdir(argv[1]):
    fn, fe = splitext(fname)
    if fe != ".png":
        continue
    newfn = fn.replace(".", "")[:-6]
    rename(argv[1]+"/"+fname, argv[1]+"/"+newfn+fe)