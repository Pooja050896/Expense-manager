import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_mysql_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_manager"
    )

    if connection.is_connected():
        print("Connected to MySQL")
    else:
        print("Failed to connect to MySQL")
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_records():
    with get_mysql_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses=cursor.fetchall()
        for expense in expenses:
            return expense


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_mysql_cursor() as cursor:
        cursor.execute("select * from expenses where expense_date=%s",(expense_date,))
        expenses=cursor.fetchall()
        return expenses

def insert_expenses(expense_date,amount,category,notes):
    logger.info(f"insert_expenses_for_date called with {expense_date},{amount},{category},{notes}")
    with get_mysql_cursor(commit=True) as cursor:
        cursor.execute("insert into expenses(expense_date,amount,category,notes) values (%s,%s,%s,%s)",
                       (expense_date,amount,category,notes))

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expenses_for_date {expense_date}")
    with get_mysql_cursor(commit=True) as cursor:
        cursor.execute("Delete from expenses where expense_date=%s",(expense_date,))

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_summary_for_date between {start_date} and {end_date}")
    with get_mysql_cursor() as cursor:
        cursor.execute('''select category,sum(amount) as total from expenses where expense_date between %s and %s 
                        group by category;''',
                       (start_date,end_date)),
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)
