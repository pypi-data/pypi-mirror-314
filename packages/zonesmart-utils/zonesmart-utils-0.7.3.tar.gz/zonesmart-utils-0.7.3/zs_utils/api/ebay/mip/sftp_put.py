# import argparse
# import os

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

# parser = argparse.ArgumentParser(description="Загрузка eBay feed")


# class StoreNameValuePair(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         n, v = values.split("=")
#         setattr(namespace, n, v)


# parser.add_argument("file_path", action=StoreNameValuePair, help="Путь к feed-файлу на локальной машине")
# parser.add_argument(
#     "mip_dir",
#     action=StoreNameValuePair,
#     help="Папка на сервере mip.ebay.com, в которую будет загружен feed-файл",
# )
# # parser.add_argument('--apps', nargs='+', required=False,
# #                    help='список приложений, в которых будут очищаться папки migrations')
# args = parser.parse_args()

# file_path = args.file_path
# if not os.path.isfile(file_path):
#     raise AttributeError(f"Файл {file_path} не существует на локальной машине!")

# mip_dir = args.mip_dir
# if mip_dir not in mip_dirs:
#     raise AttributeError(f"Недопустимая папка для загрузки: {mip_dir}\n" f"Допустимые папки: {mip_dirs}")


# def callback(ready, total):
#     print(f"File was {'un' if ready!=total else ''}successfully uploaded:")
#     print(f"{ready} of {total} bytes uploaded")


# with Connection(**credentials, cnopts=cnopts) as sftp:
#     sftp.chdir(os.path.join("store", mip_dir))
#     try:
#         sftp.put(localpath=file_path, callback=callback)
#     except FileNotFoundError as err:
#         print(err)
