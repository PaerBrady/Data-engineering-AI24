import os, sys
print("Hello from container!")
print("Python version:", sys.version.split()[0])

TEST_FILE = os.path.join(os.path.dirname(__file__), "hello.txt")
with open(TEST_FILE, "w", encoding="utf-8") as f:
    f.write("Detta skrevs från containern via bind-mount.\n")
with open(TEST_FILE, "r", encoding="utf-8") as f:
    print("File content:", f.read().strip())
