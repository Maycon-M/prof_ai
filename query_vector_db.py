from src.pipeline import Pipeline

# Configurações do DB vetorial
pdf_path = "historia.pdf"
db_path = "./chroma_db"
collection_name = "pdf_collection"

# Instancia Pipeline sem recriar a coleção (usa get_or_create)
pipeline = Pipeline(pdf_path, db_path=db_path, collection_name=collection_name)

# Leitura de pergunta do usuário
def main():
    question = input("Digite sua pergunta: ")
    # Busca sem recriar ou limpar o banco
    results = pipeline.query_documents(question, n_results=5)

    print(f"\nPergunta: {question}\n")
    for i, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0]), start=1):
        print(f"Resultado {i} (distância {dist}):\n{doc}\n")

if __name__ == "__main__":
    main()
