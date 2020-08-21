import  subprocess

while True:
    process = subprocess.Popen(['python', 'main.py'])
    process.wait()