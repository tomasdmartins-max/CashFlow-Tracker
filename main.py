import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("transactions.csv")

CATEGORY_MAP = {
    "Supermarket": ["CONTINENTE", "PINGO DOCE"],
    "Transport": ["UBER TRIP", "GALP"],
    "Dining Out": ["RESTAURANT", "EATS"],
    "Subscriptions": ["NETFLIX", "SPOTIFY"],
    "Income": ["SALARY"]
}

df["Date"] = pd.to_datetime(df["Date"])

df["Amount"] = (df["Amount"]
    .astype(str)
    .str.replace("€", "")
    .str.replace("EUR", "")
    .str.replace(" ", "")
    .astype(float)
)

df["Type"] = df["Amount"].apply(lambda x: "Income" if x > 0 else "Expense")

def categorize_transaction(description):
    desc = str(description).upper()

    for category, keywords in CATEGORY_MAP.items():
        if any(keyword in desc for keyword in keywords):
            return category
    return "Other"

df["Category"] = (df["Description"]).apply(categorize_transaction)

df["Year_Month"] = df["Date"].dt.to_period("M")

expenses_by_category = (
    df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().abs()
) 

print("-----TOTAL SPENT PER CATEFORY-----")
print(expenses_by_category)

monthly_summary = (
    df.groupby(["Year_Month", "Type"])["Amount"].sum().unstack(fill_value=0)
)

monthly_summary["Expense"] = monthly_summary["Expense"].abs()

monthly_summary["Balance"] = monthly_summary["Income"] - monthly_summary["Expense"]

print("----- MENSAL RESUME -----")
print(monthly_summary)

plt.figure(figsize=(8, 5))
expenses_by_category.plot(kind="bar", color="skyblue")

plt.title("Total expenses by category")
plt.xlabel("Category")
plt.ylabel("Amount (€)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("expenses_by_category.png")
print("Graphic successfully saved as 'expenses_by_category.png'!")

plt.show()

monthly_summary.to_csv("monthly_summary.csv")
print("Mensal resume saved in 'monthly_summary.csv'!")