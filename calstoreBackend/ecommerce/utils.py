import requests
from decouple import config

def send_telegram_notification(order_details):
    token = config('my_bot_token')
    chat_id = config('my_bot_chat_id')
    message = f"🚀 **Nouvelle commande !**\n\n" \
              f"Client: {order_details['customer']}\n" \
              f"Total: {order_details['amount']}€\n" \
              f"ID: #{order_details['id']}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erreur notification : {e}")

def send_order_telegram_notifications(
    id,
    order_number,
    customer,
    items,
    total_price,
):
    token = config('my_bot_token')
    chat_id = config('my_bot_chat_id')
    
    # Formatage de la liste des articles
    items_list = ""
    for i, item in enumerate(items[:5], 1):  # Limite à 5 articles pour lisibilité
        items_list += f"  • {item.get('name', 'Produit')} x{item.get('quantity', 1)}\n"
    
    if len(items) > 5:
        items_list += f"  • ... et {len(items) - 5} autre(s) article(s)\n"
    
    # Message professionnel avec emojis et formatage Markdown
    message = (
        "🛒 *NOUVELLE COMMANDE CALSTORE* 🛒\n\n"
        f"📦 *Commande :* #{order_number}\n"
        f"👤 *Client :* {customer}\n"
        f"💰 *Total :* {float(total_price):.2f}€\n"
        f"📋 *Articles ({len(items)}) :*\n"
        f"{items_list}\n"
        f"🆔 *ID interne :* {id}"
    )
    
    # Alternative plus concise si préférée
    """
    message = (
        "🛒 *NOUVELLE COMMANDE* | Calstore\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 #{order_number} | {customer}\n"
        f"💰 {float(total_price):.2f}€ | 📋 {len(items)} art.\n"
        f"🆔 Ref: {id}"
    )
    """
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Erreur notification Telegram : {e}")
        return False
    


