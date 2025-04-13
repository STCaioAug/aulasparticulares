#!/usr/bin/env python3
"""
Script para enviar o relatório diário por WhatsApp.
Este script pode ser agendado para execução diária usando cron ou outro agendador.

Uso: python send_daily_whatsapp_report.py [--dry-run]
Opções:
  --dry-run    Mostra o link WhatsApp sem abrir o navegador

Exemplo de configuração cron (executa todos os dias às 7:00 da manhã):
0 7 * * * cd /caminho/para/app && python send_daily_whatsapp_report.py
"""

import os
import sys
import argparse
import requests
import webbrowser
from datetime import datetime

# Número de telefone para receber os relatórios diários
DEFAULT_PHONE_NUMBER = "+5519993843839"  # Número fornecido pelo usuário

def send_daily_report(phone_number=DEFAULT_PHONE_NUMBER, dry_run=False):
    """
    Envia o relatório diário para o número de telefone especificado.
    
    Args:
        phone_number (str): Número de telefone para receber o relatório
        dry_run (bool): Se True, apenas mostra o link sem abri-lo
        
    Returns:
        bool: True se o relatório foi enviado com sucesso, False caso contrário
    """
    # URL da API local para gerar o relatório diário
    url = f"http://localhost:5000/notifications/auto-daily-report/{phone_number}"
    
    try:
        # Envia a requisição para a API
        response = requests.get(url)
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                whatsapp_link = data.get('whatsapp_link')
                report_date = data.get('report_date')
                
                print(f"Relatório diário para {report_date} gerado com sucesso.")
                print(f"Link WhatsApp: {whatsapp_link}")
                
                # Abre o link no navegador padrão se não for dry-run
                if not dry_run:
                    print("Abrindo WhatsApp no navegador...")
                    webbrowser.open(whatsapp_link)
                
                return True
            else:
                print(f"Erro ao gerar relatório: {data.get('error')}")
                return False
        else:
            print(f"Erro na requisição: Status {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Erro ao enviar relatório diário: {e}")
        return False

def main():
    # Configurar analisador de argumentos
    parser = argparse.ArgumentParser(description='Enviar relatório diário por WhatsApp')
    parser.add_argument('--dry-run', action='store_true', 
                        help='Mostra o link WhatsApp sem abrir o navegador')
    parser.add_argument('--phone', type=str, default=DEFAULT_PHONE_NUMBER,
                        help=f'Número de telefone para receber o relatório (padrão: {DEFAULT_PHONE_NUMBER})')
    
    args = parser.parse_args()
    
    # Registrar início da execução
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando envio do relatório diário...")
    
    # Enviar o relatório
    success = send_daily_report(args.phone, args.dry_run)
    
    # Registrar resultado
    if success:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Relatório enviado com sucesso!")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Falha ao enviar relatório.")
        sys.exit(1)

if __name__ == "__main__":
    main()