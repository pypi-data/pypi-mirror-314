from selenium_stealth import stealth
import undetected_chromedriver as uc
import random
import sys
import os

# 1. Alterar o User-Agent
def set_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

# 2. Configurar e iniciar o navegador com undetected_chromedriver
def launch_browser(download_dir):
    # Configurações para o Chrome
    options = uc.ChromeOptions()

    # Alterar o User-Agent
    options.add_argument(f"user-agent={set_user_agent()}")

    # Default's
    profile = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        # 'plugins.always_open_pdf_externally': True, # É detectado como automação
        'download.default_directory': download_dir,
    }

    options.add_experimental_option('prefs', profile)

    # Configurações para reduzir detecção
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    # Inicializar o navegador com undetected_chromedriver
    try: driver = uc.Chrome(options=options, use_subprocess=True)
    except: driver = uc.Chrome(options=options, use_subprocess=True)

    return driver

def apply_stealth(driver):
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )

def start_instance(caminho):
    driver = launch_browser(caminho)
    apply_stealth(driver)
    print(" - Instância driver iniciada com sucesso")
    return driver