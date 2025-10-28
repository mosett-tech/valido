import reflex as rx
import os
import logging
from supabase import create_client, Client
from typing import Literal


class AuthState(rx.State):
    show_login_modal: bool = False
    show_signup_modal: bool = False
    full_name: str = ""
    email: str = ""
    phone: str = ""
    password: str = ""
    role: Literal["Business", "Customer"] = "Customer"

    def _get_supabase_client(self) -> Client | None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)

    @rx.event
    def toggle_login_modal(self):
        self.show_login_modal = not self.show_login_modal

    @rx.event
    def toggle_signup_modal(self):
        self.show_signup_modal = not self.show_signup_modal

    @rx.event
    def toggle_login_signup(self):
        self.show_login_modal = not self.show_login_modal
        self.show_signup_modal = not self.show_signup_modal

    @rx.event
    def login(self, form_data: dict):
        supabase = self._get_supabase_client()
        if not supabase:
            yield rx.toast.error("Supabase not configured.")
            return
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": form_data.get("email"), "password": form_data.get("password")}
            )
            if response.user:
                yield rx.toast.success("Login successful!")
                self.show_login_modal = False
                return rx.redirect("/")
        except Exception as e:
            logging.exception(f"Login failed: {e}")
            yield rx.toast.error(f"Login failed: {e}")

    @rx.event
    def signup(self, form_data: dict):
        supabase = self._get_supabase_client()
        if not supabase:
            yield rx.toast.error("Supabase not configured.")
            return
        email = form_data.get("email")
        password = form_data.get("password")
        full_name = form_data.get("full_name")
        phone = form_data.get("phone")
        role = form_data.get("role")
        if not all([email, password, full_name, role]):
            yield rx.toast.error("Please fill all required fields.")
            return
        try:
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {"full_name": full_name, "phone": phone, "role": role}
                    },
                }
            )
            if response.user:
                yield rx.toast.success(
                    "Signup successful! Please check your email to verify."
                )
                self.show_signup_modal = False
            else:
                yield rx.toast.error("Signup failed. Please try again.")
        except Exception as e:
            logging.exception(f"Signup failed: {e}")
            yield rx.toast.error(f"Signup failed: {e}")