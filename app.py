from yarn import create_app
from yarn.utils.configuration import config

if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.get('debug'))
