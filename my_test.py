import ast
import sys, os
import json
from ast2json import ast2json
import time


def _reader(filename):
    content = []
    with open(filename, encoding='iso-8859-15') as file:
        #try:
            for line in file:
                if line.startswith('#'):# or line.startswith(' """ ') or line.endswith(' """ '):
                    continue  # skip comments
                content.append(line.strip())
        #except: UnicodeDecodeError
    return str(content)

def _save_single_file_tree(content, s_file):
    # TO DO 
        # create in diferent folder depending on the structure
    tree = ast.parse(content)
    astprint = ast2json(tree)
    name = s_file.split('.')
    print(name)
    f = open(name[0] + ".txt", "w")
    f.write(json.dumps(astprint, indent=3))
    f.close()

def _save_only(string):
    with open('imports.txt','w') as f:
        f.write('\n'.join(map(str, string)))

def _management_imports(content, level, path):
    if content != []:
        imports_ini = [] # import, alias, importFrom
        aux = content.split('\n') # separo por saltos de linea
        aux_tmp = aux[:]
        for i in range(len(aux)):
            if aux[i].startswith("import"):
                #imports_ini.insert(0, [aux[i], level, path])
                imports_ini.insert(0, [aux[i], level])
                aux_tmp.remove(aux[i])

            elif aux[i].startswith("from"):
                #imports_ini.insert(0, [aux[i], level, path])
                imports_ini.insert(0, [aux[i], level])
                aux_tmp.remove(aux[i])  
            else:
                pass
        return imports_ini
    
def _management_files(content, imports, level):
    tree = ast.parse(content)
    astprint = ast2json(tree)
    string = json.dumps(astprint, indent=2**level)
    return string

def main(name):
    start = time.time()
    folder = sys.argv[1]
    print(folder)
    #mode = sys.argv[2]

    if len(sys.argv) < 3 :
        print("::::: funciona con carpeta, modo :::::")
        print(" 1: < de un fichero ")
        print(" 2: = fichero ")
        print(" 3: = carpeta ")
        print(" 4: = proyecto ")

    elif sys.argv[2] == '2':
        for i in os.walk(folder):
            dirpath, dirnames, filenames = i[0], i[1], i[2]
            for s_file in filenames:
                fullpath = os.path.join(dirpath, s_file)
                if s_file.endswith('.py'):
                    content = _reader(fullpath)
                    _save_single_file_tree(content, s_file)

    elif sys.argv[2] == '3':
        info = [0,0] # empty, no empty
        imports_ini = []
        all_ini = []
        body = []
        body_all = []

        some_dir = folder.rstrip(os.path.sep)
        num_sep = some_dir.count(os.path.sep)

        for i in os.walk(folder):
            dirpath, dirname, filnames = i[0], i[1], i[2]
  
            for s_file in filnames:
                level = abs(num_sep-dirpath.count(os.path.sep))
                fullpath = os.path.join(dirpath, s_file)
                if s_file.endswith('.py'):
                    if s_file == '__init__.py' and os.path.getsize(fullpath) == 0:
                        info[0] += 1
                    elif s_file == '__init__.py' and os.path.getsize(fullpath) != 0:
                        info[1] += 1
                        content = _reader(fullpath)
                        imports_ini = _management_imports(content, level, dirpath.rstrip(os.path.sep))
                        all_ini.insert(0, imports_ini)
                    else:
                        content = _reader(fullpath)
                        body = _management_files(content, imports_ini, level)
                        body_all.append(body)
                        pass
        
        all_ini = list(filter(None, all_ini))
        print(info)
        #_save_only(all_ini)
        _save_only(body_all)

        print(abs(start-time.time()))
               

if __name__ == '__main__':
    main(sys.argv[1])