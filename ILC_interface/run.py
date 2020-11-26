import os
import sys
import pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/../"))


from app import app

if __name__ == '__main__':
    #running my file
    app.run(debug=True, port=81)
