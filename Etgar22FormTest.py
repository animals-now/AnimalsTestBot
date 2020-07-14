import customFuncs

site = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
sheet = "אתגר 22 מבוגרים - 2019 (Responses)"
sheet1 = "אתגר 22 - טלפניות (Responses)"

session = customFunc.webFunc(site)
session.url()
customFunc.sleep(6)
session.insertinfo()
session.etgarconfirm()
session.send()
session.driver.quit()

customFunc.sleep(480)
session.check_in_sheets(sheet)
session.check_in_sheets(sheet1)
