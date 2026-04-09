import logging
import requests
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Configuración de Logging para auditoría de O&M
logging.basicConfig(
    filename='network_backup_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Webhook simulado de n8n para alertas críticas de infraestructura
N8N_WEBHOOK_URL = "https://n8n.tudominio.com/webhook/alerta-backup-critica"

def trigger_n8n_alert(device_ip, error_message):
    """Orquesta una alerta automatizada a través de n8n si un nodo falla."""
    payload = {"device": device_ip, "error": str(error_message)}
    try:
        # Timeout corto para no bloquear el flujo principal
        requests.post(N8N_WEBHOOK_URL, json=payload, timeout=3)
        logging.info(f"[ALERTA n8n ENVIADA] Fallo notificado para el equipo {device_ip}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[ERROR WEBHOOK] Fallo al contactar con la API de n8n: {e}")

def execute_backup_job(device):
    """Conecta al dispositivo, extrae la configuración y gestiona la resiliencia."""
    device_ip = device.get('ip')
    
    try:
        logging.info(f"[INICIO O&M] Iniciando conexión a {device_ip}...")
        
        # Conexión SSH simulada mediante Netmiko (Ejemplo para Cisco IOS)
        with ConnectHandler(**device) as net_connect:
            running_config = net_connect.send_command("show running-config")
            
            # Persistencia de la copia de seguridad
            filename = f"backup_config_{device_ip}.cfg"
            with open(filename, 'w') as f:
                f.write(running_config)
                
        logging.info(f"[ÉXITO] Backup validado y completado para {device_ip}")

    # Gestión granular de excepciones para evitar la ruptura del bucle principal
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        logging.error(f"[ERROR CRÍTICO] Fallo de conexión o credenciales en {device_ip}: {e}")
        trigger_n8n_alert(device_ip, "Timeout SSH o Auth Failed")
        
    except Exception as e:
        logging.error(f"[ERROR SISTEMA] Excepción no controlada en {device_ip}: {e}")
        trigger_n8n_alert(device_ip, f"Excepción general: {e}")

if __name__ == "__main__":
    # Inventario simulado (Los datos reales se extraen de una CMDB en producción)
    cmdb_inventory = [
        {'device_type': 'cisco_ios', 'ip': '192.168.10.1', 'username': 'admin_oam', 'password': 'SimulatedPassword1!'},
        {'device_type': 'cisco_ios', 'ip': '192.168.10.2', 'username': 'admin_oam', 'password': 'SimulatedPassword1!'},
        # Añadir más nodos
    ]

    logging.info("=== INICIANDO FLUJO DE AUTOMATIZACIÓN DE BACKUPS ===")
    for node in cmdb_inventory:
        execute_backup_job(node)
    logging.info("=== FLUJO DE AUTOMATIZACIÓN FINALIZADO ===")
