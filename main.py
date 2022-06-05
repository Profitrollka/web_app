#!/usr/bin/env python3
from app import create_app
from config import config

app = create_app(config.development)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

