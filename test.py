from google_sheets import GoogleSheets

from icecream import ic

obj = GoogleSheets()
values = obj.get_values()

for row in values:
    ic(row)
    