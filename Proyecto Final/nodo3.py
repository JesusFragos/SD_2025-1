import socket
import threading
import json
import os

# Configuración del nodo
TRACKER_HOST = '10.86.15.245'
TRACKER_PORT = 8081
PEER_HOST = '0.0.0.0'
PEER_PORT = 9091

files = ["img4.jpeg", "img6.jpeg"]
peers = {}  # Diccionario para almacenar información sobre otros peers

# Verificar que los archivos existen en el directorio de trabajo
def verificar_archivos():
    archivos_existentes = []
    for archivo in files:
        if os.path.isfile(archivo):
            archivos_existentes.append(archivo)
        else:
            print(f"Advertencia: {archivo} no existe en el directorio de trabajo")
    return archivos_existentes

# Función para manejar solicitudes de otros nodos
def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode()
        request = json.loads(data)
        
        if request['type'] == 'download':
            file_name = request['file_name']
            print(f"Solicitud de descarga de {file_name} recibida de {addr}")
            if file_name in archivos_existentes:
                with open(file_name, 'rb') as f:
                    while True:
                        file_data = f.read(1024)
                        if not file_data:
                            break
                        conn.sendall(file_data)
                print(f"Enviado {file_name} a {addr}")
            else:
                conn.send(b"Archivo no encontrado")
                print(f"{file_name} no encontrado en este nodo")
        elif request['type'] == 'download_resume':
            file_name = request['file_name']
            offset = request['offset']
            print(f"Solicitud de reanudación de descarga de {file_name} recibida de {addr} desde el offset {offset}")
            if file_name in archivos_existentes:
                with open(file_name, 'rb') as f:
                    f.seek(offset)
                    while True:
                        file_data = f.read(1024)
                        if not file_data:
                            break
                        conn.sendall(file_data)
                print(f"Enviado {file_name} desde el offset {offset} a {addr}")
            else:
                conn.send(b"Archivo no encontrado")
                print(f"{file_name} no encontrado en este nodo")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Función para registrar el nodo en el rastreador
def register_with_tracker():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        request = {
            'type': 'register',
            'peer_id': 'Nodo3',
            'port': PEER_PORT,
            'files': archivos_existentes
        }
        s.send(json.dumps(request).encode())
        response = json.loads(s.recv(1024).decode())
        if response['status'] == 'registered':
            print("Registrado en el rastreador")
        else:
            print("Error al registrar en el rastreador")

# Función para solicitar un archivo a otros nodos
def request_file(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        request = {
            'type': 'request_file',
            'file_name': file_name
        }
        s.send(json.dumps(request).encode())
        response = json.loads(s.recv(1024).decode())
        nodes_with_file = response.get('nodes', {})
        print(f"Nodos con el archivo {file_name}: {nodes_with_file}")
        if nodes_with_file:
            peer_id, peer_info = next(iter(nodes_with_file.items()))
            peers[peer_id] = peer_info
            download_from_peer(peer_id, file_name)  # Descarga desde el primer nodo disponible
        else:
            print("Archivo no encontrado en otros nodos")

# Función para descargar archivo desde otro nodo
def download_from_peer(peer_id, file_name):
    peer_info = peers.get(peer_id)
    if not peer_info:
        print(f"Información del peer {peer_id} no encontrada")
        return

    print(f"Conectando a peer {peer_id} en {peer_info['address']}:{peer_info['port']} para descargar {file_name}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_info['address'], peer_info['port']))
        request = {
            'type': 'download',
            'file_name': file_name
        }
        s.send(json.dumps(request).encode())
        
        with open(file_name, 'wb') as f:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"Archivo {file_name} descargado de {peer_id}")

# Función para reanudar descargas interrumpidas
def resume_download(file_name):
    temp_file = f"{file_name}.part"
    if not os.path.exists(temp_file):
        print(f"No se encontró la descarga interrumpida de {file_name}")
        return

    with open(temp_file, 'rb') as f:
        f.seek(0, os.SEEK_END)
        offset = f.tell()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        request = {
            'type': 'request_file',
            'file_name': file_name
        }
        s.send(json.dumps(request).encode())
        response = json.loads(s.recv(1024).decode())
        nodes_with_file = response.get('nodes', {})
        if nodes_with_file:
            peer_id, peer_info = next(iter(nodes_with_file.items()))
            peers[peer_id] = peer_info
            download_from_peer_resume(peer_id, file_name, offset)
        else:
            print("Archivo no encontrado en otros nodos")

def download_from_peer_resume(peer_id, file_name, offset):
    peer_info = peers.get(peer_id)
    if not peer_info:
        print(f"Información del peer {peer_id} no encontrada")
        return

    print(f"Conectando a peer {peer_id} en {peer_info['address']}:{peer_info['port']} para reanudar {file_name} desde el offset {offset}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_info['address'], peer_info['port']))
        request = {
            'type': 'download_resume',
            'file_name': file_name,
            'offset': offset
        }
        s.send(json.dumps(request).encode())
        with open(f"{file_name}.part", 'ab') as f:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        os.rename(f"{file_name}.part", file_name)
        print(f"Descarga reanudada y archivo {file_name} completado")

# Función para obtener la lista de archivos de cada nodo desde el rastreador
def get_files_from_tracker():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        request = {
            'type': 'get_files'
        }
        s.send(json.dumps(request).encode())
        response = json.loads(s.recv(1024).decode())
        print("Lista de archivos en cada nodo:")
        for peer_id, peer_info in response.items():
            print(f"{peer_id}: {peer_info['files']}")

# Función principal del nodo
def peer():
    # Verificar archivos antes de registrar
    global archivos_existentes
    archivos_existentes = verificar_archivos()
    
    # Iniciar el servidor del nodo
    threading.Thread(target=start_server).start()
    
    # Registrar el nodo en el rastreador
    register_with_tracker()
    
    # Solicitar dos archivos simultáneamente
    files_to_download = ["img3.jpeg", "img5.jpeg"]
    download_threads = []

    for file_name in files_to_download:
        thread = threading.Thread(target=request_file, args=(file_name,))
        thread.start()
        download_threads.append(thread)

    for thread in download_threads:
        thread.join()

    # Obtener la lista de archivos desde el rastreador
    get_files_from_tracker()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((PEER_HOST, PEER_PORT))
        s.listen()
        print(f"Nodo escuchando en {PEER_HOST}:{PEER_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    peer()
