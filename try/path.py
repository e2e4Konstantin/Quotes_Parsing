from pathlib import Path

db_name = Path('my.db').resolve()
csv_file = Path('file.csv').resolve()

print( Path(__name__).resolve())

print(db_name)
print(csv_file)