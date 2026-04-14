import os
# Ensures your C: drive stays empty
os.environ['SENTENCE_TRANSFORMERS_HOME'] = 'D:/GDS_VectorDB/models'

from vectordb import Memory

print("🚀 Starting GDS Vector Engine...")

try:
    # No extra arguments - we handle the model inside embedding.py now
    memory = Memory() 
    
    # Test saving
    memory.save(["Garuda Digital Solutions is officially live!"], [{"status": "victory"}])
    print("✅ Success: Data saved to D drive!")

    # Test searching
    results = memory.search("Is GDS live?", top_n=1)
    print(f"🔍 Result: {results[0]['chunk']}")
    print("\n✨ Mission Accomplished. You are ready to build.")

except Exception as e:
    print(f"❌ Error: {e}")