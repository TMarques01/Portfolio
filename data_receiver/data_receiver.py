import serial
import json
import time
from datetime import datetime
from pymongo import MongoClient
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ArduinoDataReceiver:
    def __init__(self, com_port='COM5', baud_rate=9600, mongo_uri='mongodb+srv://tiagomarques527:1FEA136wq9Hu3oio@temphum.cpauwro.mongodb.net/?retryWrites=true&w=majority&appName=TempHum', 
                 db_name='TempHum', collection_name='sensor_readings'):
        """
        Inicializa o receptor de dados do Arduino
        
        Args:
            com_port (str): Porta COM do Arduino (default: COM5)
            baud_rate (int): Taxa de transmissão (default: 9600)
            mongo_uri (str): URI de conexão do MongoDB
            db_name (str): Nome da base de dados
            collection_name (str): Nome da coleção
        """
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        
        self.serial_connection = None
        self.mongo_client = None
        self.db = None
        self.collection = None
        
    def connect_serial(self):
        """Conecta à porta serial do Arduino"""
        try:
            self.serial_connection = serial.Serial(self.com_port, self.baud_rate, timeout=1)
            time.sleep(2)  # Aguarda a inicialização da conexão
            logger.info(f"Conectado com sucesso à porta {self.com_port}")
            return True
        except serial.SerialException as e:
            logger.error(f"Erro ao conectar à porta {self.com_port}: {e}")
            return False
    
    def connect_mongodb(self):
        """Conecta ao MongoDB"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.db_name]
            self.collection = self.db[self.collection_name]
            
            # Testa a conexão
            self.mongo_client.admin.command('ping')
            logger.info(f"Conectado com sucesso ao MongoDB - Base de dados: {self.db_name}, Coleção: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao conectar ao MongoDB: {e}")
            return False
    
    def parse_arduino_data(self, raw_data):
        """
        Parse dos dados recebidos do Arduino no formato: temp,hum
        
        Args:
            raw_data (str): Dados em bruto recebidos do Arduino (ex: "25.5,60.3")
            
        Returns:
            dict: Dados parseados
        """
        try:
            data_dict = {
                'timestamp': datetime.now(),
                'raw_data': raw_data.strip()
            }
            
            # Remove espaços e quebras de linha
            clean_data = raw_data.strip()
            
            # Verifica se os dados contêm vírgula (formato temp,hum)
            if ',' in clean_data:
                values = clean_data.split(',')
                
                # Verifica se temos exatamente 2 valores
                if len(values) == 2:
                    try:
                        # Converte para float e atribui aos campos corretos
                        data_dict['temperature'] = float(values[0].strip())
                        data_dict['humidity'] = float(values[1].strip())
                        
                        logger.info(f"Temperatura: {data_dict['temperature']}°C, Humidade: {data_dict['humidity']}%")
                        
                    except ValueError as e:
                        logger.error(f"Erro ao converter valores para números: {e}")
                        # Guarda como string se não conseguir converter
                        data_dict['temperature_raw'] = values[0].strip()
                        data_dict['humidity_raw'] = values[1].strip()
                else:
                    logger.warning(f"Formato inesperado - esperado 2 valores separados por vírgula, recebido {len(values)}")
                    data_dict['parse_warning'] = f"Formato inesperado - {len(values)} valores"
            
            # Se não tem vírgula, tenta interpretar como valor único
            else:
                try:
                    data_dict['single_value'] = float(clean_data)
                except ValueError:
                    data_dict['single_value'] = clean_data
                    
            return data_dict
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse dos dados: {e}")
            return {
                'timestamp': datetime.now(),
                'raw_data': raw_data.strip(),
                'parse_error': str(e)
            }  
              
    def save_to_mongodb(self, data):
        """
        Salva os dados no MongoDB
        
        Args:
            data (dict): Dados a serem salvos
        """
        try:
            result = self.collection.insert_one(data)
            logger.info(f"Dados salvos no MongoDB com ID: {result.inserted_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar no MongoDB: {e}")
            return False
    
    def run(self):
        """Loop principal para receber e processar dados"""
        if not self.connect_serial():
            logger.error("Não foi possível conectar à porta serial")
            return
        
        if not self.connect_mongodb():
            logger.error("Não foi possível conectar ao MongoDB")
            return
        
        logger.info("Iniciando receção de dados... (Pressione Ctrl+C para parar)")
        
        try:
            while True:
                if self.serial_connection.in_waiting > 0:
                    # Lê uma linha de dados
                    raw_data = self.serial_connection.readline().decode('utf-8', errors='ignore')
                    
                    if raw_data.strip():  # Se há dados válidos
                        logger.info(f"Dados recebidos: {raw_data.strip()}")
                        
                        # Parse dos dados
                        parsed_data = self.parse_arduino_data(raw_data)
                        
                        # Salva no MongoDB
                        self.save_to_mongodb(parsed_data)
                
                time.sleep(3)  # Pequena pausa para não sobrecarregar o CPU
                
        except KeyboardInterrupt:
            logger.info("Receção de dados interrompida pelo utilizador")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpa as conexões"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info("Conexão serial fechada")
        
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("Conexão MongoDB fechada")

def main():
    # Configurações - ajuste conforme necessário
    receiver = ArduinoDataReceiver(
        com_port='COM5',
        baud_rate=9600,  # Ajuste conforme a configuração do seu Arduino
        mongo_uri='mongodb+srv://tiagomarques527:1FEA136wq9Hu3oio@temphum.cpauwro.mongodb.net/?retryWrites=true&w=majority&appName=TempHum',  # Ajuste se necessário
        db_name='TempHum',
        collection_name='sensor_readings'
    )
    
    receiver.run()

if __name__ == "__main__":
    main()