from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Lancer Chrome ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    print("\n===== TEST SWITCH WINDOW =====")

    # --- TC-01 : Ouvrir la page ---
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")
    time.sleep(2)

    open_window_btn = driver.find_element(By.ID, "openwindow")
    assert open_window_btn.is_displayed(), "Le bouton Open Window n'est pas visible"
    print("TC-01 OK : Bouton Open Window affiché")

    # --- TC-02 : Cliquer et passer à la nouvelle fenêtre ---
    main_window = driver.current_window_handle
    open_window_btn.click()
    time.sleep(2)

    all_windows = driver.window_handles
    assert len(all_windows) > 1, "La nouvelle fenêtre ne s'est pas ouverte"
    print("TC-02 OK : Nouvelle fenêtre ouverte")

    # Passer à la nouvelle fenêtre
    for w in all_windows:
        if w != main_window:
            driver.switch_to.window(w)
            break

    # --- TC-03 : Vérifier l'URL de la nouvelle fenêtre ---
    current_url = driver.current_url.lower()

    assert ("rahulshettyacademy" in current_url or "qaclickacademy" in current_url), \
        f"URL incorrecte : {current_url}"

    print("TC-03 OK : URL correcte dans la nouvelle fenêtre")

    # --- TC-04 : Retour à la fenêtre principale ---
    driver.close()  # ferme la nouvelle fenêtre
    driver.switch_to.window(main_window)
    time.sleep(1)

    assert driver.current_url == "https://rahulshettyacademy.com/AutomationPractice/", \
        "Retour incorrect à la fenêtre principale"
    print("TC-04 OK : Retour correct à la fenêtre principale")

except AssertionError as e:
    print("❌ Test échoué →", e)

finally:
    time.sleep(1)
    driver.save_screenshot("screenshot_switchwindow.png")
    driver.quit()

print("===== FIN DU TEST =====")


