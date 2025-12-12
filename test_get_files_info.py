from functions.get_files_info import get_files_info
from functions.config import MAX_CHARS

print(get_files_info("calculator", "."))
print("........................................")
print(get_files_info("calculator", "pkg"))
print("........................................")
print(get_files_info("calculator", "/bin"))
print("........................................")
print(get_files_info("calculator", "../"))
print("........................................")
