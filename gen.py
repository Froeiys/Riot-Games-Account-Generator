import os
import random
import string
import subprocess
import sys
import time
import uuid

from DrissionPage import ChromiumOptions, ChromiumPage
from DrissionPage.common import Keys
from PySide6.QtCore import QThread, QTimer, QUrl, Qt, QEasingCurve, QPropertyAnimation
from PySide6.QtCore import Signal as pyqtSignal
from PySide6.QtGui import QCursor, QDesktopServices, QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QGridLayout,
    QGraphicsOpacityEffect,
    QSizePolicy,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QScroller,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


# ==================== YARDIMCI FONKSİYONLAR ====================
def generate_secure_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choices(chars, k=length))

def fast_password_type(element, text, delay=0.16):
    """
    Şifreyi insan benzetimi olmadan, her karakter arasında sabit 0.16s (160ms) bekleme ile yazar.
    """
    element.click()
    for char in text:
        element.input(char)
        time.sleep(delay)


# ==================== WARP UDP KONTROL FONKSİYONLARI ====================
def setup_warp_udp():
    try:
        subprocess.run(["warp-cli", "mode", "warp"], capture_output=True, check=False)
        subprocess.run(
            ["warp-cli", "set-mode", "warp"], capture_output=True, check=False
        )
    except Exception as e:
        print(f"[WARP] Mod ayarlama hatası: {e}")


def connect_warp(wait_time=2):
    try:
        print("[WARP] Bağlantı açılıyor...")
        subprocess.run(["warp-cli", "connect"], capture_output=True, check=False)
        time.sleep(wait_time)
        print("[WARP] Bağlantı sağlandı.")
    except Exception as e:
        print(f"[WARP] Bağlanma hatası: {e}")


def disconnect_warp():
    try:
        print("[WARP] Bağlantı kapatılıyor...")
        subprocess.run(["warp-cli", "disconnect"], capture_output=True, check=False)
        print("[WARP] Bağlantı kesildi.")
    except Exception as e:
        print(f"[WARP] Kesme hatası: {e}")


def reset_warp_ip(wait_time=2):
    disconnect_warp()
    time.sleep(0.5)
    connect_warp(wait_time)


# ==================== DİNAMİK TEMA MOTORU ====================
THEMES = {
    "mor": {
        "primary": "#c084fc",
        "secondary": "#a855f7",
        "bg_main": "#0b0512",
        "bg_card": "#150a24",
        "bg_nav": "#0e071a",
        "border": "#2c1545",
        "btn_start": "linear-gradient(135deg, #a855f7 0%, #7e22ce 100%)",
        "btn_start_hover": "linear-gradient(135deg, #9333ea 0%, #6b21a8 100%)",
        "text_main": "#f3e8ff",
        "btn_text": "#ffffff",
    },
    "mavi": {
        "primary": "#38bdf8",
        "secondary": "#0284c7",
        "bg_main": "#040b14",
        "bg_card": "#09172a",
        "bg_nav": "#06101e",
        "border": "#132d4f",
        "btn_start": "linear-gradient(135deg, #38bdf8 0%, #0284c7 100%)",
        "btn_start_hover": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
        "text_main": "#e0f2fe",
        "btn_text": "#ffffff",
    },
    "yesil": {
        "primary": "#34d399",
        "secondary": "#10b981",
        "bg_main": "#030f0a",
        "bg_card": "#072017",
        "bg_nav": "#051710",
        "border": "#0f4230",
        "btn_start": "linear-gradient(135deg, #10b981 0%, #047857 100%)",
        "btn_start_hover": "linear-gradient(135deg, #059669 0%, #065f46 100%)",
        "text_main": "#ecfdf5",
        "btn_text": "#ffffff",
    },
    "sari": {
        "primary": "#fbbf24",
        "secondary": "#f59e0b",
        "bg_main": "#120e03",
        "bg_card": "#211a07",
        "bg_nav": "#181305",
        "border": "#42340e",
        "btn_start": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
        "btn_start_hover": "linear-gradient(135deg, #d97706 0%, #b45309 100%)",
        "text_main": "#fef3c7",
        "btn_text": "#000000",
    },
    "kirmizi": {
        "primary": "#f87171",
        "secondary": "#ef4444",
        "bg_main": "#120404",
        "bg_card": "#210909",
        "bg_nav": "#170606",
        "border": "#451212",
        "btn_start": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "btn_start_hover": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
        "text_main": "#fef2f2",
        "btn_text": "#ffffff",
    },
    "siyah_beyaz": {
        "primary": "#ffffff",
        "secondary": "#a1a1aa",
        "bg_main": "#09090b",
        "bg_card": "#18181b",
        "bg_nav": "#121215",
        "border": "#27272a",
        "btn_start": "linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)",
        "btn_start_hover": "linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%)",
        "text_main": "#ffffff",
        "btn_text": "#09090b",
    },
}


def get_theme_stylesheet(theme_name):
    t = dict(THEMES[theme_name])
    primary = t.get("primary", "#ef4444")
    secondary = t.get("secondary", "#991b1b")
    bg = t.get("bg_main", "#08090d")
    panel = t.get("bg_card", "#101217")
    sidebar = t.get("bg_nav", "#0b0d12")
    border = t.get("border", "#242834")
    text_main = t.get("text_main", "#f4f7fb")
    muted = t.get("text_muted", t.get("text_sub", "#8b93a7"))

    return f"""
    * {{
        font-family: "Segoe UI", Arial;
        color: {text_main};
    }}

    QMainWindow, QWidget {{
        background: {bg};
    }}

    QFrame#Sidebar {{
        background: {sidebar};
        border: 1px solid {border};
        border-radius: 22px;
    }}

    QFrame#TopBar, QFrame#Surface, QFrame#StatCard, QFrame#AboutCard {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 18px;
    }}

    QFrame#AccentCard {{
        background: {panel};
        border: 1px solid {primary};
        border-radius: 20px;
    }}

    QLabel#Brand {{
        color: {primary};
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 2px;
    }}

    QLabel#Eyebrow {{
        color: {muted};
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
    }}

    QLabel#PageTitle {{
        font-size: 25px;
        font-weight: 800;
        color: {text_main};
    }}

    QLabel#SectionTitle {{
        font-size: 15px;
        font-weight: 800;
        color: {text_main};
    }}

    QLabel#Muted {{
        color: {muted};
        font-size: 12px;
    }}

    QLabel#Metric {{
        color: {primary};
        font-size: 24px;
        font-weight: 900;
    }}

    QPushButton {{
        background: transparent;
        color: {text_main};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
    }}

    QPushButton:hover {{
        border-color: {primary};
        background: rgba(255,255,255,0.035);
    }}

    QPushButton#NavButton {{
        text-align: left;
        color: {muted};
        border: 0px;
        border-radius: 12px;
        padding: 13px 14px;
    }}

    QPushButton#NavButton:hover, QPushButton#NavButton:checked {{
        background: {panel};
        color: {primary};
        border: 0px;
    }}

    QPushButton#PrimaryButton {{
        background: {primary};
        color: #ffffff;
        border: 1px solid {primary};
        font-weight: 900;
        min-height: 26px;
    }}

    QPushButton#PrimaryButton:hover {{
        background: {secondary};
        border-color: {secondary};
    }}

    QPushButton#DangerButton:hover {{
        color: #ff5a6a;
        border-color: #ff5a6a;
    }}

    QPushButton#BtnWarpToggle:checked {{
        background: {primary};
        color: #ffffff;
        border-color: {primary};
    }}

    QLineEdit {{
        background: {sidebar};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 12px 14px;
        min-height: 24px;
        color: {text_main};
    }}

    QLineEdit:focus {{
        border-color: {primary};
        background: {panel};
    }}

    QRadioButton {{
        background: {sidebar};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 11px 13px;
        color: {muted};
    }}

    QRadioButton:hover {{
        border-color: {primary};
        color: {text_main};
    }}

    QRadioButton::indicator {{
        width: 13px;
        height: 13px;
    }}

    QRadioButton::indicator:checked {{
        background: {primary};
        border: 2px solid {text_main};
        border-radius: 6px;
    }}

    QTextEdit, QScrollArea {{
        background: transparent;
        border: 0px;
    }}

    QProgressBar {{
        background: {sidebar};
        border: 1px solid {border};
        border-radius: 8px;
        height: 10px;
    }}

    QProgressBar::chunk {{
        background: {primary};
        border-radius: 7px;
    }}

    QScrollBar:vertical {{
        width: 7px;
        background: transparent;
        margin: 4px;
    }}

    QScrollBar::handle:vertical {{
        background: {border};
        border-radius: 3px;
        min-height: 28px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {primary};
    }}

    QSlider::groove:horizontal {{
        border: 1px solid {border};
        height: 8px;
        background: {sidebar};
        border-radius: 4px;
    }}

    QSlider::handle:horizontal {{
        background: {primary};
        border: 1px solid {primary};
        width: 18px;
        margin-top: -5px;
        margin-bottom: -5px;
        border-radius: 9px;
    }}

    QSlider::handle:horizontal:hover {{
        background: {secondary};
    }}
    """

class WarpResetWorker(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        reset_warp_ip(wait_time=2)
        self.finished_signal.emit()


class AccountCardWidget(QFrame):

    def __init__(self, username, password, email):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #0b101d;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 10px;
            }
            QLabel {
                font-size: 12px;
            }
            QPushButton {
                background-color: #1e293b;
                color: #38bdf8;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
                color: #ffffff;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(12)

        layout.addWidget(QLabel("<b style='color:#64748b;'>USER:</b>"))
        lbl_user = QLabel(self.username)
        lbl_user.setStyleSheet("color: #38bdf8; font-weight: bold;")
        layout.addWidget(lbl_user)
        btn_copy_user = QPushButton("Kopyala")
        btn_copy_user.clicked.connect(
            lambda: self.copy_to_clipboard(self.username, btn_copy_user)
        )
        layout.addWidget(btn_copy_user)

        layout.addSpacing(10)

        layout.addWidget(QLabel("<b style='color:#64748b;'>PASS:</b>"))
        lbl_pass = QLabel(self.password)
        lbl_pass.setStyleSheet("color: #f43f5e; font-weight: bold;")
        layout.addWidget(lbl_pass)
        btn_copy_pass = QPushButton("Kopyala")
        btn_copy_pass.clicked.connect(
            lambda: self.copy_to_clipboard(self.password, btn_copy_pass)
        )
        layout.addWidget(btn_copy_pass)

        layout.addSpacing(10)

        layout.addWidget(QLabel("<b style='color:#64748b;'>MAIL:</b>"))
        lbl_email = QLabel(self.email)
        lbl_email.setStyleSheet("color: #a855f7;")
        layout.addWidget(lbl_email)
        btn_copy_email = QPushButton("Kopyala")
        btn_copy_email.clicked.connect(
            lambda: self.copy_to_clipboard(self.email, btn_copy_email)
        )
        layout.addWidget(btn_copy_email)

        layout.addStretch()

    def copy_to_clipboard(self, text, button):
        QApplication.clipboard().setText(text)
        button.setText("✓")
        button.setStyleSheet(
            "background-color: #10b981; color: #ffffff; border-radius: 6px;"
            " padding: 5px 10px;"
        )
        QTimer.singleShot(1500, lambda: self.reset_button_style(button))

    def reset_button_style(self, button):
        button.setText("Kopyala")
        button.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #38bdf8;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
                color: #ffffff;
            }
        """)


class GeneratorWorker(QThread):
    account_created_signal = pyqtSignal(dict)
    account_result_signal = pyqtSignal(bool)
    finished_signal = pyqtSignal()

    def __init__(self, count, use_warp=False, browser_wait_time=15):
        super().__init__()
        self.count = count
        self.use_warp = use_warp
        self.browser_wait_time = browser_wait_time
        self._is_running = True

    def run(self):
        if self.use_warp:
            disconnect_warp()
            time.sleep(1)
            setup_warp_udp()
            connect_warp(wait_time=2)

        for i in range(self.count):
            if not self._is_running:
                break

            t_id = str(uuid.uuid4())
            u_dir = f"user_data_{t_id}"

            success = False
            account_info = {}

            try:
                success, account_info = self.create_riot_account(t_id, u_dir)
            except Exception:
                success = False

            if not self._is_running:
                break

            if success and account_info:
                line = f"{account_info['username']}:{account_info['password']}\n"
                with open("kurulanhesaplar.txt", "a", encoding="utf-8") as f:
                    f.write(line)

                self.account_created_signal.emit(account_info)
                self.account_result_signal.emit(True)
            else:
                if account_info.get("username") and account_info.get("password"):
                    fail_line = (
                        f"{account_info['username']}:{account_info['password']}\n"
                    )
                    with open("hatalihesaplar.txt", "a", encoding="utf-8") as f:
                        f.write(fail_line)
                self.account_result_signal.emit(False)

            if i < self.count - 1 and self._is_running and self.use_warp:
                reset_warp_ip(wait_time=2)

        if self.use_warp:
            disconnect_warp()

        self.finished_signal.emit()

    def stop(self):
        self._is_running = False

    def create_riot_account(self, task_id, user_data_dir):
        os.makedirs(user_data_dir, exist_ok=True)
        account_info = {}
        page = None

        try:
            port = random.randint(9000, 9999)
            options = ChromiumOptions()
            options.incognito(True)
            
            options.set_argument("--disable-blink-features=AutomationControlled")
            options.set_argument("--no-first-run")
            options.set_argument("--disable-infobars")
            options.set_argument("--lang=tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7")
            options.set_argument("--window-size=1920,1080")
            options.set_local_port(port)
            options.set_user_data_path(user_data_dir)
            options.set_argument("--no-sandbox")
            options.set_argument("--disable-gpu")

            page = ChromiumPage(options)
            page.get("https://account.riotgames.com/")
            time.sleep(0.8)

            if not self._is_running:
                return False, account_info

            btn_create = page.ele(
                "xpath:/html/body/div[2]/div/main/div/form/div/div/div[3]/span[2]"
            )
            btn_create.click()
            time.sleep(0.5)

            account_info["email"] = (
                "".join(
                    random.choices(string.ascii_lowercase + string.digits, k=10)
                )
                + "@gmail.com"
            )
            email_field = page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div[1]/div/input"
            )
            email_field.click()
            email_field.input(account_info["email"])
            
            time.sleep(0.2)
            page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[3]/button/div"
            ).click()
            time.sleep(0.5)

            if not self._is_running:
                return False, account_info

            day_field = page.ele("xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[1]/input")
            month_field = page.ele("xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[2]/input")
            year_field = page.ele("xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[3]/input")

            day_field.input("12")
            month_field.input("12")
            year_field.input("2002")

            time.sleep(0.2)
            page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[3]/button/div"
            ).click()
            time.sleep(0.5)

            random_suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=6)
            )
            account_info["username"] = f"neverloop{random_suffix}"

            username_input = page.ele(
                'xpath://input[@type="text" or @name="username"]', timeout=3
            )
            if not username_input:
                username_input = page.ele(
                    "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div/input"
                )
            
            username_input.click()
            username_input.input(account_info["username"])

            time.sleep(0.2)
            page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[3]/button/div"
            ).click()
            time.sleep(0.5)

            # ŞİFRE ADIMI (Sabit 0.16s / 160ms Gecikme ile Yazım)
            password_str = generate_secure_password()
            account_info["password"] = password_str

            pass_field = page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[1]/div/input"
            )
            fast_password_type(pass_field, password_str, delay=0.16)

            confirm_field = page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[4]/div[1]/input"
            )
            fast_password_type(confirm_field, password_str, delay=0.16)

            time.sleep(0.5)
            page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[3]/button/div"
            ).click()
            time.sleep(0.8)

            tos_scroll = page.ele('xpath://*[@id="tos-scrollable-area"]')
            if tos_scroll:
                page.run_js(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", tos_scroll
                )

            time.sleep(0.3)
            page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[2]/div/div[3]/div/div/div/input"
            ).click()
            
            time.sleep(0.2)
            page.ele(
                "xpath:/html/body/div[2]/div/main/div[3]/div/div[2]/div/div[3]/button"
            ).click()

            # Kullanıcı ayarlarından alınan dinamik bekleme süresi
            time.sleep(self.browser_wait_time)

            return True, account_info

        except Exception:
            return False, account_info
        finally:
            if page:
                try:
                    page.quit()
                except:
                    pass
            if os.path.exists(user_data_dir):
                import shutil

                shutil.rmtree(user_data_dir, ignore_errors=True)


class ClickableLabel(QLabel):

    def __init__(self, text, url):
        super().__init__(text)
        self.url = url
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            QDesktopServices.openUrl(QUrl(self.url))


class MotionBlurOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter, QColor
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255, 18))


class RiotAppGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.success_count = 0
        self.fail_count = 0
        self.total_target = 0
        self.worker = None
        self.warp_worker = None
        self.current_theme = "kirmizi"
        self.browser_wait_time = 15

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("NeverManuel")
        self.setMinimumSize(1260, 760)
        self.resize(1420, 820)

        self.motion_blur_enabled = True
        self.transition_sound_enabled = False
        self.ambient_sound_enabled = False
        self._last_page = 0

        self.setStyleSheet(get_theme_stylesheet(self.current_theme))

        central = QWidget(self)
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        # ---------------- LEFT SIDEBAR ----------------
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(236)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(16, 20, 16, 16)
        side.setSpacing(8)

        brand = QLabel("NEVERMANUEL")
        brand.setObjectName("Brand")
        side.addWidget(brand)

        subtitle = QLabel("CONTROL DESK")
        subtitle.setObjectName("Eyebrow")
        side.addWidget(subtitle)
        side.addSpacing(24)

        self.btn_nav_control = self._nav_button("◉   Kontrol", 0, True)
        self.btn_nav_logs = self._nav_button("▣   Oturumlar", 1)
        self.btn_nav_settings = self._nav_button("⚙   Ayarlar", 2)
        self.btn_nav_about = self._nav_button("◌   Bağlantılar", 3)

        for button in (
            self.btn_nav_control,
            self.btn_nav_logs,
            self.btn_nav_settings,
            self.btn_nav_about,
        ):
            side.addWidget(button)

        side.addStretch()

        status_card = QFrame()
        status_card.setObjectName("AccentCard")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(14, 14, 14, 14)
        status_title = QLabel("SİSTEM DURUMU")
        status_title.setObjectName("Eyebrow")
        status_value = QLabel("Hazır")
        status_value.setObjectName("SectionTitle")
        status_layout.addWidget(status_title)
        status_layout.addWidget(status_value)
        side.addWidget(status_card)

        cg = QPushButton("CG")
        cg.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://cheatglobal.com/members/froeiys.274294/"))
        )
        side.addWidget(cg)

        root.addWidget(sidebar)

        # ---------------- MAIN AREA ----------------
        main = QVBoxLayout()
        main.setSpacing(14)

        topbar = QFrame()
        topbar.setObjectName("TopBar")
        topbar.setFixedHeight(88)
        top = QHBoxLayout(topbar)
        top.setContentsMargins(24, 16, 24, 16)

        title_box = QVBoxLayout()
        page_title = QLabel("Kontrol Merkezi")
        page_title.setObjectName("PageTitle")
        self.lbl_page_title = page_title
        page_sub = QLabel("Tüm işlemler ve görünüm tek merkezden yönetilir.")
        page_sub.setObjectName("Muted")
        title_box.addWidget(page_title)
        title_box.addWidget(page_sub)
        top.addLayout(title_box)
        top.addStretch()

        self.lbl_warp_state = QLabel("WARP • KAPALI")
        self.lbl_warp_state.setObjectName("Eyebrow")
        top.addWidget(self.lbl_warp_state)

        main.addWidget(topbar)

        self.stack = QStackedWidget()
        main.addWidget(self.stack, 1)
        root.addLayout(main, 1)

        # ================= PAGE 0: CONTROL =================
        page_control = QWidget()
        control = QVBoxLayout(page_control)
        control.setContentsMargins(0, 0, 0, 0)
        control.setSpacing(14)

        grid = QGridLayout()
        grid.setSpacing(14)
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 2)

        run_card = QFrame()
        run_card.setObjectName("Surface")
        run_layout = QVBoxLayout(run_card)
        run_layout.setContentsMargins(24, 24, 24, 24)
        run_layout.setSpacing(14)

        run_head = QLabel("Yeni Oturum")
        run_head.setObjectName("SectionTitle")
        run_text = QLabel("Miktarı belirle, ağ tercihini seç ve işlemi başlat.")
        run_text.setObjectName("Muted")
        run_layout.addWidget(run_head)
        run_layout.addWidget(run_text)
        run_layout.addSpacing(8)

        amount_label = QLabel("İŞLEM MİKTARI")
        amount_label.setObjectName("Eyebrow")
        run_layout.addWidget(amount_label)

        self.entry_count = QLineEdit()
        self.entry_count.setText("1")
        self.entry_count.setPlaceholderText("Örn. 1")
        run_layout.addWidget(self.entry_count)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.btn_start = QPushButton("BAŞLAT")
        self.btn_start.setObjectName("PrimaryButton")
        self.btn_start.clicked.connect(self.start_process)
        action_row.addWidget(self.btn_start, 2)

        self.btn_stop = QPushButton("DURDUR")
        self.btn_stop.setObjectName("DangerButton")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_process)
        action_row.addWidget(self.btn_stop, 1)

        run_layout.addLayout(action_row)
        grid.addWidget(run_card, 0, 0)

        warp_card = QFrame()
        warp_card.setObjectName("AccentCard")
        warp_layout = QVBoxLayout(warp_card)
        warp_layout.setContentsMargins(24, 24, 24, 24)
        warp_layout.setSpacing(12)

        warp_head = QLabel("Ağ Tercihi")
        warp_head.setObjectName("SectionTitle")
        warp_desc = QLabel("Açık olduğunda işlem başlamadan önce bağlantı hazırlanır.")
        warp_desc.setWordWrap(True)
        warp_desc.setObjectName("Muted")
        warp_layout.addWidget(warp_head)
        warp_layout.addWidget(warp_desc)
        warp_layout.addStretch()

        self.btn_use_warp = QPushButton("WARP KULLAN: KAPALI")
        self.btn_use_warp.setObjectName("BtnWarpToggle")
        self.btn_use_warp.setCheckable(True)
        self.btn_use_warp.setChecked(False)
        self.btn_use_warp.toggled.connect(self.update_warp_toggle)
        warp_layout.addWidget(self.btn_use_warp)

        self.btn_warp_manual = QPushButton("Bağlantıyı Yenile")
        self.btn_warp_manual.setEnabled(False)
        self.btn_warp_manual.clicked.connect(self.manual_warp_reset)
        warp_layout.addWidget(self.btn_warp_manual)
        grid.addWidget(warp_card, 0, 1)

        control.addLayout(grid)

        overview = QFrame()
        overview.setObjectName("Surface")
        overview_layout = QHBoxLayout(overview)
        overview_layout.setContentsMargins(20, 18, 20, 18)
        overview_layout.setSpacing(12)

        self.lbl_success = self._metric_card("BAŞARILI", "0")
        self.lbl_fail = self._metric_card("HATALI", "0")
        self.lbl_rate = self._metric_card("BAŞARI ORANI", "%0")

        overview_layout.addWidget(self._metric_widget("BAŞARILI", self.lbl_success))
        overview_layout.addWidget(self._metric_widget("HATALI", self.lbl_fail))
        overview_layout.addWidget(self._metric_widget("BAŞARI ORANI", self.lbl_rate))
        control.addWidget(overview)

        progress_card = QFrame()
        progress_card.setObjectName("Surface")
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setContentsMargins(20, 18, 20, 18)
        progress_title = QLabel("İLERLEME")
        progress_title.setObjectName("Eyebrow")
        progress_layout.addWidget(progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar)
        control.addWidget(progress_card)

        control.addStretch()
        self.stack.addWidget(page_control)

        # ================= PAGE 1: SESSIONS =================
        page_logs = QWidget()
        logs = QVBoxLayout(page_logs)
        logs.setContentsMargins(0, 0, 0, 0)
        logs.setSpacing(14)

        logs_head = QFrame()
        logs_head.setObjectName("Surface")
        logs_head_layout = QHBoxLayout(logs_head)
        logs_head_layout.setContentsMargins(22, 18, 22, 18)
        logs_title = QLabel("Oturum Geçmişi")
        logs_title.setObjectName("PageTitle")
        logs_head_layout.addWidget(logs_title)
        logs_head_layout.addStretch()
        logs_hint = QLabel("Yeni kayıtlar üstte görünür")
        logs_hint.setObjectName("Muted")
        logs_head_layout.addWidget(logs_hint)
        logs.addWidget(logs_head)

        logs_surface = QFrame()
        logs_surface.setObjectName("Surface")
        logs_surface_layout = QVBoxLayout(logs_surface)
        logs_surface_layout.setContentsMargins(12, 12, 12, 12)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        QScroller.grabGesture(
            self.scroll_area.viewport(),
            QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        self.accounts_container = QWidget()
        self.accounts_layout = QVBoxLayout(self.accounts_container)
        self.accounts_layout.setContentsMargins(8, 8, 8, 8)
        self.accounts_layout.setSpacing(10)
        self.accounts_layout.addStretch()

        self.scroll_area.setWidget(self.accounts_container)
        logs_surface_layout.addWidget(self.scroll_area)
        logs.addWidget(logs_surface, 1)
        self.stack.addWidget(page_logs)

        # ================= PAGE 2: SETTINGS =================
        page_settings = QWidget()
        settings = QVBoxLayout(page_settings)
        settings.setContentsMargins(0, 0, 0, 0)
        settings.setSpacing(14)

        settings_title = QFrame()
        settings_title.setObjectName("Surface")
        st = QVBoxLayout(settings_title)
        st.setContentsMargins(22, 18, 22, 18)
        st_head = QLabel("Görünüm ve Deneyim")
        st_head.setObjectName("PageTitle")
        st_desc = QLabel("Temayı ve arayüz davranışlarını buradan yönet.")
        st_desc.setObjectName("Muted")
        st.addWidget(st_head)
        st.addWidget(st_desc)
        settings.addWidget(settings_title)

        settings_grid = QGridLayout()
        settings_grid.setSpacing(14)

        theme_card = QFrame()
        theme_card.setObjectName("Surface")
        theme_layout = QVBoxLayout(theme_card)
        theme_layout.setContentsMargins(20, 20, 20, 20)
        theme_layout.setSpacing(10)
        th = QLabel("Renk Profili")
        th.setObjectName("SectionTitle")
        theme_layout.addWidget(th)

        self.theme_group = QButtonGroup(self)
        theme_rows = [
            ("kirmizi", "Kırmızı"),
            ("mor", "Mor"),
            ("mavi", "Mavi"),
            ("yesil", "Yeşil"),
            ("sari", "Sarı"),
            ("siyah_beyaz", "Monokrom"),
        ]
        for key, label in theme_rows:
            rb = QRadioButton(label)
            rb.setChecked(key == self.current_theme)
            rb.toggled.connect(lambda checked, k=key: self.change_theme(k) if checked else None)
            self.theme_group.addButton(rb)
            theme_layout.addWidget(rb)
        theme_layout.addStretch()
        settings_grid.addWidget(theme_card, 0, 0)

        experience_card = QFrame()
        experience_card.setObjectName("Surface")
        experience_layout = QVBoxLayout(experience_card)
        experience_layout.setContentsMargins(20, 20, 20, 20)
        experience_layout.setSpacing(12)
        ex = QLabel("Deneyim")
        ex.setObjectName("SectionTitle")
        experience_layout.addWidget(ex)

        self.btn_motion_blur = QPushButton("Geçiş Efekti: AÇIK")
        self.btn_motion_blur.setCheckable(True)
        self.btn_motion_blur.setChecked(True)
        self.btn_motion_blur.toggled.connect(self._toggle_motion_blur)
        experience_layout.addWidget(self.btn_motion_blur)

        self.btn_transition_sound = QPushButton("Geçiş Sesi: KAPALI")
        self.btn_transition_sound.setCheckable(True)
        self.btn_transition_sound.toggled.connect(self._toggle_transition_sound)
        experience_layout.addWidget(self.btn_transition_sound)

        self.btn_ambient_sound = QPushButton("Fon Sesi: KAPALI")
        self.btn_ambient_sound.setCheckable(True)
        self.btn_ambient_sound.toggled.connect(self._toggle_ambient_sound)
        experience_layout.addWidget(self.btn_ambient_sound)

        wait_label_title = QLabel("Tarayıcı Bekleme Süresi")
        wait_label_title.setObjectName("SectionTitle")
        experience_layout.addWidget(wait_label_title)

        self.lbl_browser_wait = QLabel("Süre: 15 saniye")
        self.lbl_browser_wait.setObjectName("Muted")
        experience_layout.addWidget(self.lbl_browser_wait)

        self.slider_browser_wait = QSlider(Qt.Orientation.Horizontal)
        self.slider_browser_wait.setMinimum(10)
        self.slider_browser_wait.setMaximum(60)
        self.slider_browser_wait.setValue(15)
        self.slider_browser_wait.valueChanged.connect(self.update_browser_wait_time)
        experience_layout.addWidget(self.slider_browser_wait)

        note = QLabel("Ses seçenekleri sistem bildirimi olarak kullanılır; harici ses dosyası gerektirmez.")
        note.setWordWrap(True)
        note.setObjectName("Muted")
        experience_layout.addWidget(note)
        experience_layout.addStretch()
        settings_grid.addWidget(experience_card, 0, 1)

        settings.addLayout(settings_grid, 1)
        self.stack.addWidget(page_settings)

        # ================= PAGE 3: LINKS =================
        page_about = QWidget()
        about = QVBoxLayout(page_about)
        about.setContentsMargins(0, 0, 0, 0)
        about.setSpacing(14)

        hero = QFrame()
        hero.setObjectName("AccentCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(30, 30, 30, 30)
        hero_layout.setSpacing(8)

        about_brand = QLabel("NEVERMANUEL")
        about_brand.setObjectName("Brand")
        about_big = QLabel("Biz Yaptık Siz Kullanın")
        about_big.setObjectName("PageTitle")
        about_text = QLabel("Bağlantılar ve topluluk kanalları.")
        about_text.setObjectName("Muted")

        hero_layout.addWidget(about_brand)
        hero_layout.addWidget(about_big)
        hero_layout.addWidget(about_text)
        about.addWidget(hero)

        links_grid = QGridLayout()
        links_grid.setSpacing(14)

        cg_card = QFrame()
        cg_card.setObjectName("AboutCard")
        cbox = QVBoxLayout(cg_card)
        cbox.setContentsMargins(24, 24, 24, 24)
        ctitle = QLabel("CG")
        ctitle.setObjectName("SectionTitle")
        cdesc = QLabel("Topluluk bağlantısı")
        cdesc.setObjectName("Muted")
        cbutton = QPushButton("CG'ye Git")
        cbutton.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://cheatglobal.com/members/froeiys.274294/"))
        )
        cbox.addWidget(ctitle)
        cbox.addWidget(cdesc)
        cbox.addStretch()
        cbox.addWidget(cbutton)
        links_grid.addWidget(cg_card, 0, 1)

        about.addLayout(links_grid)
        about.addStretch()
        self.stack.addWidget(page_about)

        self._fade_effect = QGraphicsOpacityEffect(self.stack.currentWidget())
        self.stack.currentWidget().setGraphicsEffect(self._fade_effect)

    def update_browser_wait_time(self, value):
        self.browser_wait_time = value
        self.lbl_browser_wait.setText(f"Süre: {value} saniye")

    def _nav_button(self, text, index, checked=False):
        button = QPushButton(text)
        button.setObjectName("NavButton")
        button.setCheckable(True)
        button.setChecked(checked)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(lambda: self.switch_tab(index))
        return button

    def _metric_card(self, title, value):
        label = QLabel(value)
        label.setObjectName("Metric")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _metric_widget(self, title, value_label):
        card = QFrame()
        card.setObjectName("StatCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        label = QLabel(title)
        label.setObjectName("Eyebrow")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(value_label)
        return card

    def _toggle_motion_blur(self, checked):
        self.motion_blur_enabled = checked
        self.btn_motion_blur.setText(
            f"Geçiş Efekti: {'AÇIK' if checked else 'KAPALI'}"
        )

    def _toggle_transition_sound(self, checked):
        self.transition_sound_enabled = checked
        self.btn_transition_sound.setText(
            f"Geçiş Sesi: {'AÇIK' if checked else 'KAPALI'}"
        )

    def _toggle_ambient_sound(self, checked):
        self.ambient_sound_enabled = checked
        self.btn_ambient_sound.setText(
            f"Fon Sesi: {'AÇIK' if checked else 'KAPALI'}"
        )

    def switch_tab(self, index):
        buttons = [
            self.btn_nav_control,
            self.btn_nav_logs,
            self.btn_nav_settings,
            self.btn_nav_about,
        ]
        for i, button in enumerate(buttons):
            button.setChecked(i == index)

        titles = ["Kontrol Merkezi", "Oturumlar", "Ayarlar", "Bağlantılar"]
        self.lbl_page_title.setText(titles[index])

        if self.motion_blur_enabled:
            old_widget = self.stack.currentWidget()
            old_effect = QGraphicsOpacityEffect(old_widget)
            old_widget.setGraphicsEffect(old_effect)

            fade_out = QPropertyAnimation(old_effect, b"opacity", self)
            fade_out.setDuration(90)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            fade_out.setEasingCurve(QEasingCurve.Type.OutCubic)
            fade_out.start()

        self.stack.setCurrentIndex(index)
        new_widget = self.stack.currentWidget()

        if self.motion_blur_enabled:
            effect = QGraphicsOpacityEffect(new_widget)
            new_widget.setGraphicsEffect(effect)
            fade_in = QPropertyAnimation(effect, b"opacity", self)
            fade_in.setDuration(180)
            fade_in.setStartValue(0.0)
            fade_in.setEndValue(1.0)
            fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
            self._page_animation = fade_in
            fade_in.start()

        if self.transition_sound_enabled:
            QApplication.beep()

    def change_theme(self, theme_key):
        self.current_theme = theme_key
        self.setStyleSheet(get_theme_stylesheet(theme_key))
        self.lbl_warp_state.setText(
            "WARP • AÇIK" if self.btn_use_warp.isChecked() else "WARP • KAPALI"
        )

    def update_warp_toggle(self, checked):
        if checked:
            self.btn_use_warp.setText("WARP KULLAN: AÇIK")
            self.btn_warp_manual.setEnabled(True)
            self.lbl_warp_state.setText("WARP • AÇIK")
        else:
            self.btn_use_warp.setText("WARP KULLAN: KAPALI")
            self.btn_warp_manual.setEnabled(False)
            self.lbl_warp_state.setText("WARP • KAPALI")

    def start_process(self):
        try:
            count = int(self.entry_count.text())
        except ValueError:
            return

        if not self.btn_use_warp.isChecked():
            reply = QMessageBox.warning(
                self,
                "WARP Kapalı",
                "WARP kapalıyken IP limitine takılabilirsiniz.\n\n"
                "WARP'ı açmadan devam etmek istiyor musunuz?",
                QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.Cancel,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.total_target = count
        self.success_count = 0
        self.fail_count = 0
        self.update_stats()

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

        self.worker = GeneratorWorker(
            count,
            use_warp=self.btn_use_warp.isChecked(),
            browser_wait_time=self.browser_wait_time,
        )
        self.worker.account_created_signal.connect(self.add_account_card)
        self.worker.account_result_signal.connect(self.process_result)
        self.worker.finished_signal.connect(self.process_finished)
        self.worker.start()

    def stop_process(self):
        if self.worker:
            self.worker.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def manual_warp_reset(self):
        self.btn_warp_manual.setEnabled(False)
        self.btn_warp_manual.setText("⌛ IP Yenileniyor...")
        self.warp_worker = WarpResetWorker()
        self.warp_worker.finished_signal.connect(self.on_warp_manual_finished)
        self.warp_worker.start()

    def on_warp_manual_finished(self):
        self.btn_warp_manual.setEnabled(True)
        self.btn_warp_manual.setText("🔄 WARP IP Yenile (Manuel)")

    def add_account_card(self, info):
        card = AccountCardWidget(info["username"], info["password"], info["email"])
        self.accounts_layout.insertWidget(0, card)

    def process_result(self, success):
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
        self.update_stats()

    def update_stats(self):
        total_processed = self.success_count + self.fail_count
        self.lbl_success.setText(str(self.success_count))
        self.lbl_fail.setText(str(self.fail_count))

        if total_processed > 0:
            rate = int((self.success_count / total_processed) * 100)
            self.lbl_rate.setText(f"%{rate}")
        else:
            self.lbl_rate.setText("%0")

        if self.total_target > 0:
            prog = int((total_processed / self.total_target) * 100)
            self.progress_bar.setValue(prog)

    def process_finished(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RiotAppGUI()
    window.show()
    sys.exit(app.exec())
