#!/usr/bin/env python
import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, use_reloader=True)