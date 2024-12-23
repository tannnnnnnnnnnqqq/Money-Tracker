#install matplotlib - allow us to plot and see the graph
#and panda - allow us to easily categorized & search for data within the csp file

#collect data from the user
import pandas as pd #allow us to load in the csv file make work easier
import csv
from datetime import datetime #modulus built in python
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    #variables
    CSV_FILE = "finance_data.csv"
    COLUMS = ["date", "amount", "category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod #this will have access to the class itself but won't have access to its instance
    def initialize_csv(cls):
        #try to read csv file
        try:
            pd.read_csv(cls.CSV_FILE) #attempt to read this cls
        except FileNotFoundError: #file not work , create the file
            #DataFrame = object within pandas that allows us to access different row and column from a csv file
            df = pd.DataFrame(columns=cls.COLUMS) #specific 4 columns inside csv file
            #export dataFrame to csv file
            df.to_csv(cls.CSV_FILE, index=False) #not going to sort data frame by indexing it

    #add entry to file
    @classmethod
    def add_entry(cls, date, amount, category, description):
        #use CSV writer to write into file #create a dictionary that contain all data that we want to add in csv file
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        } #store in python dictionary to write in correct column when we use CSV writer
        #append mode: pending to the end of file not overwritting / delete / make new one, just open and putting cursor in the end of the file
        #very useful syntax with cuz python will automatically handle closing file for you
        with open(cls.CSV_FILE, "a", newline="") as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMS) #DicWriter=take a dictionary & write into CSV file
            writer.writerow(new_entry)
        print("Entry added successsfully!")

    @classmethod
    #give all the transaction within date range
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT) #not just to access row but to access all of the columns
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        #mask = something that we can apply to the different rows inside of a dataframeto see if we should select that row or not
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask] #returns a new filtered dataframe


        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummarry:")
            print(f"Toal Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index('date', inplace=True)
    #seperata dataframe (income and expense)
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label = "Income", color= "g")
    plt.plot(expense_df.index, expense_df["amount"], label = "Expense", color= "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income andExpenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    main()