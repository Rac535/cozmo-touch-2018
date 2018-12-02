#! /usr/bin/python
from subprocess import call, Popen, PIPE

cozmoclad_path_script = """
import cozmoclad

print(cozmoclad.__path__[0])

exit()
""".encode()

def get_cozmoclad_path():
    process = Popen(['pipenv', 'run', 'python'], stdout=PIPE, stdin=PIPE)
    stdout, stderr = process.communicate(input=cozmoclad_path_script)
    path = stdout.decode().strip()
    return path

def build_executable_file():
    process = call([
        'pipenv', 'run', 'pyinstaller',
        '--console',
        '--paths=' + get_cozmoclad_path(),
        'main.py'
    ])

build_executable_file()
