import re

def format_phone_number(phone_number):
    """
    Formata o número de telefone para uso no WhatsApp
    
    Args:
        phone_number (str): Número de telefone no formato +XX(XXX)XXXXX-XXXX ou qualquer outro
        
    Returns:
        str: Número formatado para uso no WhatsApp (somente dígitos)
    """
    if not phone_number:
        return ""
    
    # Remove todos os caracteres que não são dígitos
    digits_only = re.sub(r'\D', '', phone_number)
    
    # Garante que o número começa com o código do país (Brasil = 55)
    if not digits_only.startswith('55') and len(digits_only) <= 11:
        digits_only = '55' + digits_only
        
    return digits_only

def get_whatsapp_link(phone_number, message=None):
    """
    Gera um link para abrir uma conversa no WhatsApp
    
    Args:
        phone_number (str): Número de telefone do destinatário
        message (str, optional): Mensagem pré-preenchida (opcional)
        
    Returns:
        str: URL para abrir conversa no WhatsApp
    """
    formatted_number = format_phone_number(phone_number)
    if not formatted_number:
        return "#"
    
    base_url = f"https://wa.me/{formatted_number}"
    
    if message:
        # Codifica a mensagem para URL
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        return f"{base_url}?text={encoded_message}"
    
    return base_url

def get_whatsapp_api_link(phone_number, message=None):
    """
    Gera um link para a API do WhatsApp (usado para dispositivos móveis)
    
    Args:
        phone_number (str): Número de telefone do destinatário
        message (str, optional): Mensagem pré-preenchida (opcional)
        
    Returns:
        str: URL para abrir conversa no WhatsApp via API
    """
    formatted_number = format_phone_number(phone_number)
    if not formatted_number:
        return "#"
    
    if message:
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        return f"whatsapp://send?phone={formatted_number}&text={encoded_message}"
    
    return f"whatsapp://send?phone={formatted_number}"