from instagrapi import Client

cl = Client()
cl.login("typing.every.day", "ohm30016")

thread = cl.direct_threads(1)[0]

for i in thread.messages:
    print(i.text)