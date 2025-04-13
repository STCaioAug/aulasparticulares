# Automatização de Relatórios por WhatsApp

## Relatório Diário de Aulas

O sistema inclui um recurso para enviar automaticamente relatórios diários de aulas para um número de WhatsApp específico. Isso é útil para manter os coordenadores ou responsáveis informados sobre as aulas programadas para o dia.

## Métodos de Envio

### 1. Envio Manual (via Interface Web)

Acesse a interface web no menu "Notificações" > "Relatório Diário (WhatsApp)" e siga os passos abaixo:

1. Informe o número de WhatsApp (incluindo código do país, ex: +5519XXXXXXXX)
2. Selecione a data desejada (padrão: hoje)
3. Clique em "Gerar Relatório"
4. Use o botão "Abrir WhatsApp" para enviar a mensagem

### 2. Envio Automático (via Script)

O sistema inclui um script Python que pode ser executado manualmente ou agendado para envio automático diário.

#### Executar manualmente:

```bash
python send_daily_whatsapp_report.py
```

#### Opções do script:

- `--dry-run`: Apenas mostra o link do WhatsApp, sem abrir o navegador
- `--phone NÚMERO`: Especifica um número diferente do padrão configurado

#### Exemplo:

```bash
python send_daily_whatsapp_report.py --phone +5519987654321
```

## Configuração para Envio Automático Diário

Para configurar o envio automático diário, você pode usar o `cron` em sistemas Linux/Mac ou o "Agendador de Tarefas" no Windows.

### Exemplo de configuração no Linux (usando cron):

Edite o arquivo de cron:

```bash
crontab -e
```

Adicione uma linha para executar o script diariamente às 7:00 da manhã:

```
0 7 * * * cd /caminho/para/aplicacao && python send_daily_whatsapp_report.py
```

### Personalizando o Número Padrão

Para alterar o número de telefone padrão que recebe os relatórios diários, edite a variável `DEFAULT_PHONE_NUMBER` no arquivo `send_daily_whatsapp_report.py`.

## API para Integração

O sistema também oferece uma API REST para integração com outros sistemas:

```
GET /notifications/auto-daily-report/{phone_number}
```

Esta API retorna um objeto JSON com o link para o WhatsApp e outras informações relevantes.

Exemplo de resposta:

```json
{
  "success": true,
  "message": "Relatório diário gerado com sucesso",
  "report_date": "07/04/2025",
  "whatsapp_link": "https://wa.me/5519987654321?text=..."
}
```

## Formato do Relatório

O relatório diário inclui:
- Título com data e dia da semana
- Lista de aulas agendadas para o dia, incluindo:
  - Horário
  - Nome do aluno
  - Disciplina
  - Tópico (se especificado)
- Mensagem indicando que não há aulas, caso não existam aulas agendadas para o dia
