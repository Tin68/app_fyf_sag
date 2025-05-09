import reflex as rx

# comun
def lang()->rx.Component:
    return rx.script("document.documentElement.lang='es'")

#carpetas
sheet_title = "FyFSag app"
sheet_description = "App gestion carpetas, solicitos y provisiones"


#Index
index_title = "Debe Autentificarse"
index_description = "Debe Autentificarse"

#login
login_title = "Por favor autentificarse"
login_description = "Por favor autentificarse"

login_algorithm = "HS256"
login_access_token_duration = 1
login_secret = "de6de62abecd528273d4bedaeddc5ad95423fee6a37a7fbfe8d50ba49179533b0"