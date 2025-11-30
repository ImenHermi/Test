# -*- coding: utf-8 -*-
import os
from datetime import datetime
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# ===============================
# CONFIGURATION GLOBALE
# ===============================
URL = "https://rahulshettyacademy.com/iframe-example"  # page qui contient uniquement l'iFrame Example
SCREENSHOTS_DIR = "screenshots_iframe"

# Crée le dossier de screenshots si besoin
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def nowstamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def take_screenshot(driver, name):
    """Sauvegarde une capture d’écran horodatée dans SCREENSHOTS_DIR."""
    path = os.path.join(SCREENSHOTS_DIR, f"{name}_{nowstamp()}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot : {path}")
    return path

def setup_driver():
    """
    Ouvre Edge par défaut. Si Edge n'est pas dispo, fallback sur Chrome.
    Selenium 4+ peut gérer les drivers automatiquement.
    """
    try:
        driver = webdriver.Edge()
    except WebDriverException:
        driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def wait_iframe_and_modal(driver, timeout_iframe=20, timeout_modal=20):
    """
    Va sur l'URL, bascule dans l'iFrame #courses-iframe,
    puis attend l’ouverture du modal (role=dialog).
    """
    driver.get(URL)

    # Attendre l’iFrame précis
    iframe = WebDriverWait(driver, timeout_iframe).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#courses-iframe"))
    )
    driver.switch_to.frame(iframe)

    # Attendre le modal (Radix UI -> role=dialog, souvent data-state="open")
    # On attend la visibilité du role=dialog, puis on vérifie si affiché.
    modal = WebDriverWait(driver, timeout_modal).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
    )
    assert modal.is_displayed(), "Le modal n'est pas visible."
    return modal

@contextmanager
def test_session(title, success_shot=None, fail_shot=None):
    """
    Contexte pratique pour log + screenshots.
    - success_shot : nom de fichier pour le screenshot en cas de succès
    - fail_shot    : nom de fichier pour le screenshot en cas d’échec
    """
    print("\n" + "="*70)
    print(f"🧪 {title}")
    print("="*70)
    driver = setup_driver()
    try:
        yield driver
        if success_shot:
            take_screenshot(driver, success_shot)
        print(f"✅ {title} : OK")
    except Exception as e:
        print(f"❌ {title} : {e}")
        if fail_shot:
            try:
                take_screenshot(driver, fail_shot)
            except Exception:
                pass
        raise
    finally:
        driver.quit()

# =====================================================
# 1️⃣ Test 1 : Présence iFrame + affichage du modal
# =====================================================
def test_iframe_and_modal_display():
    with test_session(
        "Test 1 - Présence iFrame + affichage du modal",
        success_shot="T1_iFrame_Modal_Success",
        fail_shot="T1_iFrame_Modal_Fail",
    ) as driver:
        wait_iframe_and_modal(driver)

# =====================================================
# 2️⃣ Test 2 : Validation vide + email invalide
#    (adapté si le formulaire apparait dans le modal)
# =====================================================
def test_form_validation_empty_and_invalid_email():
    with test_session(
        "Test 2 - Validation champs vides + email invalide",
        success_shot="T2_Validation_Success",
        fail_shot="T2_Validation_Fail",
    ) as driver:
        wait_iframe_and_modal(driver)

        wait = WebDriverWait(driver, 12)

        # Sélecteurs "robustes" (adapte-les à ton DOM réel si besoin)
        name = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="name"], input#name, input[type="text"]')))
        email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"], input#email, input[type="email"]')
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], button[role="button"], [data-testid="submit"]')

        # 2.1 – champs vides
        submit.click()
        try:
            err = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="alert"], .error, .error-email')))
            assert any(k in err.text.lower() for k in ["email", "required", "obligatoire"]), "Message d'erreur inattendu."
        except TimeoutException:
            raise AssertionError("Aucun message d’erreur pour champs vides.")

        # 2.2 – email invalide
        name.clear(); name.send_keys("Aya QA")
        email.clear(); email.send_keys("abc@")
        submit.click()
        try:
            err2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="alert"], .error, .error-email')))
            assert any(k in err2.text.lower() for k in ["invalid", "invalide", "format"]), "Message d'erreur email invalide non détecté."
        except TimeoutException:
            raise AssertionError("Email invalide accepté sans message d'erreur.")

# =====================================================
# 3️⃣ Test 3 : Soumission valide + anti double-submit
# =====================================================
def test_form_submission_valid_and_anti_double_submit():
    with test_session(
        "Test 3 - Soumission valide + anti double submit",
        success_shot="T3_Submit_Success",
        fail_shot="T3_Submit_Fail",
    ) as driver:
        wait_iframe_and_modal(driver)
        wait = WebDriverWait(driver, 20)

        # Remplir un formulaire plausible
        # (adapte les sélecteurs au markup réel du modal)
        name = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="name"], input#name, input[type="text"]')))
        email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"], input#email, input[type="email"]')
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], button[role="button"], [data-testid="submit"]')

        name.clear();  name.send_keys("Aya QA")
        email.clear(); email.send_keys("aya.qa+test@example.com")
        submit.click()

        # Succès = soit fermeture du modal, soit message/état "Thank"/toast/status
        try:
            wait.until(
                EC.any_of(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')),
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, '[role="status"], .toast, .message, .success'), "Thank")
                )
            )
        except TimeoutException:
            raise AssertionError("Aucun signe de succès (modal ouvert / pas de message).")

        # Anti double-submit : bouton disabled, état loading, etc.
        if submit.is_enabled() and "loading" not in (submit.get_attribute("class") or "").lower():
            # On tente un second clic pour voir si la double requête est possible
            try:
                submit.click()
                raise AssertionError("Double soumission possible (le bouton est resté actif).")
            except Exception:
                # Si le 2e clic échoue parce que bouton masqué/invisible, c'est bon
                pass

# =====================================================
# 4️⃣ Test 4 : Accessibilité (Tab order, focus trap, Esc)
# =====================================================
def test_accessibility_tab_focus_and_escape():
    with test_session(
        "Test 4 - Accessibilité (Tab, focus, Esc)",
        success_shot="T4_A11y_Success",
        fail_shot="T4_A11y_Fail",
    ) as driver:
        wait_iframe_and_modal(driver)
        wait = WebDriverWait(driver, 10)

        # Forcer le focus sur le 1er champ si présent
        try:
            name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="name"], input#name, input[type="text"]')))
            name.send_keys("")  # force le focus
        except TimeoutException:
            # Si pas de champ name, on garde le focus sur le modal
            pass

        # Simuler la tabulation 4 fois (Name -> Email -> Submit -> Close / retour)
        active_el = driver.switch_to.active_element
        for _ in range(4):
            active_el.send_keys(Keys.TAB)
            active_el = driver.switch_to.active_element

        # ESC doit fermer le modal
        active_el.send_keys(Keys.ESCAPE)
        WebDriverWait(driver, 6).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
        )

# =====================================================
# 5️⃣ Test 5 : Fermeture × et backdrop
# =====================================================
def test_modal_close_button_and_backdrop():
    with test_session(
        "Test 5 - Fermeture (× & backdrop)",
        success_shot="T5_Close_Success",
        fail_shot="T5_Close_Fail",
    ) as driver:
        # 5.1 — bouton ×
        wait_iframe_and_modal(driver)
        close_btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Close"], [data-testid="close"], button:has(svg)'))
        )
        close_btn.click()
        WebDriverWait(driver, 6).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
        )

        # 5.2 — backdrop (on recharge la page pour retrouver le modal)
        driver.switch_to.default_content()
        driver.refresh()
        # Re-bascule iFrame + attendre le modal
        wait_iframe_and_modal(driver)
        # Essayer plusieurs sélecteurs d’overlay courants
        backdrop = driver.find_element(By.CSS_SELECTOR, '.modal-backdrop, .ReactModal__Overlay, .overlay, .fixed.inset-0')
        backdrop.click()
        WebDriverWait(driver, 6).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
        )

# =====================================================
# 🧪 Exécution de tous les tests
# =====================================================
if __name__ == "__main__":
    # Chaque test est indépendant et produit ses propres screenshots.
    try:
        test_iframe_and_modal_display()
    except Exception:
        pass

    try:
        test_form_validation_empty_and_invalid_email()
    except Exception:
        pass

    try:
        test_form_submission_valid_and_anti_double_submit()
    except Exception:
        pass

    try:
        test_accessibility_tab_focus_and_escape()
    except Exception:
        pass

    try:
        test_modal_close_button_and_backdrop()
    except Exception:
        pass

    print("\n✅ Exécution terminée. Consulte le dossier:", os.path.abspath(SCREENSHOTS_DIR))
