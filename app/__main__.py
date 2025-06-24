from . import create_app
import os
import dotenv

dotenv.load_dotenv()

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port) 