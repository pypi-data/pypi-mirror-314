import os

def get_deps():
    return []

def get_libs():
    return ["debug-mgr"]

def get_libdirs():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return [pkg_dir]

def get_incdirs():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(os.path.join(pkg_dir, "include")):
        return [os.path.join(pkg_dir, "include")]
    else:
        root_dir = os.path.abspath(os.path.join(pkg_dir, "../.."))
        return [os.path.join(root_dir, "src", "include")]


class PkgInfo(object):

    def __init__(self):
        pkgdir = os.path.dirname(os.path.abspath(__file__))
        projdir = os.path.dirname(os.path.dirname(pkgdir))

        self._name = "debug-mgr"
        if os.path.isdir(os.path.join(projdir, "src")):
            self._incdirs = [os.path.join(projdir, "src", "include")]
            self._libdirs = [
                os.path.join(projdir, "build", "lib"),
                os.path.join(projdir, "build", "lib64")]
        else:
            self._incdirs = [os.path.join(pkgdir, "share", "include")]
            self._libdirs = [os.path.join(pkgdir)]

        self._deps = []
        self._libs = ["debug-mgr"]

    @property
    def name(self):
        return self._name

    def getDeps(self):
        return self._deps
    
    def getIncDirs(self):
        return self._incdirs
    
    def getLibDirs(self):
        return self._libdirs
    
    def getLibs(self):
        return self._libs
    
