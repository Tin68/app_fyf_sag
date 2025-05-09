import reflex as rx

def header() -> rx.Component:
    return rx.vstack(
        rx.avatar(fallback="CS", variant="soft", color_scheme="green", size="lg"),
    )