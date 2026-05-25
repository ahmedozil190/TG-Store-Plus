import os

def update_file(filename, is_store):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = {
        'en': ('lbl_txid: "ID"', 'otp_sent_desc: "A 5-digit code was sent to {phone} on Telegram."', 
               'acc_restricted_title: "Account Restricted", acc_restricted_desc: "Your access has been suspended due to a violation of our terms. Contact support for more info.", btn_updates_channel: "Updates Channel"',
               'maint_title: "Under Maintenance", maint_desc: "We\'re currently performing some scheduled maintenance to improve your experience. Please check back soon!", maint_eta: "Estimated time: 30-60 mins", '),
               
        'ar': ('lbl_txid: "المعرف"', 'otp_sent_desc: "تم إرسال كود من 5 أرقام إلى {phone} على تليجرام."', 
               'acc_restricted_title: "حساب مقيد", acc_restricted_desc: "تم تعليق وصولك بسبب انتهاك شروطنا. تواصل مع الدعم لمزيد من المعلومات.", btn_updates_channel: "قناة التحديثات"',
               'maint_title: "تحت الصيانة", maint_desc: "نحن نجري حالياً صيانة دورية لتحسين تجربتك. يرجى العودة لاحقاً!", maint_eta: "الوقت المقدر: 30-60 دقيقة", '),
               
        'zh': ('lbl_txid: "ID"', 'otp_sent_desc: "一个5位数的验证码已发送至 {phone} 的 Telegram。"', 
               'acc_restricted_title: "帐户受限", acc_restricted_desc: "由于违反我们的条款，您的访问已被暂停。请联系支持获取更多信息。", btn_updates_channel: "更新频道"',
               'maint_title: "维护中", maint_desc: "我们目前正在进行一些例行维护，以改善您的体验。请稍后再来！", maint_eta: "预计时间：30-60 分钟", '),
               
        'bn': ('lbl_txid: "ID"', 'otp_sent_desc: "টেলিগ্রামে {phone} নম্বরে একটি ৫-সংখ্যার কোড পাঠানো হয়েছে।"', 
               'acc_restricted_title: "অ্যাকাউন্ট সীমাবদ্ধ", acc_restricted_desc: "আমাদের শর্তাবলী লঙ্ঘনের কারণে আপনার অ্যাক্সেস স্থগিত করা হয়েছে। আরও তথ্যের জন্য সমর্থনের সাথে যোগাযোগ করুন。", btn_updates_channel: "আপডেট চ্যানেল"',
               'maint_title: "রক্ষণাবেক্ষণ চলছে", maint_desc: "আপনার অভিজ্ঞতা উন্নত করতে আমরা কিছু নির্ধারিত রক্ষণাবেক্ষণ করছি। শীঘ্রই ফিরে আসছি!", maint_eta: "আনুমানিক সময়: ৩০-৬০ মিনিট", '),
               
        'fa': ('lbl_txid: "المعرف"', 'otp_sent_desc: "یک کد ۵ رقمی به {phone} در تلگرام ارسال شد."', 
               'acc_restricted_title: "حساب محدود شد", acc_restricted_desc: "دسترسی شما به دلیل نقض قوانین ما مسدود شده است. برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.", btn_updates_channel: "کانال بروزرسانی‌ها"',
               'maint_title: "در حال بروزرسانی", maint_desc: "ما در حال انجام تعمیرات دوره‌ای برای بهبود تجربه شما هستیم. لطفا بعداً مراجعه کنید!", maint_eta: "زمان تقریبی: ۳۰-۶۰ دقیقه", '),
               
        'ru': ('lbl_txid: "ID"', 'otp_sent_desc: "5-значный код отправлен на {phone} в Telegram."', 
               'acc_restricted_title: "Учетная запись ограничена", acc_restricted_desc: "Ваш доступ приостановлен из-за нарушения наших условий. Свяжитесь с поддержкой для получения информации.", btn_updates_channel: "Канал обновлений"',
               'maint_title: "Техническое обслуживание", maint_desc: "Мы проводим плановые работы для улучшения сервиса. Пожалуйста, зайдите позже!", maint_eta: "Ожидаемое время: 30-60 мин.", '),
               
        'uz': ('lbl_txid: "ID"', 'otp_sent_desc: "Telegram\'da {phone} raqamiga 5 xonali kod yuborildi."', 
               'acc_restricted_title: "Hisob cheklangan", acc_restricted_desc: "Bizning shartlarimizni buzganingiz uchun kirishingiz to\'xtatildi. Qo\'shimcha ma\'lumot uchun qo\'llab-quvvatlash bilan bog\'laning.", btn_updates_channel: "Yangilanishlar kanali"',
               'maint_title: "Texnik xizmat ko\'rsatish", maint_desc: "Xizmat sifatini oshirish uchun profilaktika ishlari olib borilmoqda. Iltimos, birozdan keyin qayta urinib ko\'ring!", maint_eta: "Taxminiy vaqt: 30-60 daqiqa", '),
               
        'es': ('lbl_txid: "ID"', 'otp_sent_desc: "Se ha enviado un código de 5 dígitos a {phone} en Telegram."', 
               'acc_restricted_title: "Cuenta restringida", acc_restricted_desc: "Su acceso ha sido suspendido debido a una violación de nuestros términos. Contacte a soporte para más información.", btn_updates_channel: "Canal de actualizaciones"',
               'maint_title: "En mantenimiento", maint_desc: "Estamos realizando mantenimiento de rutina para mejorar su experiencia. ¡Vuelva pronto!", maint_eta: "Tiempo estimado: 30-60 min.", '),
               
        'tr': ('lbl_txid: "ID"', 'otp_sent_desc: "Telegram\'da {phone} adresine 5 haneli bir kod gönderildi."', 
               'acc_restricted_title: "Hesap Kısıtlandı", acc_restricted_desc: "Şartlarımızı ihlal ettiğiniz için erişiminiz askıya alındı. Daha fazla bilgi için destekle iletişime geçin.", btn_updates_channel: "Güncellemeler Kanalı"',
               'maint_title: "Bakım Çalışması", maint_desc: "Deneyiminizi iyileştirmek için rutin bakım yapıyoruz. Lütfen daha sonra tekrar gelin!", maint_eta: "Tahmini süre: 30-60 dk.", ')
    }

    for lang, data in replacements.items():
        if is_store:
            target = data[0] # lbl_txid: ...
            # Store already has maint_title, maint_desc, maint_eta. Just add acc_restricted
            replacement = f'{target},\n                {data[2]}'
        else:
            target = data[1] # otp_sent_desc: ...
            # Seller needs both maint_* and acc_restricted_*
            replacement = f'{target},\n                {data[3]}{data[2]}'
            
        content = content.replace(target, replacement)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('templates/store.html', True)
update_file('templates/seller.html', False)

print("Direct string replacement successful!")
