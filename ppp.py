"""Path Pretty Printer"""

import os

TVERTICAL   = '│  '
TBRANCH     = '├──'
TLAST       = '└──'
TSPACE      = '   '

        
class File():
    def __init__(self, path:str) -> None:
        self._checkPath(path)
        self.path = path
        self.name = os.path.basename(path)
        
    def _checkPath(self, path:str):
        if os.path.isfile(path) is False:
            raise OSError("Path is not file or nonexistent")
            
    def _type(self):
        return "File"
        
    def __repr__(self) -> str:
        return self.name
        
class Folder(File):
    def __init__(self, path:str) -> None:
        super().__init__(path)
        self.childs:list[File] = []
        
        childs = os.listdir(path)
        for child in childs:
            p = os.path.join(path, child)
            if os.path.isdir(p):
                c = Folder(p)
            elif os.path.isfile(p):
                c = File(p)
            else:
                raise OSError("Child directory is not file or folder")
            self.childs.append(c)
            
    def _checkPath(self, path: str):
        if os.path.isdir(path) is False:
            raise OSError("Path is not folder or nonexistent")
            
    def _type(self):
        return "Folder"
        
    def __repr__(self) -> str:
        return f"{self.name}{self.childs}"

    
def _pretty(item: File | Folder, trees:list=[], postfix='', lastParent=True,isRoot=False):
    t = ''
    for tree in trees:
        t += tree
        
    if not isinstance(item, Folder):
        print(f"{t}{postfix}─{item.name}")
    
    if isinstance(item, Folder):
        if isRoot:
            print(f"{item.name}")
        else:
            print(f"{t}{postfix}●{item.name}")

        last = len(item.childs) - 1
        localtrees = trees[:]
        if not lastParent:
            localtrees.append(TVERTICAL)
        elif not isRoot:
            localtrees.append(TSPACE)
            
        for id, child in enumerate(item.childs):
            if id != last:
                childPrefix = TBRANCH
                lastChild = False
            else:
                childPrefix = TLAST
                lastChild = True
            _pretty(child, localtrees, childPrefix, lastChild)

def PrintFolder(path:str):
    """Pretty print folder structure.
    Path is assumed to be folder directory."""
    if os.path.isdir(path) is False:
        raise OSError("Path is not folder or nonexistent")
        
    folder = Folder(path)
    _pretty(folder, isRoot=True)
