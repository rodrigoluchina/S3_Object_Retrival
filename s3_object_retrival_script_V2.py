import boto3
import json
import os
from configparser import ConfigParser
from tkinter import Tk, Label, Entry, Button, messagebox, Frame

# Configurar boto3
s3_client = boto3.client('s3')

# Carregar configurações do arquivo ini
config = ConfigParser()
config.read('s3_config.ini')

bucket_name = config['DEFAULT'].get('BucketName', '')
prefix = config['DEFAULT'].get('Prefix', '')
phone_numbers_to_search = config['DEFAULT'].get('PhoneNumber', '')
local_download_path = config['DEFAULT'].get('LocalDownloadPath', '')

# Garantir que o prefixo termina com "/"
if prefix and not prefix.endswith('/'):
    prefix += '/'

def save_config():
    config['DEFAULT'] = {'BucketName': bucket_name_entry.get(),
                         'Prefix': prefix_entry.get(),
                         'PhoneNumber': phone_numbers_entry.get(),
                         'LocalDownloadPath': local_download_path_entry.get()}
    with open('s3_config.ini', 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo("Configuração", "Configurações salvas com sucesso!")

def download_file(bucket, key, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    file_path = os.path.join(download_path, os.path.basename(key))
    if not os.path.exists(file_path):
        print(f"Downloading {key} to {file_path}")
        s3_client.download_file(bucket, key, file_path)
        return True
    else:
        print(f"File {file_path} already exists. Skipping download.")
        return False

def search_phone_number_in_json(bucket, prefix, phone_numbers):
    paginator = s3_client.get_paginator('list_objects_v2')
    phone_numbers = [number.strip() for number in phone_numbers.split(',')]
    downloaded_files = []
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('_metadata.json'):
                json_object = s3_client.get_object(Bucket=bucket, Key=obj['Key'])
                json_content = json.loads(json_object['Body'].read().decode('utf-8'))
                json_str = json.dumps(json_content)
                
                # Verifica se qualquer um dos números de telefone (últimos 8 dígitos) está presente no JSON
                if any(phone_number[-8:] in json_str for phone_number in phone_numbers):
                    print(f"Phone number found in {obj['Key']}")
                    audio_file_key = obj['Key'].replace('_metadata.json', '')
                    print(f"Corresponding audio file key: {audio_file_key}")
                    try:
                        # Construir o caminho de download local
                        parts = audio_file_key.split('/')
                        year = parts[-5].split('=')[1]
                        month = parts[-4].split('=')[1]
                        day = parts[-3].split('=')[1]
                        matched_phone_number = next(pn for pn in phone_numbers if pn[-8:] in json_str)
                        local_path = os.path.join(local_download_path, matched_phone_number, year, month, day)
                        if download_file(bucket, audio_file_key, local_path):
                            downloaded_files.append(audio_file_key)
                    except Exception as e:
                        print(f"Error downloading {audio_file_key}: {e}")
                        messagebox.showerror("Erro", f"Erro ao baixar {audio_file_key}: {e}")

    if downloaded_files:
        messagebox.showinfo("Download", f"Download concluído com sucesso para {len(downloaded_files)} arquivos!")
    else:
        messagebox.showinfo("Download", "Todos os arquivos já estão armazenados localmente.")

def run_search():
    global bucket_name, prefix, phone_numbers_to_search, local_download_path
    bucket_name = bucket_name_entry.get()
    prefix = prefix_entry.get()
    phone_numbers_to_search = phone_numbers_entry.get()
    local_download_path = local_download_path_entry.get()

    # Garantir que o prefixo termina com "/"
    if prefix and not prefix.endswith('/'):
        prefix += '/'

    search_phone_number_in_json(bucket_name, prefix, phone_numbers_to_search)

# Configurar a interface Tkinter
root = Tk()
root.title("Busca e Download de Arquivos S3")
root.geometry("768x400")

# Lado esquerdo com texto explicativo
left_frame = Frame(root, bg='lightblue', width=100, height=768)
left_frame.pack(side="left", fill="both", expand=True)

left_label = Label(left_frame, text="Como usar a aplicação:\n\n"
                                    "1. Insira o nome do bucket.\n"
                                    "2. Insira o número de telefone.\n"
                                    "3. Insira o caminho local para download.\n\n"
                                    "\n",
                   bg='lightblue', fg='black', justify="left", anchor="w")
left_label.pack(padx=10, pady=10)

# Lado direito com entradas e botões
right_frame = Frame(root, bg='white', width=200, height=300)
right_frame.pack(side="right", fill="both", expand=True)

bucket_name_label = Label(right_frame, text="Nome do Bucket S3:", bg='white')
bucket_name_label.pack(padx=10, pady=5)
bucket_name_entry = Entry(right_frame, width=50)
bucket_name_entry.pack(padx=10, pady=5)
bucket_name_entry.insert(0, bucket_name)

# prefix_label = Label(right_frame, text="Prefix (opcional):", bg='white')
# prefix_label.pack(padx=10, pady=5)
# prefix_entry = Entry(right_frame, width=50)
# prefix_entry.pack(padx=10, pady=5)
# prefix_entry.insert(0, prefix)

phone_numbers_label = Label(right_frame, text="Número de telefone:", bg='white')
phone_numbers_label.pack(padx=10, pady=5)
phone_numbers_entry = Entry(right_frame, width=50)
phone_numbers_entry.pack(padx=10, pady=5)
phone_numbers_entry.insert(0, phone_numbers_to_search.replace('tel:+', ''))

local_download_path_label = Label(right_frame, text="Caminho do Download Local:", bg='white')
local_download_path_label.pack(padx=10, pady=5)
local_download_path_entry = Entry(right_frame, width=50)
local_download_path_entry.pack(padx=10, pady=5)
local_download_path_entry.insert(0, local_download_path)

search_button = Button(right_frame, text="Buscar e Baixar Arquivo", command=run_search, bg='lightblue', relief='flat', borderwidth=1, highlightthickness=0)
search_button.pack(padx=10, pady=20)

save_button = Button(right_frame, text="Salvar Configuração", command=save_config, bg='lightblue', relief='flat', borderwidth=1, highlightthickness=0)
save_button.pack(padx=10, pady=5)

root.mainloop()
