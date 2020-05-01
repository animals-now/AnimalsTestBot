import customFunc

site = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
sheet = "פורם של הרשמה לאתגר 22 - SPANISH HEALTH (Responses)"

session = customFunc.webFunc(site)
session.url()
customFunc.sleep(6)
session.insertinfo()
session.ch_confirm_sixteen()
session.healthissue()
session.send()
session.driver.quit()

customFunc.sleep(480)
session.check_in_sheets(sheet)
