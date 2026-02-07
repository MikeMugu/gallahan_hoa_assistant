# Admin Panel

## Accessing the Admin Panel

The admin panel is a hidden page for uploading and indexing PDF documents. It is not linked in the main navigation for security purposes.

### URL
Navigate directly to: **http://localhost:3000/admin**

## Features

### Document Upload
- Upload PDF documents containing HOA bylaws
- Automatic indexing for the Q&A system
- Real-time upload status and feedback
- File validation (PDF only)

### How to Use

1. **Navigate to Admin Page**
   ```
   http://localhost:3000/admin
   ```

2. **Select a PDF File**
   - Click "Choose PDF File" button
   - Select a PDF document from your computer
   - File information will be displayed

3. **Upload & Index**
   - Click "📤 Upload & Index" button
   - Wait for the indexing process to complete
   - Success/error message will appear

4. **Upload Additional Documents**
   - Repeat the process for more documents
   - All documents are indexed together
   - The system maintains all previously uploaded documents

## Security Considerations

### Current Setup (Development)
- ⚠️ No authentication required
- Hidden from main navigation
- Direct URL access only

### Production Recommendations
1. **Add Authentication**
   - Implement login system
   - Use JWT tokens or session management
   - Require admin credentials

2. **Add Authorization**
   - Role-based access control (RBAC)
   - Separate admin and user roles
   - Audit logging for uploads

3. **Additional Security**
   - Rate limiting on uploads
   - File size restrictions
   - Virus scanning for uploaded files
   - HTTPS only in production

## Example: Adding Authentication

### Simple Password Protection (Backend)

```python
# main.py
from fastapi import HTTPException, Depends, Header

ADMIN_TOKEN = "your-secret-admin-token"

def verify_admin(authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.post("/api/upload-bylaws", dependencies=[Depends(verify_admin)])
async def upload_bylaws(file: UploadFile = File(...)):
    # ... existing code ...
```

### Frontend Update

```javascript
// Admin.js
const response = await axios.post(
  'http://localhost:8000/api/upload-bylaws',
  formData,
  {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': 'Bearer your-secret-admin-token'
    },
  }
);
```

## File Requirements

### Supported Formats
- ✅ PDF only

### Size Limits
- Default: 10MB (configurable in backend)
- Large documents may take longer to index

### Content Guidelines
- Text-based PDFs work best
- Scanned images may require OCR
- Clear formatting improves indexing quality

## Troubleshooting

### "Error uploading document"
- Check backend is running on port 8000
- Verify .env file has required API keys (or Ollama is running)
- Ensure file is a valid PDF

### "No such file or directory"
- ✅ **Fixed** - Backend now automatically creates directories
- If manually needed: `mkdir documents` in backend folder

### "Connection refused"
- Start the backend: `python main.py`
- Check port 8000 is available
- Verify CORS settings allow localhost:3000

### Slow Upload/Indexing
- Normal for large documents
- Indexing happens on upload
- First upload may download embedding models (1-2 minutes)

### Need More Help?
See **UPLOAD_TROUBLESHOOTING.md** for detailed troubleshooting steps.

## Maintenance

### Managing Documents
Currently, there's no UI for:
- Listing uploaded documents
- Deleting documents
- Viewing document details

### Manual Management
Documents are stored in:
```
backend/documents/        # Original PDFs
backend/faiss_index/      # Vector database
```

To clear all documents:
```powershell
cd C:\_Source\HOA-Bylaws-App\backend
Remove-Item documents\*.pdf
Remove-Item faiss_index\* -Recurse
```

## Future Enhancements

### Planned Features
- [ ] Document list/management UI
- [ ] Delete individual documents
- [ ] Document versioning
- [ ] Search within specific documents
- [ ] Document metadata (upload date, uploader, etc.)
- [ ] Bulk upload support
- [ ] Progress indicators for large files
- [ ] Admin dashboard with statistics

### Security Enhancements
- [ ] User authentication
- [ ] Role-based access control
- [ ] Upload activity logs
- [ ] IP whitelist
- [ ] Two-factor authentication

## API Endpoint

### POST /api/upload-bylaws

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file)

**Response (Success):**
```json
{
  "message": "Document processed successfully",
  "filename": "bylaws_2026.pdf",
  "chunks": 45
}
```

**Response (Error):**
```json
{
  "detail": "Error message here"
}
```

## Best Practices

### For Administrators
1. **Organize Documents**
   - Use clear, descriptive filenames
   - Include dates in filenames (e.g., bylaws_2026.pdf)
   - Keep originals backed up separately

2. **Regular Updates**
   - Re-upload when bylaws change
   - Remove outdated documents
   - Test Q&A system after uploads

3. **Monitor Performance**
   - Check index size regularly
   - Watch for slow queries
   - Optimize if needed

### For Developers
1. **Testing**
   - Test with various PDF formats
   - Verify error handling
   - Check upload limits

2. **Security**
   - Never commit admin tokens
   - Use environment variables
   - Implement proper authentication

3. **Deployment**
   - Add authentication before production
   - Configure file size limits
   - Set up monitoring/logging

---

**Admin URL:** http://localhost:3000/admin  
**Access:** Direct navigation only (not linked in main app)
