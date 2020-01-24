from flask import Flask, render_template, request

from model import db, save_db

app = Flask(__name__)


@app.route("/")
def home():
    page_views = db['page_views'] + 1
    print(page_views)
    db['page_views'] = page_views
    save_db()
    return render_template('index.html', page_views=page_views)


@app.route("/encrypt", methods=["GET", "POST"])
def enctrypter():
    value_count = db['values_encrypted']
    if request.method == "POST":
        # form has been submitted, process data
        try:
            value_to_encrypt = int(request.form['value_to_encrypt'].replace(',', '')) # ENFORCE INTEGER CONSTRAINT
        except ValueError:
            alert_message = 'You  must enter an integer between 1 and 1,000,000.'
            return render_template('encrypter.html', value_count=value_count, encrypted_value='', alert_code=True, alert_message=alert_message)
        # print(value_to_encrypt)
        encryption_key = int(request.form['encryption_key'])  # ENFORCE INTEGER CONSTRAINT
        # print(encryption_key)
        encrypted_value = encrypt(value_to_encrypt, encryption_key)
        print(encrypted_value)
        value_count += 1
        db['values_encrypted'] = value_count
        save_db()
        return render_template('encrypter.html', value_count=value_count, encrypted_value=str(encrypted_value))
    else:
        return render_template('encrypter.html', value_count=value_count)


@app.route("/decrypt", methods=["GET", "POST"])
def decrypter():
    value_count = db['values_decrypted']
    if request.method == "POST":
        # form has been submitted, process data
        try:
            value_to_decrypt = int(request.form['value_to_decrypt'].replace(',', '')) # ENFORCE INTEGER CONSTRAINT
        except ValueError:
            alert_message = 'You must enter an integer.'
            return render_template('decrypter.html', value_count=value_count, decrypted_value='', alert_code=True, alert_message=alert_message)
        decryption_key = int(request.form['decryption_key'])  # ENFORCE INTEGER CONSTRAINT
        decrypted_value = decrypt(value_to_decrypt, decryption_key)
        print(decrypted_value)
        value_count += 1
        db['values_decrypted'] = value_count
        save_db()
        return render_template('decrypter.html', value_count=value_count, decrypted_value=str(decrypted_value))
    else:
        return render_template('decrypter.html', value_count=value_count)


def encrypt(clear_value, key):
    encrypted_value = ((clear_value + 7) * key)-5
    return f'{encrypted_value:,}'


def decrypt(encrypted_value, key):
    decrypted_value = int(((encrypted_value + 5) / key) - 7)
    return f'{decrypted_value:,}'
