# Day 1: API Data Analysis (Pesa Pulse)

## Approach
I fetched the customer directory from the JSONPlaceholder Users API using
`requests`, with a timeout, a status code check and clear messages for
network failures. I explored the nested structure with a recursive
function, extracted a flat set of attributes per customer, and answered
"where are our customers?" first with sets and dictionaries, then with
pandas. Finally I exported the results to CSV and saved two charts.

## How to run
1. Install the packages: `pip install -r requirements.txt`
2. Run the analysis from the project folder: `python analysis.py`

Outputs are saved in the `output/` folder: `customers.csv`,
`city_counts.csv`, `customer_distribution.png` and
`email_domain_distribution.png`.

## Nested structure
Each customer record has two nested attributes: `address` (a dictionary
that itself contains `geo`) and `company` (a dictionary). The deepest
attribute is the latitude, reached with
`customer["address"]["geo"]["lat"]`. Latitude and longitude arrive as
strings, so I converted them to floats.

## Findings
1. There are 10 customers in 10 unique cities. Every customer is in a
   different city, so there is no city with a concentration of customers
   and marketing would have to plan regional campaigns city by city
   rather than target a few hubs.
2. The most common email top-level domain is `.biz` with 3 customers.
   Each of `.ca`, `.info`, `.io`, `.me`, `.net`, `.org` and `.tv` has 1.
3. My hand-written counts match the pandas `value_counts()` results for
   both city and email domain.

## Which chart is more useful
The city chart (`customer_distribution.png`) is flat because every city
appears exactly once, so it gives marketing nothing to compare. The email
domain chart (`email_domain_distribution.png`) is more useful because it
shows a clear leader (`.biz`) and a spread across the other domains.

## Assumptions
- The API returns the same 10 customers with the same structure.
- The email domain is the top-level domain: the text after the last dot
  in the part after the `@` sign.
- Ties in the counts are sorted alphabetically so the output is stable.