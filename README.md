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

## Security Considerations

- Keep your SECRET_KEY secure and never commit it to version control
- Use HTTPS in production
- Regularly update dependencies
- Monitor disk usage for downloaded files
- Implement rate limiting if needed
