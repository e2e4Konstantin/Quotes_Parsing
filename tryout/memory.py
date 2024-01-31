from utilites import SourceData
import contextlib
import io
import sys
import psutil
import gc
import os
from wmi import WMI
import time
# https://stackoverflow.com/questions/938733/total-memory-used-by-python-process/21632554#21632554
def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

def get_process_memory():
    Byte_Megabyte = 1024.0 ** 2
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / Byte_Megabyte

def memory():
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    # print(result)
    return int(result[0].WorkingSet)

def handling_quotes(file_data: tuple[str, str, str]):

    print(f"{memory()/(1024.0 ** 2)=:.3f} Mb")

    # was_memory = psutil.virtual_memory().used / Byte_Megabyte
    # print(f"{ was_memory = :.3f} MB {psutil.Process().memory_info().rss / Byte_Megabyte = }\n")

    mem_before = get_process_memory()
    start = time.time()
    print(f"memory before: {mem_before:.3f} Mb")

    data = SourceData(file_name=file_data[0], file_path=file_data[1], sheet_name=file_data[2])
    print(data.df.info(verbose=False), "\n")

    print(f"{memory()/(1024.0 ** 2)=:.3f} Mb")
    mem_after = get_process_memory()
    print(f"memory before: {mem_before:.3f}, after: {mem_after:.3f}, consumed: {mem_after - mem_before:.3f}")

    # after_get_data_memory = psutil.virtual_memory().used / Byte_Megabyte
    # print(f"{ after_get_data_memory = :.3f} MB, разница: {was_memory-after_get_data_memory:.3f} MB\n {psutil.Process().memory_info().rss / Byte_Megabyte = }")


    del data
    gc.collect()

    print(f"{memory()/(1024.0 ** 2)=:.3f} Mb")
    elapsed_time = elapsed_since(start)
    mem_free = get_process_memory()
    print(f"memory free: {mem_free:.3f}, size after memory release: {mem_after - mem_free:.3f}; exec time: {elapsed_time}")
    # became_memory = psutil.virtual_memory().used / Byte_Megabyte
    # print(f"{ became_memory = :.3f} MB, освободили: {became_memory-after_get_data_memory:.3f}  MB \n{psutil.Process().memory_info().rss / Byte_Megabyte = }")


paths = {"home": r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources", "office": r" ",}
source_files = {0: (r"template_3_68_v_1.xlsx", "name"),3: (r"template_3_68.xlsx", "name"),4: (r"template_4_68.xlsx", "name"),   5: (r"template_5_67.xlsx", "name"),    6: (r"res_68.xlsx", "1")}


pl = "home" # "office"

if __name__ == "__main__":
    fn = 5
    handling_quotes((source_files[fn][0], paths[pl], source_files[fn][1]))