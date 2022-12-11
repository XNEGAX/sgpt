import os
import subprocess

def ejecutando_proceso(titulo,command,path=None):
    os.system('CLS')
    os.system('clear')
    print(titulo)
    if path:
        proc = subprocess.Popen(command,shell=True, cwd=path)
    else:
        proc = subprocess.Popen(command,shell=True)
    
    proc.communicate()
    return proc.wait()

project_path = os.path.dirname(os.path.realpath(_file_))
repo_path =f'{project_path}'

ejecutando_proceso("""DETENIENDO CONTENEDORES""","docker stop $(docker ps -a -q)",repo_path)
ejecutando_proceso("""ELIMINANDO CONTENEDORES""","docker rm $(docker ps -a -q)",repo_path)
ejecutando_proceso("""ELIMINANDO IMAGENES""",["docker system prune -a --volumes"],repo_path)
os.system('CLS')
os.system('clear')
print("""DOCKER LIMPIO""")