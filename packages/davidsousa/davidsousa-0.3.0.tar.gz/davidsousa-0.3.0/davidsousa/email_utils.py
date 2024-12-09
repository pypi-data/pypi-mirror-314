# davidsousa/email_utils.py


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


def enviar_email(nome_remetente, remetente, senha, destinatario, assunto, corpo, importante=False, html=False): 
    """
    Função para enviar e-mail usando o servidor SMTP do Gmail.

    Parâmetros:
    remetente (str): Endereço de e-mail do remetente.
    senha (str): Senha do remetente.
    destinatario (str): Endereço de e-mail do destinatário.
    assunto (str): Assunto do e-mail.
    corpo (str): Corpo do e-mail.
    nome_remetente (str): Nome do remetente que será exibido no e-mail.
    importante (bool): Define se o e-mail é de alta prioridade. Valor padrão é False.
    html (bool): Define se o corpo do e-mail é HTML. Valor padrão é False.
    """
    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587
    mensagem = MIMEMultipart()
    mensagem['From'] = formataddr((nome_remetente, remetente))
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    # Marcar como importante
    if importante:
        mensagem['X-Priority'] = '1'
        mensagem['Importance'] = 'High'

    # Anexar o corpo do e-mail como texto simples ou HTML
    mensagem.attach(MIMEText(corpo, 'html' if html else 'plain'))
    
    try:
        servidor = smtplib.SMTP(host=servidor_smtp, port=porta_smtp)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, mensagem.as_string())
        servidor.quit()
        return True
    except Exception as e:
        print("Erro ao enviar o e-mail:", e)
