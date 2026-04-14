import os
import fitz  # PyMuPDF for PDF processing
from vectordb import Memory

# 1. Environment and Storage Setup
# Redirects AI models and database to D: drive for GDS
os.environ['SENTENCE_TRANSFORMERS_HOME'] = 'D:/GDS_VectorDB/models'
DB_FILE = 'D:/GDS_VectorDB/gds_permanent_data.db'

# Initialize Memory
# Note: This uses the hotfixed 'Embedder' class we created earlier
memory = Memory(memory_file=DB_FILE)

# 2. Database Functions
def add_to_database(text_list, metadata_list):
    """Saves text and metadata to the permanent storage on D: drive."""
    memory.save(text_list, metadata_list)
    print(f"✅ Successfully saved {len(text_list)} entries.")

def search_database(query, top_n=3):
    """Searches the database and returns the top relevant results."""
    return memory.search(query, top_n=top_n)

def ingest_pdf(pdf_path):
    """Extracts text from a PDF file and indexes it into the VectorDB."""
    print(f"📂 Processing PDF: {pdf_path}")
    try:
        doc = fitz.open(pdf_path)
        content_chunks = []
        metadata_chunks = []
        
        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                # We save each page as a separate searchable chunk
                content_chunks.append(text)
                metadata_chunks.append({"source": pdf_path, "page": i + 1, "type": "pdf"})
        
        if content_chunks:
            add_to_database(content_chunks, metadata_chunks)
            print(f"📄 Indexed {len(content_chunks)} pages from {pdf_path} into GDS database.")
        else:
            print(f"⚠️ No readable text found in {pdf_path}.")
            
    except Exception as e:
        print(f"❌ Failed to ingest PDF: {e}")

# 3. Execution Controller
if __name__ == "__main__":
    print(f"🛰️  Garuda Digital Solutions Storage Active")
    
    # TO INGEST A PDF: Uncomment the line below and change the filename
    # ingest_pdf("D:/GDS_VectorDB/your_document.pdf")
    
    # Search Test
    query = input("\n🔍 Query the GDS knowledge base: ")
    if query:
        results = search_database(query)
        print("\n💡 AI Search Results:")
        for i, res in enumerate(results):
            source = res['metadata'].get('source', 'Manual Entry')
            page = res['metadata'].get('page', 'N/A')
            print(f"{i+1}. {res['chunk'][:300]}... \n   [Source: {source} | Page: {page}]")
            print("-" * 30)