import reflex as rx
from app.states.auth_state import AuthState


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="w-10 h-10 text-blue-600 mb-4"),
        rx.el.h3(title, class_name="text-xl font-bold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-gray-600"),
        class_name="p-6 bg-white rounded-lg shadow-md border",
    )


def step_card(number: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(number, class_name="text-blue-600 font-bold"),
            class_name="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full text-2xl mb-4",
        ),
        rx.el.h3(title, class_name="text-xl font-bold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-gray-600"),
        class_name="text-center",
    )


def login_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.el.form(
                rx.radix.primitives.dialog.title("Log In to Valido"),
                rx.el.div(
                    rx.el.label("Email Address", class_name="font-medium text-sm"),
                    rx.el.input(
                        name="email",
                        placeholder="you@example.com",
                        type="email",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.label("Password", class_name="font-medium text-sm mt-4"),
                    rx.el.input(
                        name="password",
                        placeholder="Enter your password",
                        type="password",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="checkbox", name="remember", class_name="mr-2"
                            ),
                            "Remember me",
                            class_name="flex items-center text-sm",
                        ),
                        rx.el.a(
                            "Forgot password?",
                            href="#",
                            class_name="text-sm text-blue-600 hover:underline",
                        ),
                        class_name="flex justify-between items-center mt-4",
                    ),
                    rx.el.button(
                        "Log In",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white py-2 rounded-md mt-6 hover:bg-blue-700",
                    ),
                    rx.el.p(
                        "Don't have an account? ",
                        rx.el.a(
                            "Sign up",
                            on_click=AuthState.toggle_login_signup,
                            class_name="text-blue-600 hover:underline cursor-pointer",
                        ),
                        class_name="text-center text-sm text-gray-600 mt-4",
                    ),
                    class_name="mt-4",
                ),
                on_submit=AuthState.login,
                reset_on_submit=True,
            )
        ),
        open=AuthState.show_login_modal,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), AuthState.toggle_login_modal
        ),
    )


def signup_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.el.form(
                rx.radix.primitives.dialog.title("Create Your Valido Account"),
                rx.el.div(
                    rx.el.label("Full Name", class_name="font-medium text-sm"),
                    rx.el.input(
                        name="full_name",
                        placeholder="John Doe",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.label("Email Address", class_name="font-medium text-sm mt-4"),
                    rx.el.input(
                        name="email",
                        placeholder="you@example.com",
                        type="email",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.label("Phone Number", class_name="font-medium text-sm mt-4"),
                    rx.el.input(
                        name="phone",
                        placeholder="+1234567890",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.label("Password", class_name="font-medium text-sm mt-4"),
                    rx.el.input(
                        name="password",
                        placeholder="Create a strong password",
                        type="password",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.label("I am a:", class_name="font-medium text-sm mt-4"),
                    rx.el.select(
                        ["Business", "Customer"],
                        name="role",
                        on_change=AuthState.set_role,
                        default_value="Customer",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            name="terms",
                            required=True,
                            class_name="mr-2",
                        ),
                        "I agree to the ",
                        rx.el.a(
                            "Terms and Conditions",
                            href="#",
                            class_name="text-blue-600 hover:underline",
                        ),
                        class_name="flex items-center text-sm mt-4",
                    ),
                    rx.el.button(
                        "Sign Up",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white py-2 rounded-md mt-6 hover:bg-blue-700",
                    ),
                    rx.el.p(
                        "Already have an account? ",
                        rx.el.a(
                            "Log in",
                            on_click=AuthState.toggle_login_signup,
                            class_name="text-blue-600 hover:underline cursor-pointer",
                        ),
                        class_name="text-center text-sm text-gray-600 mt-4",
                    ),
                    class_name="mt-4",
                ),
                on_submit=AuthState.signup,
                reset_on_submit=True,
            )
        ),
        open=AuthState.show_signup_modal,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), AuthState.toggle_signup_modal
        ),
    )


def landing_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.div(
                    rx.icon("shield-check", class_name="h-8 w-8 text-blue-600"),
                    rx.el.h1("Valido", class_name="text-2xl font-bold text-gray-900"),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    rx.el.button(
                        "Log In",
                        on_click=AuthState.toggle_login_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md",
                    ),
                    rx.el.button(
                        "Sign Up",
                        on_click=AuthState.toggle_signup_modal,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="container mx-auto flex justify-between items-center p-4",
            ),
            class_name="bg-white border-b sticky top-0 z-10",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h1(
                    "Digital Receipts and Warranties You Can Trust",
                    class_name="text-4xl md:text-6xl font-bold text-gray-800 text-center mb-6",
                ),
                rx.el.p(
                    "Valido provides immutable, verifiable proof of purchase and warranty for businesses and consumers.",
                    class_name="text-lg text-gray-600 text-center max-w-3xl mx-auto mb-8",
                ),
                rx.el.div(
                    rx.el.button(
                        "Get Started",
                        on_click=AuthState.toggle_signup_modal,
                        class_name="px-8 py-3 text-lg font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700",
                    ),
                    rx.el.button(
                        "Learn More",
                        class_name="px-8 py-3 text-lg font-semibold text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200",
                    ),
                    class_name="flex justify-center gap-4",
                ),
                class_name="container mx-auto px-4 py-20 text-center",
            )
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    "Empowering Trust Through Technology",
                    class_name="text-3xl font-bold text-gray-800 text-center mb-12",
                ),
                rx.el.div(
                    feature_card(
                        "file-check-2",
                        "Warranty Management",
                        "Create, manage, and track digital warranties with ease.",
                    ),
                    feature_card(
                        "receipt",
                        "Receipt Validation",
                        "Instantly verify purchase receipts for authenticity.",
                    ),
                    feature_card(
                        "qr-code",
                        "QR Code Verification",
                        "Scan QR codes for quick and secure validation on the go.",
                    ),
                    feature_card(
                        "shield-alert",
                        "Fraud Detection",
                        "AI-powered system to detect and prevent fraudulent activities.",
                    ),
                    class_name="grid md:grid-cols-2 lg:grid-cols-4 gap-8",
                ),
                class_name="container mx-auto px-4 py-16",
            ),
            class_name="bg-gray-50",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    "Simple Steps to Secure Your Purchase",
                    class_name="text-3xl font-bold text-gray-800 text-center mb-12",
                ),
                rx.el.div(
                    step_card(
                        "1",
                        "Generate",
                        "Businesses issue a digital receipt and warranty at the point of sale.",
                    ),
                    step_card(
                        "2",
                        "Receive",
                        "Customers instantly receive a secure link to their documents.",
                    ),
                    step_card(
                        "3",
                        "Validate",
                        "Verify authenticity anytime, anywhere by scanning a QR code or entering a unique ID.",
                    ),
                    class_name="grid md:grid-cols-3 gap-12",
                ),
                class_name="container mx-auto px-4 py-16",
            )
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p("10,000+", class_name="text-4xl font-bold text-blue-600"),
                    rx.el.p("Verified Warranties", class_name="text-gray-600"),
                    class_name="text-center",
                ),
                rx.el.div(
                    rx.el.p("500+", class_name="text-4xl font-bold text-blue-600"),
                    rx.el.p("Businesses Onboarded", class_name="text-gray-600"),
                    class_name="text-center",
                ),
                rx.el.div(
                    rx.el.p("99.9%", class_name="text-4xl font-bold text-blue-600"),
                    rx.el.p("Uptime & Reliability", class_name="text-gray-600"),
                    class_name="text-center",
                ),
                class_name="container mx-auto px-4 py-16 grid md:grid-cols-3 gap-8",
            ),
            class_name="bg-gray-50",
        ),
        rx.el.footer(
            rx.el.div(
                rx.el.p(
                    "© 2024 Valido. All rights reserved.",
                    class_name="text-sm text-gray-500",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.icon("twitter"),
                        href="#",
                        class_name="text-gray-500 hover:text-gray-700",
                    ),
                    rx.el.a(
                        rx.icon("github"),
                        href="#",
                        class_name="text-gray-500 hover:text-gray-700",
                    ),
                    rx.el.a(
                        rx.icon("linkedin"),
                        href="#",
                        class_name="text-gray-500 hover:text-gray-700",
                    ),
                    class_name="flex gap-4",
                ),
                class_name="container mx-auto flex justify-between items-center p-4",
            ),
            class_name="border-t",
        ),
        login_modal(),
        signup_modal(),
    )