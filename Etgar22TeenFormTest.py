import customFunc

site = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
sheet = "אתגר 22 נוער - 2019 (Responses)"

session = customFunc.webFunc(site)
session.url()
customFunc.sleep(6)
session.insertinfo()
session.etgarconfirm()
session.teen()
session.send()
session.driver.quit()

customFunc.sleep(300)
session.check_in_sheets(sheet)
