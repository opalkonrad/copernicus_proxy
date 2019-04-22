from downloader.constants import formats, days, months, years

years_list = []
months_list = []
days_list = []
formats_list = []

for i in range(years.MIN, years.MAX + 1):
    years_list.append((i, i))

for i in range(0, 12):
    months_list.append((i + 1, months.names[i]))

for i in range(days.MIN, days.MAX + 1):
    days_list.append((i, i))

for f in formats.list:
    formats_list.append((f.extension, f.name))

years = tuple(years_list)
months = tuple(months_list)
days = tuple(days_list)
formats = tuple(formats_list)
