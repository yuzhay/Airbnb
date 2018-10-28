from datetime import date

def add_months(sourcedate, months=1):
  """Add extra month to date"""
  month = sourcedate.month - 1 + months
  year = int(sourcedate.year + month / 12)
  month = month % 12 + 1
  return date(year, month, 1)
