import customFunc

site = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
sheet = "אתגר 22 מבוגרים - 2019 (Responses)"

session = customFunc.webFunc(site)
session.url()
customFunc.sleep(6)
session.insertinfo()
session.etgarconfirm()
session.healthissue()
session.send()
session.driver.quit()

customFunc.sleep(480)
session.check_in_sheets(sheet)

client = customFunc.auth.get_service_sheet()
report_sheet = client.open("Report").sheet1
row = ["Row below assign to Etgar22 Health issues"]
report_sheet.insert_row(row, 2)
