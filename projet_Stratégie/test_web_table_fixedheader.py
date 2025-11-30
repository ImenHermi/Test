from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Lancer Chrome ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    print("\n===== TEST AUTOMATISÉ – WEB TABLE FIXED HEADER =====")

    # --- Ouvrir la page ---
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")
    time.sleep(2)

    # --- TC-01 : Vérifier l'affichage du tableau et du header ---
    table = driver.find_element(By.ID, "product")
    assert table.is_displayed(), "Le tableau n'est pas visible"

    header = driver.find_element(By.XPATH, "//div[@class='tableFixHead']//thead")
    assert header.is_displayed(), "Le header n'est pas affiché"

    print("TC-01 OK : Tableau et header affichés correctement")

    # --- TC-02 : Vérifier que le header reste fixe lors du scroll ---
    driver.execute_script("arguments[0].scrollIntoView();", table)
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)

    assert header.is_displayed(), "Le header n'est plus visible après scroll"
    print("TC-02 OK : Header reste fixe pendant le scroll")

    # --- TC-03 : Vérifier les données du tableau ---
    rows = driver.find_elements(By.XPATH, "//div[@class='tableFixHead']//tbody/tr")
    assert len(rows) > 0, "Aucune ligne dans le tableau"

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        assert len(cells) == 4, "Le tableau n'a pas 4 colonnes"
        for cell in cells:
            assert cell.text.strip() != "", "Une cellule est vide"

    print("TC-03 OK : Toutes les lignes contiennent des données")

    # --- TC-04 : Vérifier que tous les prix sont numériques ---
    prices = driver.find_elements(By.XPATH, "//div[@class='tableFixHead']//tbody/tr/td[4]")

    for price in prices:
        assert price.text.isdigit(), f"Valeur non numérique détectée : {price.text}"

    print("TC-04 OK : Tous les prix sont numériques")

    print("\n✔ Tous les tests Web Table Fixed Header sont PASS")

except AssertionError as e:
    print("❌ Test échoué →", e)

finally:
    driver.save_screenshot("screenshot_webtable_fixedheader.png")
    driver.quit()

print("===== FIN DU TEST =====")



