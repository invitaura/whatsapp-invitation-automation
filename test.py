import urllib.parse

name = "Hello&Anna" 
name_with_url =  f"🌐 https://mukesh-weds-akhila.netlify.app?guest={urllib.parse.quote(name)}\n\n"

print(name_with_url)