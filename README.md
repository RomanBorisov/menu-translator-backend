# OpenAI Backend for Menu Translator

A Django-based backend service that handles image processing with OpenAI's Vision API for menu translation and analysis.

## Project Structure

```
openai-backend/
├── api/                    # Django app for API endpoints
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py             # URL routing for API endpoints
│   └── views.py            # API view implementations
├── menu_backend/           # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py
├── media/                  # Directory for uploaded media (created at runtime)
├── venv/                   # Virtual environment (not included in repo)
├── .env                    # Environment variables (not included in repo)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore file
├── manage.py               # Django management script
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository (if not already done):
   ```bash
   git clone <repository-url>
   cd openai-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file and replace the placeholder values:
   - `SECRET_KEY`: A secure random string for Django
   - `OPENAI_API_KEY`: Your OpenAI API key

### Running the Server

1. Apply migrations:
   ```bash
   python manage.py migrate
   ```

2. Run the development server:
   ```bash
   python manage.py runserver
   ```

The server will start at http://localhost:8000/

## API Usage

### Process Image Endpoint

- **URL**: `/api/process-image/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Request Body**:
  - `image`: An image file (JPEG, PNG)

#### Example Request (curl):

```bash
curl -X POST \
  -F "image=@/path/to/menu-image.jpg" \
  http://localhost:8000/api/process-image/
```

#### Example Request (Angular):

```typescript
const formData = new FormData();
formData.append('image', imageFile);

this.http.post('http://localhost:8000/api/process-image/', formData)
  .subscribe(
    (response) => {
      console.log('OpenAI response:', response);
      // Handle the response
    },
    (error) => {
      console.error('Error:', error);
      // Handle the error
    }
  );
```

#### Example Response:

```json
{
  "result": "Content returned from OpenAI...",
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 456,
    "total_tokens": 579
  }
}
```

## Security Notes

- The OpenAI API key is stored only on the backend for security.
- CORS settings are configured to allow only specific origins (default: localhost:4200).
- In production, set `DEBUG=False` in the `.env` file and configure proper `ALLOWED_HOSTS` in settings.py.

## Troubleshooting

- **"OpenAI API key is not set"**: Ensure you've set the `OPENAI_API_KEY` in your `.env` file.
- **CORS issues**: Check that your Angular app's domain is listed in the `CORS_ALLOWED_ORIGINS` in settings.py.
- **Image upload failures**: Ensure the image is under 10MB (default limit) and in a supported format. 