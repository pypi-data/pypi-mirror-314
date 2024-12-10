```bash
pip install asmix
```

```python
from asmix import Email

python = Email.hotmail('example@hotmail.com')

if python == True:
  print('Email Valide')
else:
  print('Email Invalide')
```
```python
from asmix import Instagram as gg

username = "cristiano"
info = gg.info(username) or {}

name = info.get("name", "None")
username = info.get("username", "None")
followers = info.get("followers", "None")
following = info.get("following", "None")
date = info.get("date", "None")
id = info.get("id", "None")
post = info.get("post", "None")
bio = info.get("bio", "None")
user_is_verified = info.get("is_verified", "None")
user_is_private = info.get("is_private", "None")

print("Name:", name)
print("Username:", username)
print("Followers:", followers)
print("Following:", following)
print("Date:", date)
print("ID:", id)
print("Posts:", post)
print("Bio:", bio)
print("Verified:", user_is_verified)
print("Private:", user_is_private)
```

```python
from asmix import Instagram as ig
#Date 2012/2013/2014, 2024
try:
  username = ig.usergen(2012)

  print(username)
except:pass
```

```python
from asmix import Instagram as ig

username = "geraldvkirkland"

rr = ig.rest(username)

print(rr)

#result g*******d@gmail.com
```

```python
from asmix import Instagram

aa = Instagram.check('example.gmail.com')
print(aa)

```