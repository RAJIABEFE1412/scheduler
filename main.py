# from flask import Flask, jsonify

# app = Flask(__name__)

# # The existing code from your project

# # ... (copy the entire code above)

# # Add the following lines to create a Flask endpoint


# if __name__ == '__main__':
#     app.run(debug=True)




# main.py
from flask import Flask, request, jsonify
from models import Data
from utils import DisplayMgr
from routes import generate_schedule

app = Flask(__name__)

app.register_blueprint(generate_schedule)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
