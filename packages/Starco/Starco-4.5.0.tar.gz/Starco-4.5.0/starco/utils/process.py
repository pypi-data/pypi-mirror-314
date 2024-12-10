import subprocess,sys
from starco.utils.directories import get_executed_file_path,path_maker
def pid_finder(mt):
    result = subprocess.run(f"ps -aux |grep {mt}",shell=True, stdout=subprocess.PIPE,text=True)
    pids = [i.split()[1] for i in result.stdout.split('\n') if mt in i and len(i.split())>2]
    return pids

def killer(targets:list[str]):
    if isinstance(targets,str):targets=[targets]
    pids =[]
    for i in targets:
        pids +=pid_finder(i)
    for i in pids:
        subprocess.run(f'sudo kill -9 {i}',shell=True)
        print(i)
        
def process_is_running(count=4):
    p =get_executed_file_path()
    print(p)
    pid = pid_finder(p)
    print(pid)
    return len(pid)>count

def restarter(file_name:str='run.py',virtual_dir='.venv',background=True,background_with='nohup'):
    path = path_maker()
    command=f'{path}/{virtual_dir}/bin/python {path}/{file_name}'
    killer([f'{path}/{file_name}'])
    if background:
        if background_with=='nohup':
            command = f'nohup {command} &'
        else:
            name = f"{path}/{file_name}".replace('/','_')
            command = f'screen -dmS {name} {command}'
    
    subprocess.run(command,shell=True)