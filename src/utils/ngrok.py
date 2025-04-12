import requests
import time
import logging

logger = logging.getLogger(__name__)

def get_ngrok_url():
    """Получить публичный URL от ngrok"""
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            response = requests.get('http://ngrok:4040/api/tunnels')
            data = response.json()
            
            if 'tunnels' in data and len(data['tunnels']) > 0:
                public_url = data['tunnels'][0]['public_url']
                logger.info(f"Получен публичный URL от ngrok: {public_url}")
                return public_url
                
        except Exception as e:
            logger.warning(f"Попытка {attempt + 1}/{max_retries} получить URL от ngrok не удалась: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                
    raise Exception("Не удалось получить публичный URL от ngrok") 