#! /usr/bin/python
import os
from zipfile import ZipFile
from subprocess import call, Popen, PIPE
from shutil import rmtree

cozmoclad_path_script = """
import cozmoclad

print(cozmoclad.__path__[0])

exit()
""".encode()

def clean():
    rmtree('build')
    rmtree('dist')

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

def zip_dir(zip, dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            zip.write(os.path.join(root, file))

def zip_all_the_things():
    zip = ZipFile('cozmos_night_at_the_museum.zip', 'w', zipfile.ZIP_DEFLATED)
    zip.write('windows_and_android.ps1')
    zipdir(zip, 'platform-tools')
    zipdir(zip, 'dist')
    zip.close()

clean()
build_executable_file()
zip_all_the_things()
