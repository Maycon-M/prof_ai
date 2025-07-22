from src.pipeline import Pipeline
import os

# Caminho do PDF e configuração do banco
pdf_path = "historia.pdf"
db_path = "./chroma_db"
collection_name = "pdf_collection"

if __name__ == "__main__":
    # Limpa banco anterior, se existir
    if os.path.exists(db_path):
        import shutil
        shutil.rmtree(db_path)
        print(f"Banco anterior removido: {db_path}")

    # Cria e popula o banco vetorial
    pipeline = Pipeline(pdf_path, db_path=db_path, collection_name=collection_name)
    pipeline.run()
    print(f"Banco vetorial criado em '{db_path}' com a coleção '{collection_name}'.")
