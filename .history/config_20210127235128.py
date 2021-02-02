DEBUG = True

# Define the application directory
import os  
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Auto reload templates
TEMPLATES_AUTO_RELOAD = True  


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JSON_AS_ASCII = False


# UPLOAD FOLDER 

# UPLOAD_FOLDER = MY_UPLOAD