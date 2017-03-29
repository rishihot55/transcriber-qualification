# transcriber-qualification

for http://cmusphinx.sourceforge.net/wiki/summerofcodeideas

## Build Instructions

To set up the project for development, perform the following actions:

- Install the required packages (either in a virtual environment or normally) using `pip install -r requirements.txt`
- Include jQuery and Bootstrap via [Bower](https://bower.io/) through the command `bower install` or download and move them manually into the `app/static` folder
- If installed using bower, run the static file setup script `sh ./static_setup.sh`
- After completing the previous steps, start the flask server using `python run.py`

## Deployment on PythonAnywhere

The deployment steps for PythonAnywhere are as follows:
- Open up a bash console and clone the project using `git clone https://github.com/rishihot55/transcriber-qualification` to your desired path
- Perform the previously mentioned [build steps](#build-instructions)
- Go to the Web tab and click on _Add a new webapp_ and select *Manual configuration* and select **Python 3.5** as the version. This will provide a customizable configuration which we can work with.
- Open up the bash console once more and go to `/var/www/`, which will contain the WSGI file to be modified. It will be called `<username>_pythonanywhere_com_wsgi.py`
- Open up the WSGI file in the editor, clear the existing config and enter the following:
```
import sys
path=<path to the project>
if path not in sys.path:
	sys.path.append(path)

from app import app as application
```
- If you have used a virtual environment, specify its path on the virtualenv directory portion of the Web dashboard
- `(Optional)` Add the path to the static files by specifying the url and the location of the static files. This is usually in the `app/static` folder of the project
- Click on _Reload Configuration_ to see your site deployed on `<username>.pythonanywhere.com`