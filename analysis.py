"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("output")


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}.")
            return []
        return response.json()
    except requests.exceptions.Timeout:
        print("The request timed out. Check your connection and try again.")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the API. Check your internet connection.")
    except requests.exceptions.RequestException as error:
        print(f"Something went wrong with the request: {error}")
    return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    spacing = "    " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{spacing}{key}: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 1)
    elif isinstance(record, list):
        for i, item in enumerate(record):
            print(f"{spacing}[{i}]: {type(item).__name__}")
            if isinstance(item, (dict, list)):
                explore(item, indent + 1)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []
    for c in customers:
        rows.append({
            "customer_id": c["id"],
            "name": c["name"],
            "username": c["username"],
            "email": c["email"],
            "email_domain": c["email"].split("@")[1].split(".")[-1],
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),
            "longitude": float(c["address"]["geo"]["lng"]),
            "company": c["company"]["name"],
            "website": c["website"],
        })
    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c["address"]["city"] for c in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop (no Counter, no pandas)."""
    counts = {}
    for c in customers:
        city = c["address"]["city"]
        counts[city] = counts.get(city, 0) + 1
    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    tlds = [c["email"].split("@")[1].split(".")[-1] for c in customers]
    return {t: tlds.count(t) for t in set(tlds)}


def sort_counts(counts: dict[str, int]) -> dict[str, int]:
    """Sort from most to least common, ties A to Z."""
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert the list of flat dicts into a pandas DataFrame."""
    return pd.DataFrame(rows)


def export_csvs(df: pd.DataFrame, by_city: dict[str, int], folder: Path = OUTPUT_DIR) -> None:
    """Write customers.csv and city_counts.csv without the pandas index."""
    folder.mkdir(parents=True, exist_ok=True)
    df.to_csv(folder / "customers.csv", index=False)

    city_df = pd.DataFrame(list(by_city.items()), columns=["city", "customer_count"])
    city_df.to_csv(folder / "city_counts.csv", index=False)


def plot_distribution(
    counts: dict[str, int],
    path: Path,
    title: str = "Customers by City",
    xlabel: str = "City",
) -> None:
    """Save a labelled bar chart of the distribution to path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of customers")
    plt.yticks(range(0, max(values) + 1))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


if __name__ == "__main__":
    customers = get_customers()
    if not customers:
        raise SystemExit("No customer data retrieved. Stopping.")

    print("Structure of the first customer:")
    explore(customers[0])

    rows = extract_attributes(customers)
    cities = unique_cities(customers)
    print(f"\nUnique cities: {len(cities)} for {len(customers)} customers")
    print("Every customer is in a different city, so marketing must plan "
          "regional campaigns city by city.")

    by_city = sort_counts(city_counts(customers))
    by_domain = sort_counts(email_domain_counts(customers))

    df = to_dataframe(rows)
    print(f"\nDataFrame shape: {df.shape}")
    print(df.dtypes)
    print("\nPandas city counts match:", df["city"].value_counts().to_dict() == by_city)
    print("Pandas domain counts match:",
          df["email_domain"].value_counts().to_dict() == by_domain)

    export_csvs(df, by_city)

    city_chart = OUTPUT_DIR / "customer_distribution.png"
    domain_chart = OUTPUT_DIR / "email_domain_distribution.png"
    plot_distribution(by_city, city_chart)
    plot_distribution(
        by_domain, domain_chart,
        title="Customers by Email Domain", xlabel="Email top-level domain",
    )

    top_city, top_n = next(iter(by_city.items()))
    print("\n--- Findings ---")
    print(f"Customers retrieved : {len(customers)}")
    print(f"Unique cities       : {len(cities)}")
    print(f"Most common city    : {top_city} ({top_n})")
    print(f"Email domains       : {by_domain}")
    print(f"Chart saved to      : {city_chart.as_posix()}")
    print(f"Second chart        : {domain_chart.as_posix()}")