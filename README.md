# HOA Bylaws Lookup Application

A modern web application that helps homeowners easily lookup HOA bylaws and submit requests for home modifications using RAG (Retrieval-Augmented Generation) technology.

## Features

### 🔍 Ask Questions
- Natural language search through HOA bylaws
- Powered by OpenAI and LangChain RAG technology
- Instant answers with source citations
- Example questions to get started

### 📝 Submit Requests
- Easy-to-use form for home modification requests
- Multiple change types supported (painting, landscaping, fencing, etc.)
- Automatic request ID generation
- Email confirmation

### 📄 Document Management
- Upload PDF bylaws documents via hidden admin panel
- Automatic indexing using vector embeddings
- Semantic search across all documents
- **Admin Access:** Navigate to `/admin` (not linked in main UI)

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - RAG orchestration
- **OpenAI / Ollama / HuggingFace** - LLM providers (your choice!)
- **FAISS** - Vector database for similarity search
- **PyPDF** - PDF document processing

**🆓 FREE Option:** Use Ollama with Mistral for completely free, local operation! See OLLAMA_SETUP.md

### Frontend
- **React** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **CSS3** - Modern styling

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- **OpenAI API key** OR **Ollama** (for local/free models like Mistral)

### Backend Setup

1. Navigate to backend directory:
```bash
cd HOA-Bylaws-App/backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your AI provider configuration to `.env`:

**Option A: OpenAI (Cloud, Paid)**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_actual_api_key_here
EMBEDDING_PROVIDER=openai
```

**Option B: Ollama + Mistral (Local, Free)** ⭐ Recommended for privacy
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral
EMBEDDING_PROVIDER=huggingface
```
Then install Ollama and Mistral - see **OLLAMA_SETUP.md** for details!

**Option C: HuggingFace (Cloud, Free tier available)**
```bash
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=your_hf_token_here
EMBEDDING_PROVIDER=huggingface
```

6. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd HOA-Bylaws-App/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (optional):
```bash
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Usage

### Uploading Bylaws Documents

Use the API endpoint to upload PDF documents:

```bash
curl -X POST "http://localhost:8000/api/upload-bylaws" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/bylaws.pdf"
```

Or use a tool like Postman to upload files via the API.

### Asking Questions

1. Open the app in your browser
2. Navigate to "Ask Questions"
3. Type your question or click an example
4. Receive instant answers with source citations

### Submitting Requests

1. Click "Submit Request" in the navigation
2. Fill out the form with:
   - Your name and email
   - Property address
   - Type of change
   - Detailed description
   - Urgency level
3. Submit and receive a confirmation request ID

## Admin Panel

A hidden admin interface for document management is available at:
```
http://localhost:3000/admin
```

**Features:**
- Upload PDF bylaws for indexing
- Real-time upload status
- File validation
- ⚠️ **Note:** No authentication in development mode. See `ADMIN.md` for security recommendations.

See **[ADMIN.md](ADMIN.md)** for complete admin documentation.

## API Endpoints

### GET /
Health check endpoint

### POST /api/ask
Ask a question about HOA bylaws
```json
{
  "question": "Can I paint my house?"
}
```

### POST /api/upload-bylaws
Upload a PDF document (multipart/form-data)

### POST /api/submit-request
Submit a home modification request
```json
{
  "homeowner_name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main St",
  "change_type": "Exterior Painting",
  "description": "Paint house blue",
  "urgency": "normal"
}
```

### GET /api/health
Check service health and RAG initialization status

## Project Structure

```
HOA-Bylaws-App/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag_service.py       # RAG implementation
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   ├── documents/           # Uploaded PDF files
│   ├── requests/            # Submitted requests (JSON)
│   └── faiss_index/         # Vector database
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── AskQuestion.js
│   │   │   ├── AskQuestion.css
│   │   │   ├── SubmitRequest.js
│   │   │   └── SubmitRequest.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## Development

### Adding New Features

The application is designed to be extensible:

- **Backend**: Add new endpoints in `main.py`
- **Frontend**: Create new components in `src/components/`
- **RAG**: Modify prompts and retrieval logic in `rag_service.py`

### Database Integration

Currently, requests are saved as JSON files. For production:

1. Install a database (PostgreSQL, MongoDB, etc.)
2. Add database connection to backend
3. Update request submission endpoints
4. Add admin dashboard for reviewing requests

## Troubleshooting

### Backend Issues

**Error: "OPENAI_API_KEY not set"**
- Ensure `.env` file exists with valid API key
- Restart the backend server after updating `.env`

**Error: "Module not found"**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Port 3000 already in use**
- Change port: `PORT=3001 npm start`

**CORS errors**
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`

## Security Considerations

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- Implement authentication for production use
- Validate and sanitize all user inputs
- Use HTTPS in production

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Admin dashboard for request management
- [ ] Email notifications
- [ ] Request status tracking
- [ ] Document version control
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Request approval workflow

## License

MIT License - Feel free to use and modify for your needs.

## Support

For issues or questions, please open an issue on the project repository.
