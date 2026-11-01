from flask import Flask, request, jsonify
import random
import requests
import os

app = Flask(__name__)

# Твой ключ уже вставлен
SMSRU_API_KEY = "00C37724-1016-DA00-F39F-0DA154B0FF22"

codes = {}

@app.route('/')
def home():
    return "Сервер Мехаграмм работает!"

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    phone = data.get('phone')
    if not phone:
        return jsonify({"error": "Нет номера"}), 400

    phone = ''.join(filter(str.isdigit, phone))
    if phone.startswith('8'):
        phone = '7' + phone[1:]

    code = str(random.randint(1000, 9999))
    codes[phone] = code

    url = f"https://sms.ru/sms/send?api_id={SMSRU_API_KEY}&to={phone}&msg=Ваш код для Мехаграмма: {code}&json=1"
    
    try:
        res = requests.get(url).json()
        if res.get('status') == 'OK':
            return jsonify({"success": True})
        else:
            return jsonify({"error": res.get('status_text', 'Ошибка SMS')}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.json
    phone = data.get('phone')
    user_code = data.get('code')
    
    phone = ''.join(filter(str.isdigit, phone))
    if phone.startswith('8'):
        phone = '7' + phone[1:]

    if codes.get(phone) == user_code:
        del codes[phone]
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Неверный код"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
