contacts = [
    ('James', 42),
    ('Amy', 24),
    ('John', 31),
    ('Amanda', 63),
    ('Bob', 18)
]

name = input()

for i in contacts:
 if name in i:
  print(i[0],'is',i[1])
 else:
  print("Not found")