from typing import List, Union, Optional, Any
import json

PROD = True

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

class File:
    def __init__(self, size: int, name: str):
        self._size: int = size
        self.name: str = name
    def size(self):
        return self._size
    def __str__(self):
        return f"{self.name} ({self._size})"

class Directory:
    def __init__(self, name: str, parent: Optional[Any] = None):
        self.name: str = name
        self.files: List[Union[File, Directory]] = []
        self.parent = parent
    def size(self):
        return sum(entry.size() for entry in self.files)
    def cd(self, name: str):
        if name == "..":
            return self.parent
        return list(directory for directory in self.files if directory.name == name)[0]
    def directories(self):
        return list(filter(lambda f: isinstance(f, Directory), self.files))
    def realfiles(self):
        return list(filter(lambda f: isinstance(f, File), self.files))
    def __str__(self):
        return self.name

trueroot = Directory("")
trueroot.files.append(Directory("/"))
root = trueroot.files[0] 
cd = root

listing = []
consuming = False

for line in lines:
    args = line.split(" ")
    if consuming:
        if args[0] == "$":
            consuming = False
            for entry in listing:
                size, name = entry
                if size == "dir":
                    cd.files.append(Directory(name, cd))
                else:
                    cd.files.append(File(int(size), name))
            listing = []
        else:
            listing.append(args)
            continue

    if args[0] == "$": # entering a command
        if args[1] == "cd":
            if args[2] == "/":
                cd = root
            else:
                cd = cd.cd(args[2])
        elif args[1] == "ls":
            consuming = True

for entry in listing:
    size, name = entry
    if size == "dir":
        cd.files.append(Directory(name, cd))
    else:
        cd.files.append(File(int(size), name))

dir_sizes = []
def log_size(d):
        size = d.size()
        dir_sizes.append(size)
        return size

def get_directories(directory: Directory):
    files = {
        "FILES": {file.name: str(file) for file in directory.realfiles()},
        "SIZE": log_size(directory),
        **{sub.name: get_directories(sub) for sub in directory.directories()}
    }
    return {**files, **{}}

tree = get_directories(trueroot)

dir_sizes = dir_sizes[1:] # exclude duplicate root node

with open("out.json", "w") as j:
    json.dump(tree, j, indent=4)

print("PART 1:", sum(size for size in dir_sizes if size <= 100000))

total_unused = 70000000 - dir_sizes[0] # size of root
need_to_remove = 30000000 - total_unused

print(min(size for size in dir_sizes if size >= need_to_remove))