A Python wrapper around the data provided by the ISO 10383 specification.

# Install
`$ pip install iso10383`

# Usage
The package is relatively easy to use. The `MIC` class is the enum that
contains all the entries:
```py
>>> from iso10383 import MIC
>>> MIC.xnys.value
MICEntry(
    mic='XNYS',
    market_name='NEW YORK STOCK EXCHANGE, INC.',
    market_category_code=<MCC.nspd: 6>,
    creation_date=datetime.date(2005, 5, 23),
    status=<Status.active: 0>,
    city=<City.new_york: 208>,
    operating_mic=None,
    institution_description=None,
    legel_entity_name=None,
    legal_entity_identifier=None,
    acronym='NYSE',
    iso_country_code=<ISOCC.us: 137>,
    website='www.nyse.com',
    last_update_date=datetime.date(2005, 5, 23),
    last_validation_date=None,
    expiry_date=None,
    comments=None
)

```
Each `MICEntry` has the following attributes, which correspond to those found
in [the specification](https://www.iso20022.org/market-identifier-codes):
```py
mic                     : str
market_name             : str
market_category_code    : MCC
creation_date           : datetime.date
status                  : Status
city                    : City          | None
operating_mic           : MICEntry      | None
institution_description : str           | None
legel_entity_name       : str           | None
legal_entity_identifier : str           | None
acronym                 : str           | None
iso_country_code        : ISOCC         | None
website                 : str           | None
last_update_date        : datetime.date | None
last_validation_date    : datetime.date | None
expiry_date             : datetime.date | None
comments                : str           | None
```
`MCC`, `Status`, `City`, and `ISOCC` are supporting enums that can be imported
separately.

The operating/segment column is notably not present, and is instead indicated
by the presence of the `operating_mic` attribute (that is, whether or not it is
`None`).

# Notes
Given the large number of entries in the ISO 10383 specification, hard-coding
an enum would cause major performance issues with intellisense and linters. For
this reason, a dummy enum was hardcoded, and is then replaced by deserializing
the contents at runtime. This means there is a small performance hit (on the
order of milliseconds) at runtime when the module is imported.
