import os
import re
import extract_msg

diretorio_msg = f'seu_caminho'  # Defina aqui o caminho da pasta com os arquivos .msg
diretorio_destino = f'seu_caminho'  # Defina aqui o caminho da pasta onde os arquivos extraídos serão salvos

def sanitizar_nome(nome, max_length=100):
    """Remove caracteres inválidos para nome de pastas no Windows e limita o tamanho."""
    if not nome:
        return "arquivo_sem_nome"
    nome = re.sub(r'[<>:"/\\|?*]', '_', nome)  # Substitui caracteres inválidos
    nome = re.sub(r'\s+', ' ', nome).strip()  # Remove espaços extras
    nome = nome.replace('\\', '_')  # Substitui barras invertidas que podem vir no assunto
    return nome[:max_length]  # Limita o tamanho do nome

def processar_arquivos_msg(diretorio_origem, diretorio_destino):
    os.makedirs(diretorio_destino, exist_ok=True)
    
    for arquivo in os.listdir(diretorio_origem):
        if arquivo.endswith(".msg"):
            caminho_arquivo = os.path.join(diretorio_origem, arquivo)
            msg = extract_msg.Message(caminho_arquivo)
            
            # Pegando o assunto do e-mail e sanitizando o nome da pasta
            assunto = sanitizar_nome(msg.subject.strip())
            pasta_destino = os.path.join(diretorio_destino, assunto)
            
            # Verificando se a pasta já existe, se não, cria
            try:
                os.makedirs(pasta_destino, exist_ok=True)
            except Exception as e:
                print(f"Erro ao criar pasta {pasta_destino}: {e}")
                continue
            
            # Salvando o corpo do e-mail em um arquivo TXT
            corpo_email = msg.body if msg.body else "(Corpo do e-mail vazio)"
            caminho_corpo = os.path.join(pasta_destino, "corpo_email.txt")
            try:
                with open(caminho_corpo, "w", encoding="utf-8") as f:
                    f.write(corpo_email)
            except Exception as e:
                print(f"Erro ao salvar corpo do e-mail em {caminho_corpo}: {e}")
                continue
            
            # Extraindo anexos
            for anexo in msg.attachments:
                nome_anexo = sanitizar_nome(anexo.longFilename, max_length=50)
                caminho_anexo = os.path.join(pasta_destino, nome_anexo)
                try:
                    with open(caminho_anexo, "wb") as f:
                        f.write(anexo.data)
                except Exception as e:
                    print(f"Erro ao salvar anexo {nome_anexo}: {e}")
                    continue
            
            print(f"Processado: {arquivo} -> {pasta_destino}")

if __name__ == "__main__":
    if os.path.exists(diretorio_msg):
        processar_arquivos_msg(diretorio_msg, diretorio_destino)
        print("Processamento concluído!")
    else:
        print("Diretório de origem não encontrado!")