import os
from pathlib import Path, PurePath, PureWindowsPath
#https://www.delftstack.com/es/howto/python/how-to-get-the-current-script-file-directory/

wd = os.getcwd()
print("working directory is ", wd)
x = PureWindowsPath(wd)
y = str(x)
print(x)


p = Path('.')
print(p)

pp = PurePath('main.py')
print(pp)

def get_path_from_template(path_template: str, path_type: PathType = PathType.AUTO) -> str:
    """Replace tags in the given path template and return either Windows or Linux formatted path."""
    # automatically select path type depending on running OS
    if path_type == PathType.AUTO:
        if platform.system() == "Windows":
            path_type = PathType.WINDOWS
        elif platform.system() == "Linux":
            path_type = PathType.LINUX
        else:
            raise RuntimeError("Unknown platform")

    path_template = path_template.replace("<USERNAME>", get_user_name())

    # return correctly formatted path
    if path_type == PathType.WINDOWS:
        return str(pathlib.PureWindowsPath(path_template))
    elif path_type == PathType.LINUX:
        return str(pathlib.PurePosixPath(path_template))
    else:
        raise RuntimeError("Unknown platform") 