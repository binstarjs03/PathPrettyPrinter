"""Path Pretty Printer"""

from abc import ABC, abstractmethod
import os

TVERTICAL   = '│  '
TBRANCH     = '├──'
TLAST       = '└──'
TSPACE      = '   '

        
class DiskItem(ABC):
    """Represent item of disk. May be a file or folder.
    
    Attributes:
    - path: path of this item (including the directory path and the name of the item)
    - name: name of this item
    """
    def __init__(self, path:str) -> None:
        self._checkPath(path)
        self.path = path
        self.name = os.path.basename(path)
        
    @abstractmethod
    def _checkPath(self, path:str) -> None:
        ...
            
    def getTypeName(self) -> str:
        return self.__class__.__name__
        
    def __str__(self) -> str:
        return self.name

        
class File(DiskItem):
    """Represent file of disk
    
    Attributes:
    - path: path of this file (including the directory path and the name of the file)
    - name: name of this file
    """
    def _checkPath(self, path:str) -> None:
        if os.path.isfile(path) is False:
            raise OSError("Path is not file or nonexistent")

        
class Folder(DiskItem):
    """Represent folder of disk
    
    Attributes:
    - path: path of this folder (including the directory path and the name of the folder)
    - name: name of this folder
    - childs: items this folder contain. May be files or folders
    """
    def __init__(self, path:str) -> None:
        super().__init__(path)
        self.childs:list[File | Folder] = []
        
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
            
    def _checkPath(self, path: str) -> None:
        if os.path.isdir(path) is False:
            raise OSError("Path is not folder or nonexistent")
        
    def __str__(self) -> str:
        return f"{self.name}{self.childs}"

    
def _pretty(item: File | Folder, trees:list=[], postfix='', lastParent=True,isRoot=False):
    t = ''
    for tree in trees:
        t += tree
        
    if isinstance(item, File):
        print(f"{t}{postfix}─{item.name}")
    
    elif isinstance(item, Folder):
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
            
    else:
        raise TypeError("Not a file or folder object")

def PrintFolder(path:str):
    """Pretty print folder structure.
    Path is assumed to be folder directory."""
        
    folder = Folder(path)
    _pretty(folder, isRoot=True)
