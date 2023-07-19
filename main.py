from tasks import handling_quotes, handling_resource

paths = {
    "home": r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources",
    "office": r" ",
}

source_files = {
    0: (r"template_3_68_v_1.xlsx", "name"),
    3: (r"template_3_68.xlsx", "name"),
    4: (r"template_4_68.xlsx", "name"),
    5: (r"template_5_67.xlsx", "name"),
    6: (r"res_68.xlsx", "1")
}


pl = "home" # "office"

if __name__ == "__main__":
    fn = 5
    handling_quotes((source_files[fn][0], paths[pl], source_files[fn][1]))

    # fn = 6
    # handling_resource((source_files[fn][0], paths[pl], source_files[fn][1]))
