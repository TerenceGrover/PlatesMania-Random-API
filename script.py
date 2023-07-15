import json

def main():
  with open ('countries.json') as f:
      countries = json.load(f)['Country']

  arr = [
  "AD", "AE", "AL", "AM", "AT", "AZ", "BA", "BE", "BG", "BR", "BY", "CA", "CH", "CN", "CZ", "CY",
  "DE", "DK", "EE", "EG", "ES", "FI", "FR", "GE", "GR", "HK", "HR", "HU", "ID", "IE", "IL", "IQ",
  "IT", "JP", "KG", "KH", "KR", "KZ", "LI", "LT", "LU", "LV", "MA", "MC", "ME", "MD", "MK", "MN",
  "MT", "MX", "MY", "NL", "NO", "NZ", "PL", "PS", "PT", "RO", "RS", "RU", "SA", "SE", "SG", "SI",
  "SK", "SM", "TH", "TJ", "TR", "UA", "UK", "US", "SU", "UZ", "VN"
]
  arr = [x.lower() for x in arr]

  print('In json but not in website:')
  for country, country_code in countries.items():
    if country_code not in arr:
      print(country_code, country)


  print('In website but not in json:')
  for country_code in arr:
    if country_code not in countries.values():
      print(country_code)


main()