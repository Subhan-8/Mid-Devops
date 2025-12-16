from dotenv import load_dotenv
load_dotenv('.env')

from ssis import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
    