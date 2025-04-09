# Envio Automático de Relatórios por WhatsApp

Este diretório contém os arquivos necessários para o envio automático de relatórios diários de aulas por WhatsApp.

## Arquivos Principais

- `send_daily_whatsapp_report.py`: Script para envio automático de relatórios diários.
- `docs/automatizacao_whatsapp.md`: Documentação detalhada sobre o recurso.

## Uso Rápido

Para enviar manualmente o relatório diário para o número padrão (+5519993843839):

```bash
python send_daily_whatsapp_report.py
```

Isso irá:
1. Gerar um relatório com as aulas do dia atual
2. Criar um link para o WhatsApp com o relatório já preenchido
3. Abrir o navegador com o link do WhatsApp

Para apenas ver o link sem abrir o navegador:

```bash
python send_daily_whatsapp_report.py --dry-run
```

## Configuração

Para alterar o número de telefone padrão, edite a linha `DEFAULT_PHONE_NUMBER` no arquivo `send_daily_whatsapp_report.py`.

## Documentação

Para uma documentação mais detalhada, consulte o arquivo [docs/automatizacao_whatsapp.md](docs/automatizacao_whatsapp.md).
