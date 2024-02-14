import os
import glob

class Utils():
    @classmethod
    def getAllFiles(cls, path):
        return glob.glob(f"{path}/*.mp4")

    @classmethod 
    def clearFolder(cls, path, verbose=False):
        files = Utils.getAllFiles(path)

        if verbose: 
            print(f"Removing all video files from path: {path}")

        for file in files:
            os.remove(file)

        if verbose:
            print(f"{len(files)} video clips successfully removed from {path}")