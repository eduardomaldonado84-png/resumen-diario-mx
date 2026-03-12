import requests
import os
import urllib.parse

def obtener_datos():
    # 1. TIPO DE CAMBIO (Banxico)
    # Metodología: Extracción del indicador SF43718 (Dólar FIX)
    token_bx = os.getenv("BANXICO_TOKEN")
    url_bx = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token={token_bx}"
    
    try:
        res_bx = requests.get(url_bx).json()
        serie = res_bx['bmx']['series'][0]['datos'][0]
        tipo_cambio = f"${serie['dato']}"
        fecha_tc = serie['fecha']
    except Exception as e:
        tipo_cambio, fecha_tc = "No disponible", "N/A"

    # 2. NOTICIAS (NewsAPI)
    # Filtro: Solo negocios y noticias relevantes de México
    news_key = os.getenv("NEWS_KEY")
    url_news = f"https://newsapi.org/v2/top-headlines?country=mx&category=business&pageSize=3&apiKey={news_key}"
    
    resumen_noticias = ""
    try:
        res_n = requests.get(url_news).json()
        for art in res_n.get('articles', []):
            titulo = art['title'].split(' - ')[0] # Limpieza: quita el nombre del medio al final
            resumen_noticias += f"🔹 {titulo}\n"
    except:
        resumen_noticias = "No se pudieron cargar noticias hoy."

    # 3. CONSTRUCCIÓN DEL MENSAJE (Markdown)
    mensaje = (
        f"🇲🇽 *REPORTE DIARIO MÉXICO*\n\n"
        f"💰 *Tipo de Cambio:* {tipo_cambio} MXN\n"
        f"📅 *Datos al:* {fecha_tc}\n\n"
        f"📰 *NOTICIAS DE NEGOCIOS:*\n"
        f"{resumen_noticias}\n"
        f"📈 _Generado automáticamente_"
    )
    return mensaje

def enviar_telegram(texto):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': texto,
        'parse_mode': 'Markdown'
    }
    
    r = requests.post(url, data=payload)
    return r.json()

if __name__ == "__main__":
    contenido = obtener_datos()
    enviar_telegram(contenido)
