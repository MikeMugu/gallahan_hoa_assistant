import asyncio
from dotenv import load_dotenv
from rag_service import RAGService
import os

load_dotenv()

async def reindex_documents():
    """Re-index all documents in the documents folder"""
    print("Initializing RAG Service with OpenAI embeddings...")
    rag = RAGService()
    
    docs_dir = "documents"
    pdf_files = [f for f in os.listdir(docs_dir) if f.endswith('.pdf')]
    
    print(f"\nFound {len(pdf_files)} PDF file(s) to index:")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    print("\nIndexing documents...")
    for pdf in pdf_files:
        file_path = os.path.join(docs_dir, pdf)
        print(f"\nIndexing {pdf}...")
        try:
            await rag.index_document(file_path)
            print(f"✓ Successfully indexed {pdf}")
        except Exception as e:
            print(f"✗ Error indexing {pdf}: {e}")
    
    print("\n" + "="*50)
    print("Re-indexing complete!")
    print("="*50)
    
    # Test a query
    print("\nTesting query...")
    try:
        result = await rag.query("Am I allowed to install solar panels?")
        print("✓ Query successful!")
        print(f"\nAnswer: {result['answer']}")
        print(f"\nSources: {result['sources']}")
    except Exception as e:
        print(f"✗ Query failed: {e}")

if __name__ == "__main__":
    asyncio.run(reindex_documents())
