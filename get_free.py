from os import statvfs

s = statvfs("/")

print("Free space = {} MB".format(s[1]*s[4]/pow(1024,2)))
