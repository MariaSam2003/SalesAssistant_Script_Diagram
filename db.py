import pyodbc

def connect():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-JLPUN7T\\SQLEXPRESS;"  
        "DATABASE=SalesDB;"     
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

# Get products by category
def get_products_by_category(category: str):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT Name,Category, Price, Rating FROM Products WHERE Category = ?"
    cursor.execute(query, (category,))
    results = cursor.fetchall()
    conn.close()
    return results


# Get customer profile by name or phone number
def get_customer_profile(phone: str):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT Name, JobOccupation, DomaineOfInterest, Preferences FROM Customers WHERE PhoneNb = ?"
    cursor.execute(query, (phone,))
    result = cursor.fetchone()
    conn.close()
    return result

def search_products_by_name(keyword: str):
    cursor = connect().cursor()
    cursor.execute("SELECT name, price, rating FROM Products WHERE name LIKE ?", (f"%{keyword}%",))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return f"No products found matching '{keyword}'."

    response_lines = []
    for name, price, rating in rows:
        try:
            price = float(price)
            rating = float(rating)
            response_lines.append(f"{name} - ${price:.2f}, Rating: {rating:.1f}/10")
        except ValueError:
            response_lines.append(f"{name} - Invalid price or rating")
    return "\n".join(response_lines)