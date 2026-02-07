from __future__ import annotations
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any

class RAGService:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self.llm = None
        self.persist_directory = "./faiss_index"
        self.executor = ThreadPoolExecutor(max_workers=3)
        self._initialize()
    
    def _get_llm(self):
        """Get LLM based on configuration"""
        provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("OPENAI_API_KEY not set")
            return ChatOpenAI(
                temperature=0, 
                model_name="gpt-3.5-turbo", 
                openai_api_key=api_key
            )
        
        elif provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "mistral")
            return Ollama(
                base_url=base_url,
                model=model,
                temperature=0,
                timeout=120  # 120 second timeout for slow systems
            )
        
        elif provider == "huggingface":
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
            if not api_key:
                raise Exception("HUGGINGFACE_API_KEY not set")
            return HuggingFaceEndpoint(
                repo_id=model,
                huggingfacehub_api_token=api_key,
                temperature=0.1,
                max_new_tokens=512
            )
        
        else:
            raise Exception(f"Unknown LLM provider: {provider}")
    
    def _get_embeddings(self):
        """Get embeddings based on configuration"""
        provider = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
        
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("OPENAI_API_KEY not set")
            return OpenAIEmbeddings(openai_api_key=api_key)
        
        elif provider == "huggingface":
            model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            return HuggingFaceEmbeddings(model_name=model)
        
        else:
            raise Exception(f"Unknown embedding provider: {provider}")
    
    def _initialize(self):
        """Initialize the RAG service"""
        try:
            # Get embeddings
            self.embeddings = self._get_embeddings()
            print(f"✓ Embeddings initialized: {os.getenv('EMBEDDING_PROVIDER', 'huggingface')}")
            
            # Get LLM
            self.llm = self._get_llm()
            provider = os.getenv("LLM_PROVIDER", "ollama")
            model = os.getenv("OLLAMA_MODEL" if provider == "ollama" else "HUGGINGFACE_MODEL", "mistral")
            print(f"✓ LLM initialized: {provider} ({model})")
            
            # Load existing vectorstore or create new one
            index_file = os.path.join(self.persist_directory, "index.faiss")
            if os.path.exists(index_file):
                self.vectorstore = FAISS.load_local(
                    self.persist_directory,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self._initialize_qa_chain()
                print(f"✓ Loaded existing vector store with documents")
            else:
                # Create empty vectorstore
                self.vectorstore = None
                print("⚠ No documents loaded yet. Upload PDFs to begin.")
            
        except Exception as e:
            print(f"Error initializing RAG service: {e}")
            print("Check your .env file configuration.")
    
    def _initialize_qa_chain(self):
        """Initialize or reinitialize the QA chain"""
        try:
            if not self.llm or not self.vectorstore:
                return
            
            # Create prompt template (simplified for speed)
            prompt = ChatPromptTemplate.from_template("""You are an HOA assistant. Answer based on the context below. Be concise.

Context: {context}

Question: {question}

Answer:""")
            
            # Create retrieval chain using LCEL
            # Reduced from k=4 to k=2 for faster performance
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": 2})
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            self.qa_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            self.retriever = retriever
            
        except Exception as e:
            print(f"Error initializing QA chain: {e}")
    
    def is_initialized(self) -> bool:
        """Check if RAG service is properly initialized"""
        return self.qa_chain is not None
    
    async def index_document(self, file_path: str):
        """Index a PDF document into the vectorstore"""
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            chunks = text_splitter.split_documents(documents)
            
            # Add to vectorstore
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
            else:
                # Create new vectorstore with first documents
                self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            
            # Save vectorstore
            os.makedirs(self.persist_directory, exist_ok=True)
            self.vectorstore.save_local(self.persist_directory)
            
            # Reinitialize QA chain with updated vectorstore
            self._initialize_qa_chain()
            
        except Exception as e:
            raise Exception(f"Error indexing document: {e}")
    
    async def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system with a question"""
        if not self.qa_chain:
            raise Exception("RAG service not initialized. Please upload documents first or check your configuration.")
        
        try:
            start_time = time.time()
            
            # Run blocking operations in thread pool
            loop = asyncio.get_event_loop()
            
            # Get answer from chain (blocking call)
            print(f"[{time.time()-start_time:.1f}s] Processing question: {question[:50]}...")
            
            answer_start = time.time()
            answer = await loop.run_in_executor(
                self.executor,
                lambda: self.qa_chain.invoke(question)
            )
            answer_time = time.time() - answer_start
            print(f"[{time.time()-start_time:.1f}s] Got answer in {answer_time:.1f}s: {answer[:100]}...")
            
            # Get relevant documents for sources (blocking call)
            docs_start = time.time()
            docs = await loop.run_in_executor(
                self.executor,
                lambda: self.retriever.get_relevant_documents(question)
            )
            docs_time = time.time() - docs_start
            print(f"[{time.time()-start_time:.1f}s] Retrieved {len(docs)} documents in {docs_time:.1f}s")
            
            sources = []
            for doc in docs:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                sources.append(f"{os.path.basename(source)} (Page {page + 1})")
            
            total_time = time.time() - start_time
            print(f"[{total_time:.1f}s] Query complete!")
            
            return {
                "answer": answer,
                "sources": list(set(sources))
            }
        except Exception as e:
            print(f"Error in query: {str(e)}")
            raise Exception(f"Error querying RAG system: {e}")
