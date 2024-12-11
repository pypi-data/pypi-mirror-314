# import argparse
# import os
# import time

# from pysftp import CnOpts, Connection

# cnopts = CnOpts()
# cnopts.hostkeys = None

# credentials = {
#     "host": "mip.ebay.com",
#     "port": 22,
#     "username": "zone-smart",
#     "password": "v^1.1#i^1#r^1#I^3#f^0#p^3#t^Ul4xMF82OjQ5REY2QzJDQjM2RTVERDE5MDIyRTAwNDU3NUQ3MzVBXzNfMSNFXjI2MA==",
# }

# mip_dirs = [
#     "availability",
#     "deleteInventory",
#     "distribution",
#     "inventory",
#     "location",
#     "order",
#     "orderfulfillment",
#     "product",
#     "reports",
# ]


# parser = argparse.ArgumentParser(description="Получение результатов загрузки eBay feed")


# class StoreNameValuePair(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         n, v = values.split("=")
#         setattr(namespace, n, v)


# parser.add_argument("file_name", action=StoreNameValuePair, help="Имя файла")
# parser.add_argument(
#     "localpath",
#     action=StoreNameValuePair,
#     help="Путь на локальной машине для загруженного файла",
# )
# parser.add_argument(
#     "mip_dir",
#     action=StoreNameValuePair,
#     help="Папка на сервере mip.ebay.com, в которую был загружен feed-файл",
# )
# args = parser.parse_args()

# file_name = args.file_name
# print("Имя ранее загруженного файла:", file_name)

# localpath = os.path.join(os.path.dirname(__file__), args.localpath, file_name)
# localpath_dir = os.path.dirname(localpath)
# print("Результаты сохранятся в файл:", localpath)
# if not os.path.isdir(localpath_dir):
#     raise AttributeError(f"Указанная папка {localpath_dir} не существует на локальной машине")

# mip_dir = args.mip_dir
# print("Папка для поиска результатов в системе eBay:", mip_dir)
# if mip_dir not in mip_dirs:
#     raise AttributeError(
#         f"Недопустимая папка для поиска результатов загрузки: {mip_dir}\n" f"Допустимые папки: {mip_dirs}"
#     )


# def callback(ready, total):
#     print(f"File was {'un' if ready!=total else ''}successfully downloaded:")
#     print(f"{ready} of {total} bytes downloaded")


# def get_similar(filename, dirname):
#     print("Поиск файлов в", dirname)
#     print("Содержимое папки:", sftp.listdir(dirname))
#     files = [
#         os.path.join(dirname, file)
#         for file in sftp.listdir(dirname)
#         if (os.path.splitext(filename)[0] in file) and file.endswith(".csv")
#     ]
#     return files


# def get_last_modified(files):
#     dt_objs = []
#     for file in files:
#         dt_str = "-".join(os.path.basename(file).split("-")[1:7])
#         dt_obj = time.strptime(dt_str, "%b-%d-%Y-%H-%M-%S")
#         dt_objs.append((dt_obj, file))
#     if dt_objs:
#         return max(dt_objs, key=lambda x: x[0])[1]


# with Connection(**credentials, cnopts=cnopts) as sftp:
#     root_dir = os.path.join("store", mip_dir)
#     sftp.chdir(root_dir)

#     processed_files = []
#     for date_dir in sftp.listdir("output"):
#         processed_files += get_similar(file_name, os.path.join("output", date_dir))

#     unprocessed_files = []
#     if "inprogress" in sftp.listdir(""):
#         # возможно папка тоже содержит вложенные папки по датам
#         unprocessed_files = get_similar(file_name, "inprogress")

#     found_files = processed_files + unprocessed_files
#     print("Все найденные файлы:", found_files)

#     last_modified = get_last_modified(found_files)
#     print("Результаты последней загрузки:", last_modified)
#     if "output" in last_modified:
#         remotepath = last_modified
#     else:
#         print(f"Файл {last_modified} находится в обработке системой eBay, результаты пока недоступны.")
#         remotepath = get_last_modified(filter(lambda file_path: "output" in file_path, found_files))
#         if remotepath:
#             print(f"Загружен последний обработанный системой eBay файл с тем же именем {remotepath}.")
#         else:
#             print(f"Обработанных системой eBay файлов с тем же именем {file_name} не найдено.")

#     if remotepath:
#         sftp.get(remotepath=remotepath, localpath=localpath, callback=callback)
#         print(f"Файл {remotepath} загружен в {localpath}.")
#     else:
#         print("Файл не был загружен.")
