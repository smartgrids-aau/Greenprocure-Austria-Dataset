# Greenprocure Austria Dataset

Municipal procurement bookings of two Austrian municipalities of the climate and energy model region (KEM) Carnica Rosental, 2018–2022. The data set is used for ABC/XYZ analyses of the CO2 equivalents of public procurement.

This repository contains data only. The analysis code lives in separate repositories.

## Contents

```
Dataset/
  MunicipalityA.xlsx   bookings of municipality A (7,401 rows, 2018–2022)
  MunicipalityA.json   column mapping and product groups used by the analysis code
  MunicipalityB.xlsx   bookings of municipality B (2,673 rows, 2018–2022)
  MunicipalityB.json
```

The municipalities are anonymised. Column names are German, as exported from the municipal accounting systems. Personal names in booking texts are replaced by `X`, life-event bookings (birthdays, births, weddings, anniversaries, deaths, retirement) and personal roles (e.g. mayor, head of office, school staff) are generalised, address fragments, vehicle registration numbers and serial numbers are removed, a cost-centre name in municipality A is replaced by `[anon]`, and the document properties of the xlsx files (author, organisation, timestamps) are removed. Amounts, dates, years, account groups and masses are unchanged.

| File | Columns used by the analysis | Meaning |
|---|---|---|
| A | `Buchungsdatum`, `Jahr`, `Soll Netto`, `Text`, `Postbezeichnung`, `Menge (in Gramm)` | booking date, year, net cost (EUR), booking text, account group, mass in grams |
| B | `Buchungsdatum`, `Jahr`, `Betrag in Hauswährung`, `Text`, `Menge (in Gramm)` | booking date, year, amount (EUR), booking text, mass in grams |

The `.json` files define which column is date, year, cost, product text and split column, and how account groups map to fuels, consumables and durable goods.

## License

see LICENSE.txt