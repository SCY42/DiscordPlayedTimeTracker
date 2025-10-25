# import json


# d = {
#     "1234": [
#         (1, 2, 3),
#         (4, 5, 6)
#     ]
# }


# with open("now_playing.json", 'w', encoding="utf8") as f:
#     json.dump(d, f)


l = ["123", "546", "893", "212"]

for ll in l:
    if ll == "546":
        l.remove(ll)

print(l)