from database import get_connection

connection = get_connection()

cursor = connection.cursor()

columns = cursor.execute(
    "PRAGMA table_info(learning_progress)"
).fetchall()

print("Learning Progress Table")
print("=" * 60)

for column in columns:
    print(
        f"Column: {column['name']}"
    )
    print(
        f"Type:   {column['type']}"
    )
    print(
        f"NotNull: {column['notnull']}"
    )
    print(
        f"Default: {column['dflt_value']}"
    )
    print("-" * 60)

connection.close()