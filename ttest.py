lst = []
with open("koatuu_list_non.txt", "r") as a_file:
    for koatuu_line in a_file:
        koatu = koatuu_line.strip()
        lst.append(koatu)
myset = set(lst)
mynewlist = list(myset)

with open('koatuu_list_cutted.txt', 'w') as f:
    for item in mynewlist:
        f.write("%s\n" % item)