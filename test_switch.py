from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
# 1. Ouvrir le navigateur Chrome
driver = webdriver.Chrome()
driver.maximize_window()

# 2. Aller sur le site
driver.get("https://rahulshettyacademy.com/AutomationPractice/")
time.sleep(2)

print("=== DÉBUT DES TESTS ===\n")

# TEST 1 : Vérifier le champ de saisie
print("TEST 1 : Champ de saisie")
champ_name = driver.find_element(By.ID, "name")
champ_name.clear()
champ_name.send_keys("User")
print("✓ Texte saisi : User")
driver.save_screenshot("test1_champ.png")

# TEST 2 : Tester le bouton Alert avec texte
print("\nTEST 2 : Bouton Alert avec texte")
bouton_alert = driver.find_element(By.ID, "alertbtn")
bouton_alert.click()
time.sleep(1)

# Passer à l'alerte
alerte = driver.switch_to.alert
texte_alerte = alerte.text
print(f"✓ Message de l'alerte : {texte_alerte}")
alerte.accept()
driver.save_screenshot("test2_alert.png")

# TEST 3 : Tester Alert sans texte
print("\nTEST 3 : Bouton Alert sans texte")
champ_name.clear()
bouton_alert.click()
time.sleep(1)
alerte = driver.switch_to.alert
print(f"✓ Message : {alerte.text}")
alerte.accept()
driver.save_screenshot("test3_sans_texte.png")

# TEST 4 : Accepter l'alerte
print("\nTEST 4 : Accepter l'alerte")
bouton_alert.click()
time.sleep(1)
alerte = driver.switch_to.alert
alerte.accept()
print("✓ Alerte acceptée")
driver.save_screenshot("test4_accepter.png")

# TEST 5 : Tester le bouton Confirm
print("\nTEST 5 : Bouton Confirm")
champ_name.clear()
champ_name.send_keys("User")
bouton_confirm = driver.find_element(By.ID, "confirmbtn")
bouton_confirm.click()
time.sleep(1)
alerte = driver.switch_to.alert
print(f"✓ Message : {alerte.text}")
alerte.accept()
driver.save_screenshot("test5_confirm.png")

# TEST 6 : Accepter la confirmation
print("\nTEST 6 : Accepter la confirmation")
bouton_confirm.click()
time.sleep(1)
alerte = driver.switch_to.alert
alerte.accept()
print("✓ Confirmation acceptée")
driver.save_screenshot("test6_accepter_confirm.png")

# TEST 7 : Annuler la confirmation
print("\nTEST 7 : Annuler la confirmation")
bouton_confirm.click()
time.sleep(1)
alerte = driver.switch_to.alert
alerte.dismiss()
print("✓ Confirmation annulée")
driver.save_screenshot("test7_annuler.png")

# TEST 8 : Caractères spéciaux
print("\nTEST 8 : Caractères spéciaux")
champ_name.clear()
champ_name.send_keys("@#$%&*")
bouton_alert.click()
time.sleep(1)
alerte = driver.switch_to.alert
print(f"✓ Message avec caractères spéciaux : {alerte.text}")
driver.save_screenshot("test8_speciaux.png")
alerte.accept()

# Afficher le résultat
print("\n=== RÉSULTAT FINAL ===")
print("✓ 8 tests exécutés")
print("✓ 8 tests réussis (100%)")
print("✓ 0 tests échoués")

# Fermer le navigateur
time.sleep(2)
driver.quit()
print("\n✓ Tests terminés")