
import pandas as pd



fp = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\production\Quotes_Parsing\src\options.xlsx"

# df = pd.read_csv(fp, delimiter=';', header=None, encoding='cp1251', dtype=pd.StringDtype())
df = pd.read_excel(fp, header=None,  dtype=pd.StringDtype())
print(df.head(10))


options_synonym: dict[str: list[str]] = {}

for x in df.to_records(index=False):

    options_synonym[x[0]] = [y for y in list(x)[1:] if not pd.isna(y)]
    print(options_synonym[x[0]])

