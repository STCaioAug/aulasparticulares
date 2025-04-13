# Aulas Particulares Caio

Um sistema de gerenciamento de aulas particulares construído com Flask, otimizado para deploy no GitHub e Render.com.

## Funcionalidades

- Dashboard com agenda e estatísticas
- Gerenciamento de alunos
- Gerenciamento de responsáveis
- Agendamento de aulas
- Controle de pagamentos
- Notificações por WhatsApp
- Geração de relatórios

## Estrutura do Projeto

```
.
├── app.py           # Inicialização do Flask e configuração do banco de dados
├── main.py          # Ponto de entrada para a aplicação
├── models.py        # Modelos de dados SQLAlchemy
├── routes.py        # Rotas e funções de visualização
├── static/          # Arquivos estáticos (CSS, JS, imagens)
├── templates/       # Templates HTML usando Jinja2
│   └── forms/       # Templates de formulários
├── utils/           # Utilitários auxiliares
│   ├── reports.py   # Geração de relatórios
│   ├── sms.py       # Integração com SMS
│   └── whatsapp.py  # Integração com WhatsApp
└── scripts/         # Scripts auxiliares
```

## Como Executar Localmente

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/aulas-particulares-caio.git
   cd aulas-particulares-caio
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   python app.py
   ```

4. Acesse http://localhost:5000 no seu navegador

## Deploy no Render.com

Este projeto está configurado para implantação fácil no [Render.com](https://render.com):

1. Crie uma conta no Render.com
2. Conecte seu repositório GitHub
3. Crie um novo Web Service 
4. Selecione o repositório e use a configuração automática (o `render.yaml` já está configurado)
5. Clique em "Create Web Service"

O deploy será feito automaticamente e a aplicação estará disponível em um URL fornecido pelo Render.

## Variáveis de Ambiente

- `DATABASE_URL`: URL de conexão com o banco de dados
- `SESSION_SECRET`: Chave secreta para sessions
- `PORT`: Porta para executar a aplicação (padrão: 5000)

