# 🛡️ Secure Network Automation (O&M Workflow)

Esta es una Prueba de Concepto (PoC) técnica diseñada para automatizar la extracción de copias de seguridad de red y la auditoría de equipos en infraestructuras de misión crítica.

## 🎯 El Desafío Operativo
En entornos corporativos con cientos de nodos (routers, switches, centralitas), las comprobaciones manuales de red son ineficientes y propensas a errores. Un proceso de auditoría y backup puede demorarse semanas. 

El objetivo de esta arquitectura es **reducir los tiempos de Operación y Mantenimiento (O&M) a menos de 2 horas**, garantizando una trazabilidad absoluta.

## ⚙️ Arquitectura del Flujo de Automatización
La solución híbrida se fundamenta en dos pilares:

1. **Python (El Motor de Ejecución):**
   - Utiliza librerías de automatización SSH (`netmiko`) para acceder masivamente al inventario IT.
   - **Tolerancia a fallos:** Se implementa una estructura estricta de *Try-Catch*. Si un equipo está caído o tiene las credenciales rotadas, el script aísla la excepción y **continúa con el resto de la red** sin interrumpir el proceso global.
   - Todo se registra mediante el módulo `logging` para facilitar posibles análisis forenses.

2. **n8n (Orquestación y Respuesta Activa):**
   - En lugar de revisar logs manualmente, el script de Python integra **Webhooks** conectados a un servidor n8n.
   - Cuando se captura una excepción crítica (ej. Timeout en un nodo *Core*), Python lanza un POST request a n8n.
   - El flujo en n8n recibe la alerta y puede derivarla de forma inteligente (Slack, creación de ticket en Jira, aviso por email) al equipo de guardia correspondiente (Soporte 24x7).

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3
* **Conectividad:** SSH (Netmiko / SecureCRT concept)
* **Gestión de APIs:** Requests (Webhooks)
* **Orquestación:** n8n (Node-based workflow automation)

---
*Nota de Seguridad: Este repositorio contiene código estructural y de simulación. Se han omitido IPs, credenciales y topologías reales en cumplimiento de las políticas de confidencialidad.*
