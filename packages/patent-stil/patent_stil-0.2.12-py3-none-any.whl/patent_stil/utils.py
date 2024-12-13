import os

import wget
from tqdm import tqdm

def log(msg,file_name):
    if not os.path.exists(os.path.basename(file_name)):
        createDirs(os.path.dirname(file_name))
    with open(file_name, 'a',encoding="utf-8") as f:
        f.write(str(msg)+'\n')
def downloadFile(file_url, save_path):
    def bar_custom(current, total, width=80):
        t.total = total
        t.update(current)
    if os.path.exists(save_path):
        os.remove(save_path)
    createDirs(os.path.dirname(save_path))
    with tqdm(unit='', unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading") as t:
        return wget.download(file_url, save_path, bar=bar_custom)

def createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

