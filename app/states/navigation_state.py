import reflex as rx


class NavigationState(rx.State):
    """Manages the navigation state of the application."""

    @rx.var
    def current_page(self) -> str:
        return self.router.page.path

    @rx.event
    def set_current_page(self, page: str):
        return rx.redirect(page)