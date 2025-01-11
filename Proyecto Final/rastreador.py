import socket
import threading
import json

# Configuración del rastreador
TRACKER_HOST = '0.0.0.0'
TRACKER_PORT = 8081
peers = {}

# Función para manejar conexiones con nodos
def handle_peer(conn, addr):
    print(f"Conexión establecida con {addr}")
    try:
        data = conn.recv(1024).decode()
        request = json.loads(data)
        
        if request['type'] == 'register':
            peer_id = request['peer_id']
            files = request['files']
            peers[peer_id] = {
                'address': addr[0],
                'port': request['port'],
                'files': files
            }
            conn.send(json.dumps({'status': 'registered'}).encode())
            print(f"Peer registrado: {peer_id} con archivos: {files}")
        
        elif request['type'] == 'request_file':
            file_name = request['file_name']
            nodes_with_file = {
                peer_id: peer_info for peer_id, peer_info in peers.items()
                if file_name in peer_info['files']
            }
            conn.send(json.dumps({'nodes': nodes_with_file}).encode())
            print(f"Solicitud de archivo: {file_name}. Nodos con el archivo: {nodes_with_file}")
        
        elif request['type'] == 'get_files':
            conn.send(json.dumps(peers).encode())
            print(f"Enviando lista de archivos de cada nodo a {addr}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Función principal del rastreador
def tracker():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TRACKER_HOST, TRACKER_PORT))
        s.listen()
        print(f"Rastreador escuchando en {TRACKER_HOST}:{TRACKER_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_peer, args=(conn, addr)).start()

if __name__ == "__main__":
    tracker()
