import smtplib

def start_server():
    """
    This method is used to start a smtp mail server.

    Returns:
        object: smtp mail server object.
    """
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    return server

def login(server,username,password):
    """
    This method is used for logging into the from mail account.

    Args:
        username (str): username of the from mail account.
        password (str): password to login into from mail account.

    Returns:
        int: 0
    """
    server.login(username,password)
    return 0

def send_message(server,from_mail,to_mail,message):
    """
    This method is used for sending mail from from_mail address to to_mail address.

    Args:
        from_mail (str): from mail address.
        to_mail (str): to mail address.
        message (str): message to send.

    Returns:
        int: 0
    """
    server.sendmail(from_mail,to_mail,message)
    return 0