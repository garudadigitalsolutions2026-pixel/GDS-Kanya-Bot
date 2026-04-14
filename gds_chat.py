import os
# Mandatory: This keeps the 'weight' (the model files) on your D drive
os.environ['SENTENCE_TRANSFORMERS_HOME'] = 'D:/GDS_VectorDB/models'

from vectordb import Memory

# 1. Connect to your existing database file
DB_FILE = 'D:/GDS_VectorDB/gds_permanent_data.db'
memory = Memory(memory_file=DB_FILE)

print("--- 🛰️  Garuda Digital Solutions: Intelligence System Active ---")
print("Type your questions about GDS below. Type 'exit' to quit.\n")

# 2. Start the interactive chat loop
while True:
    query = input("🤔 Ask GDS: ")
    
    # Check if the user wants to stop
    if query.lower() == 'exit':
        print("Closing system. Goodbye!")
        break
    
    # Search the database (pulling the top 2 most relevant matches)
    results = memory.search(query, top_n=2)
    
    if results:
        print("\n💡 GDS AI Search Results:")
        for i, res in enumerate(results):
            # Using .get() ensures we don't crash if an old test entry is found
            category = res['metadata'].get('service', 'General Info')
            print(f"{i+1}. {res['chunk']} [Tag: {category}]")
        print("-" * 40 + "\n")
    else:
        print("❌ I couldn't find any information matching that in the database.\n")