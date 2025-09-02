import platform, subprocess

print("Python version:", platform.python_version())
print("\nInstallerade paket:")
subprocess.run(["pip", "list"])
