# YouTube to MP3 Converter

A Django web application that converts YouTube videos to MP3 format.

## Features

- Convert YouTube videos to MP3 format
- Modern, responsive UI using Tailwind CSS
- Error handling and loading states
- Production-ready configuration

## Prerequisites

- Python 3.9 or higher
- FFmpeg installed on your system
- Git (for version control)

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/JaponBaligi/ytmp3.git
   cd ytmp3
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your settings:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## FFmpeg Installation

### Windows
1. Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/
2. Extract the contents to a directory
3. Add the `bin` directory to your system's PATH

### Linux
```bash
sudo apt update
sudo apt install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

## Deployment to PythonAnywhere

1. Create a PythonAnywhere account
2. Upload your code to PythonAnywhere
3. Create a virtual environment and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 ytmp3env
   pip install -r requirements.txt
   ```
4. Configure your web app in PythonAnywhere:
   - Set the virtual environment path
   - Set the WSGI configuration file
   - Configure static files
5. Update the `.env` file with production settings:
   ```
   DEBUG=False
   SECRET_KEY=your-secure-secret-key
   ALLOWED_HOSTS=your-username.pythonanywhere.com
   ```
6. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
7. Reload your web app

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security Considerations

- Keep your SECRET_KEY secure and never commit it to version control
- Use HTTPS in production
- Regularly update dependencies
- Monitor disk usage for downloaded files
- Implement rate limiting if needed

## License

MIT License 