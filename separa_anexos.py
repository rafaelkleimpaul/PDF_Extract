import os
import shutil

# Diretório principal onde as pastas estão localizadas
diretorio_principal = r"seu_caminho"  # Altere para o caminho correto

# Criando a pasta "Arquivos_email" se não existir
pasta_destino = os.path.join(diretorio_principal, "Arquivos_email")
os.makedirs(pasta_destino, exist_ok=True)

# Percorrendo todas as pastas dentro do diretório principal
for pasta in os.listdir(diretorio_principal):
    caminho_pasta = os.path.join(diretorio_principal, pasta)
    
    # Verifica se é uma pasta
    if os.path.isdir(caminho_pasta):
        for arquivo in os.listdir(caminho_pasta):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)

            # Verifica se é um arquivo e se NÃO tem extensão .txt
            if os.path.isfile(caminho_arquivo) and not arquivo.lower().endswith(".txt"):
                # Move o arquivo para a pasta "Arquivos_email"
                shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
                print(f"Movido: {arquivo}")

print("Processo concluído!")
