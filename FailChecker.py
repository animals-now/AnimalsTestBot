import customFunc

email = 'test+boteykrm883@animals-now.org' 
info = ["name", "lastn", email, "phone"]
client = customFunc.auth.get_service_sheet()  # open google sheet API client
report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure
sheet = 'הרשמה לאתגר 22 - SPANISH'
sign_up_sheet = client.open(sheet).sheet1  # open sign up form sheet
time_now = str(customFunc.datetime.today())[0:16]
row_failed = [time_now, sheet, info[2], "Sign up failed: not found in the sheet (FailChecker)"]
row_succeed_all = [time_now, sheet, info[2], "Sign up succeed and removed from google sheet (FailChecker)"]
row_remove_more = [time_now, sheet, info[2], "Sign up succeed but remove more that one row (FailChecker)"]
row_not_remove = [time_now, sheet, info[2], "Sign up succeed but found test email again (FailChecker)"]

try:
    sign_up_sheet.find(info[2])  # search if the test email found in sign up form sheet
    rows_before_delete = len(sign_up_sheet.col_values(1))
    sign_up_sheet.delete_row(sign_up_sheet.find(info[2]).row)
    rows_after_delete = len(sign_up_sheet.col_values(1))
    gap = str(rows_before_delete - rows_after_delete)
    row_failed.append(gap)
    row_succeed_all.append(gap)
    row_remove_more.append(gap)
    row_not_remove.append(gap)
    try:
        sign_up_sheet.find(info[2])
        report_sheet.insert_row(row_not_remove, 2)
    except customFunc.gspread.CellNotFound:
        if rows_before_delete - rows_after_delete > 1:
            report_sheet.insert_row(row_remove_more, 2)
        else:
            report_sheet.insert_row(row_succeed_all, 2)

except customFunc.gspread.CellNotFound:
    report_sheet.insert_row(row_failed, 2)

