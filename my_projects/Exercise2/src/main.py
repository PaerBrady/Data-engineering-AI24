import os, sys

print("Hello from container!")
print("Python version:", sys.version.split()[0])

# Visa att bind-mount funkar genom att läsa/skriva en fil i src
TEST_FILE = os.path.join(os.path.dirname(__file__), "hello.txt")

# Skriv en rad
with open(TEST_FILE, "w", encoding="utf-8") as f:
    f.write("Detta skrevs från containern via bind-mount.\n")

# Läs tillbaka
with open(TEST_FILE, "r", encoding="utf-8") as f:
    print("File content:", f.read().strip())