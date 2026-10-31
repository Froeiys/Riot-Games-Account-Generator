# Riot-Games-Account-Generator
Riot Games Account Generator - ( WORK ON ALL RIOT GAMES )

İşte NmGen.py projeniz için GitHub'da doğrudan kullanabileceğiniz, çok daha detaylı, profesyonel, çift dilli (Türkçe / English) ve kapsamlı README.md şablonu:
⚡ NeverManuel (NmGen.py)

Türkçe | English
🇹🇷 Türkçe Dokümantasyon

NeverManuel, modern ve şık arayüzüyle Riot Games hesap oluşturma süreçlerini tamamen otomatikleştirmenizi sağlayan, PySide6 ve DrissionPage altyapısıyla geliştirilmiş gelişmiş bir masaüstü otomasyon aracıdır.
✨ Öne Çıkan Özellikler

    🎨 Dinamik Tema Motoru: Kırmızı, Mor, Mavi, Yeşil, Sarı ve Monokrom (Siyah-Beyaz) olmak üzere 6 farklı renk profili ve modern arayüz tasarımı.

    🤖 Akıllı Otomasyon: DrissionPage kütüphanesi güvencesiyle Riot Games kayıt sayfasını otomatik olarak yönetir; doğum tarihi, kullanıcı adı ve güvenli şifreleri insan simülasyonu (yazma gecikmeleri dahil) ile doldurur.

    🌐 Cloudflare WARP Entegrasyonu: IP limitlerine ve banlara takılmamak için dahili WARP UDP kontrolü, otomatik IP yenileme ve bağlantı yönetimi.

    📊 Canlı İstatistik Paneli: Başarılı ve hatalı işlem sayısını, anlık başarı yüzdesini ve genel ilerleme durumunu (progress bar) canlı olarak takip edin.

    📋 Gelişmiş Oturum Yönetimi: Üretilen hesapların kullanıcı adı, şifre ve e-posta bilgilerini tek tıkla panoya kopyalayın; oturum geçmişini arayüzde kartlar halinde inceleyin.

    ⚙️ Özelleştirilebilir Deneyim: Geçiş efektleri (motion blur), ses bildirimleri ve tarayıcı bekleme süresini kaydırıcılar (slider) vasıtasıyla dilediğiniz gibi ayarlayın.

⚙️ Sistem Gereksinimleri

    Python 3.8 veya üzeri

    Google Chrome (DrissionPage tarayıcı otomasyonu için zorunludur)

    Cloudflare WARP CLI (İsteğe bağlı - Ağ/IP değiştirme özelliğini kullanmak istiyorsanız gereklidir)

📥 Kurulum Adımları

    Projeyi klonlayın veya NmGen.py dosyasını bilgisayarınıza indirin.

    Terminal veya Komut İstemi'ni (CMD) açarak dosyanın bulunduğu dizine gidin.

    Gerekli Python kütüphanelerini yükleyin:
    Bash

    pip install DrissionPage PySide6

🕹️ Kullanım Rehberi

Uygulamayı başlatmak için terminale şu komutu yazın:
Bash

python NmGen.py

    Kontrol Merkezi: Üretilmesini istediğiniz hesap miktarını girin ve BAŞLAT butonuna tıklayın.

    Ağ Tercihi: WARP seçeneğini aktif ederek her hesap oluşturma döngüsünden sonra güvenli bir şekilde IP adresinizin yenilenmesini sağlayın.

    Ayarlar: Görsel tercihlerinizi ve tarayıcı bekleme sürelerini yapılandırın.

📁 Çıktı Dosyaları

Program, çalışma dizininde otomatik olarak şu dosyaları oluşturur:

    kurulanhesaplar.txt: Başarıyla oluşturulan hesapların kullaniciadi:sifre formatındaki listesi.

    hatalihesaplar.txt: İşlem sırasında hata alan hesapların kayıtları.

🇬🇧 English Documentation

NeverManuel is an advanced desktop automation tool developed with PySide6 and the DrissionPage framework, designed to seamlessly automate Riot Games account creation workflows with a modern and sleek interface.
✨ Key Features

    🎨 Dynamic Theme Engine: Features 6 distinct color profiles (Red, Purple, Blue, Green, Yellow, and Monochrome) paired with a modern UI design.

    🤖 Smart Automation: Powered by DrissionPage to automatically manage the Riot Games registration page, securely filling out birth dates, usernames, and passwords with human-like typing simulation.

    🌐 Cloudflare WARP Integration: Built-in WARP UDP control and automatic IP rotation mechanism to bypass IP limits and bans.

    📊 Live Statistics Panel: Real-time monitoring of successful and failed operations, success rate percentages, and overall progress.

    📋 Advanced Session Management: One-click clipboard copying for generated account credentials (username, password, email) with clean session history cards.

    ⚙️ Customizable Experience: Easily configure transition effects, sound notifications, and browser waiting times via interactive sliders.

⚙️ System Requirements

    Python 3.8 or higher

    Google Chrome (Required for DrissionPage browser automation)

    Cloudflare WARP CLI (Optional - Required only if you want to use the network/IP rotation feature)

📥 Installation Steps

    Clone the repository or download the NmGen.py file.

    Open your terminal or Command Prompt and navigate to the target directory.

    Install the required Python dependencies:
    Bash

    pip install DrissionPage PySide6

🕹️ Usage Guide

Launch the application by running the following command in your terminal:
Bash

python NmGen.py

    Control Center: Enter the desired number of accounts to generate and click START.

    Network Preference: Toggle WARP on to automatically rotate your IP address after each account creation cycle.

    Settings: Customize your visual preferences and browser wait times.

📁 Output Files

The script automatically generates the following text files in its working directory:

    kurulanhesaplar.txt: List of successfully created accounts in username:password format.

    hatalihesaplar.txt: Records of accounts that encountered errors during execution.
