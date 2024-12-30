#Money Tracker
A simple, Python-based money tracking application that allows users to record, manage, and visualize their financial transactions. This tool is ideal for tracking income and expenses, summarizing data, and plotting trends over time.

#Features
Add Transactions: Easily record the date, amount, category, and description of each transaction.
View Summary: Filter transactions by date range and view a summary of income, expenses, and net savings.
Visualize Data: Plot income and expense trends over time using matplotlib.

#Prerequisites
Python 3.8 or higher
Required Python libraries:
pandas
matplotlib

#CSV File
The application uses a CSV file (finance_data.csv) to store transaction data. If the file does not exist, it will be created automatically.

#File Structure
main.py: Contains the main program logic.
data_entry.py: Handles user input and validation.
finance_data.csv: Stores transaction data (auto-generated).
