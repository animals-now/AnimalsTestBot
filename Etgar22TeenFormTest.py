import customFunc

site = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
sheet = "אתגר 22 נוער - 2019 (Responses)"

session = customFunc.webFunc(site)
session.start_driver()
session.url()
customFunc.sleep(6)
session.insert_info_to_field('FirstName', session.first_name)
session.insert_info_to_field('LastName', session.last_name)
session.insert_info_to_field('Email', session.email)
session.insert_info_to_field('Phone', session.phone)
session.etgarconfirm()
session.teen_check_box()
session.send()
age = str(customFunc.randint(14, 17))
parent_phone = "067" + str(customFunc.randint(1000000, 9999999))
customFunc.sleep(6)
session.insert_info_to_field('Age', age)
session.send()
customFunc.sleep(3)
session.insert_info_to_field('Phone', parent_phone)
session.send()
session.driver.quit()

customFunc.sleep(600)
session.check_in_sheets(sheet)
