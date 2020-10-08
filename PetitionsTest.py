import customFunc

turkey = "https://animals-now.org/investigations/turkey/?utm_source=test&utm_medium=test&utm_campaign=test"
live_transports = "https://animals-now.org/issues/live-transports/?utm_source=test&utm_medium=test&utm_campaign=test"
cages = "https://animals-now.org/issues/cages/?utm_source=test&utm_medium=test&utm_campaign=test"
protection_act = "https://animals-now.org/issues/animal-protection-act/?utm_source=test&utm_medium=test&utm_campaign=test"
fish = "https://animals-now.org/investigations/fish/?utm_source=test&utm_medium=test&utm_campaign=test"
zoglobek = "https://animals-now.org/issues/zoglobek-lawsuit/?utm_source=test&utm_medium=test&utm_campaign=test"
fur = "https://animals-now.org/issues/fur/?utm_source=test&utm_medium=test&utm_campaign=test"
stop_cages = "https://animals-now.org/issues/stop-cages/?utm_source=test&utm_medium=test&utm_campaign=test"
spetember_2020 = "https://animals-now.org/investigations/investigation-september-2020/?utm_source=test&utm_medium=test&utm_campaign=test"

site_list = [turkey, cages, fish, zoglobek, fur, stop_cages] # protection_act, live_transports,
email_list = []  # list with the email used to signed up
petitions_list = []  # list with link to petition that the bot signed up
for site in site_list:  # sign up to petitions in the site list, for each sign up generate new info
    session = customFunc.webFunc(site)
    session.start_driver()
    session.url()
    customFunc.sleep(6)
    print('petition url: "{}"'.format(site))
    session.add_my_name_to_petition()  # DELETE WHEN A/B THE IS DONE
    customFunc.sleep(3)
    session.insert_info_to_field('FirstName', session.first_name)
    session.insert_info_to_field('LastName', session.last_name)
    session.insert_info_to_field('Email', session.email)
    session.insert_info_to_field('Phone', session.phone)
    session.petitions_send()
    email_list.append(session.email)
    petitions_list.append(site)
    session.driver.quit()
    customFunc.sleep(3)

customFunc.sleep(480)

session = customFunc.webFunc('None')
session.check_in_gmail(email_list, petitions_list)
