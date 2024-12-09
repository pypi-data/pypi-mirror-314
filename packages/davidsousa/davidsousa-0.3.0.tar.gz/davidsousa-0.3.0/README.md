# davidsousa

## Biblioteca para envio de e-mails com suporte a HTML e prioridade (Experimental). (Gmail)

### Instalação

```

pip install davidsousa


```

### Uso .py

```

from davidsousa import enviar_email

nome_remetente = "Seu Nome"
remetente = "seu_email@gmail.com"
senha = "sua_senha"
destinatario = "destinatario@example.com"
assunto = "Assunto do E-mail"
corpo = "<h1>Este é o assunto do e-mail</h1><p>Este é o corpo do e-mail em HTML.</p>"


# Enviar e-mail com corpo em HTML e marcado como importante
enviar_email(nome_remetente, remetente, senha, destinatario, assunto, corpo, importante=True, html=True)



```