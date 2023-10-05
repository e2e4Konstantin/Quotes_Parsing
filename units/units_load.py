import os
import pandas as pd


def get_data() -> pd.DataFrame:
    parquet_file = 'template_all_output.gzip'

    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Parsing\output"
    # file_name = r"template_all_output.xlsx"
    # file_name = os.path.join(path, file_name)
    # sheet_name = "Options"
    # df = pd.read_excel(io=file_name, sheet_name=sheet_name, dtype=pd.StringDtype())
    # df = df[['PRESSMARK', 'PARAMETER_TITLE', 'UNIT_OF_MEASURE']]
    # df.to_parquet(parquet_file, compression='gzip')

    df = pd.read_parquet(parquet_file)
    return df


def get_units() -> pd.DataFrame:
    parquet_file = 'units_measurement.gzip'
    #
    # path = r"C:\Users\kazak.ke\PycharmProjects\Quotes_Parsing\units"
    # file_name = r"units_measurement.xlsx"
    # file_name = os.path.join(path, file_name)
    # sheet_name = "load"
    # df = pd.read_excel(io=file_name, sheet_name=sheet_name, dtype=pd.StringDtype())
    # df = df.fillna(' ')
    # df['TARGET'] = df[['right', 'wrong']].apply(",".join, axis=1).str.strip().str.lower()
    # df['TARGET'] = df['TARGET'].apply(lambda x: x if not x.endswith(',') else x[:-1])
    # df = df[['abbreviation', 'TARGET']]
    # df.to_parquet(parquet_file, compression='gzip')
    # #
    df = pd.read_parquet(parquet_file)
    return df


def look_up_units(target: str, df: pd.DataFrame) -> str | None:
    standard = df['abbreviation'].tolist()
    if target in standard:
        return target
    else:
        for record in df.to_records(index=False):
            variants = [goals.strip() for goals in record['TARGET'].split(',')]
            variants = set(variants)
            if target.lower() in variants:
                return record['abbreviation']
    return None


if __name__ == '__main__':
    data = get_data()
    print(data.info())
    units = get_units()
    print(units.info())

    empty_measure = data["UNIT_OF_MEASURE"].isna().sum()
    print(f"единицы измерения не заполнены: {empty_measure} раз.")
    raw = data["UNIT_OF_MEASURE"].dropna().unique().tolist()
    # if None in raw:
    #     raw.remove(None)

    # print(len(raw), raw)

    # r = ['°С', 'кВА']

    bad = []

    print(f"нужны замены:")
    for x in raw:
        standard = look_up_units(x, units)
        if not standard:
            bad.append(x)
        else:
            if x != standard:
                print(f"{x!r} --> {standard!r}")
    print(bad)






