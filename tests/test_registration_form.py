import re
from pathlib import Path

from playwright.sync_api import Page, expect
from tests.consts import REGISTRATION_FORM

FILE_PATH = (Path(__file__).parent / "src" / "playwright_registration_form.html").as_uri()


def test_registration_form(page: Page):
    page.goto(FILE_PATH)

    fillInFullForm(page)
    validateResetForm(page)

    fillInFullForm(page)
    validateSubmitForm(page)


def test_header(page: Page):
    page.goto(FILE_PATH)

    validateRegistrationLink(page)
    validatePreferencesLink(page)
    validateHelpLink(page)
    validatePlaywrightDocsLink(page)


def fillInFullForm(page):
    fillInFirstName(page, REGISTRATION_FORM["firstName"])
    fillInLastName(page, REGISTRATION_FORM["lastName"])
    fillInEmail(page, REGISTRATION_FORM["email"])
    fillInEmailConfirmation(page, REGISTRATION_FORM["email"])
    fillInPassword(page, REGISTRATION_FORM["password"])
    fillInPhoneNumber(page, REGISTRATION_FORM["phoneNumber"])
    fillInDateOfBirth(page, REGISTRATION_FORM["dateOfBirth"])
    selectCountry(page, REGISTRATION_FORM["country"])
    fillInCity(page, REGISTRATION_FORM["city"])
    selectGender(page, REGISTRATION_FORM["gender"])


def printAccessibilityTree(page):
    print(page.locator("body").aria_snapshot())


def fillInFirstName(page, firstName):
    page.get_by_role("textbox", name="First name").fill(firstName)


def fillInLastName(page, lastName):
    page.get_by_label("Last name").fill(lastName)


def fillInEmail(page, email):
    page.get_by_label("Email address *", exact=True).fill(email)


def fillInEmailConfirmation(page, email):
    page.get_by_label("Confirm email address").fill(email)


def fillInPassword(page, password):
    page.get_by_label("Password").fill(password)


def fillInPhoneNumber(page, phoneNumber):
    page.get_by_label("Phone number").fill(phoneNumber)


def fillInDateOfBirth(page, dateOfBirth):
    page.get_by_label("Date of birth").fill(dateOfBirth)


def selectCountry(page, country):
    page.get_by_label("Country").select_option(label=country)


def fillInCity(page, city):
    page.get_by_label("City").fill(city)


def selectGender(page, gender):
    page.get_by_label(gender, exact=True).check()


def validateResetForm(page):
    page.get_by_role("button", name="Reset form").click()

    expect(page.get_by_label("First name")).to_have_value("")
    expect(page.get_by_label("Last name")).to_have_value("")
    expect(page.get_by_label("Country")).to_have_value("")
    expect(page.get_by_role("status")).to_have_text(REGISTRATION_FORM["resetMessage"])


def validateSubmitForm(page):
    page.get_by_label("I agree to the terms and conditions").check()
    page.get_by_role("button", name="Submit registration").click()

    dialog = page.get_by_role("dialog", name=REGISTRATION_FORM["successHeaderText"])
    expect(dialog).to_be_visible()
    expect(dialog).to_contain_text(f"Thank you, {REGISTRATION_FORM['firstName']}!")

    dialog.get_by_role("button", name=REGISTRATION_FORM["successCloseButtonText"]).click()
    expect(dialog).to_be_hidden()


def validateRegistrationLink(page):
    page.get_by_role("link", name="Registration").click()

    expect(page).to_have_url(re.compile(r"#registration$"))
    expect(page.get_by_role("heading", name="Registration details")).to_be_visible()


def validatePreferencesLink(page):
    page.get_by_role("link", name="Preferences").click()

    expect(page).to_have_url(re.compile(r"#preferences$"))
    expect(page.get_by_role("heading", name="Preferences")).to_be_visible()


def validateHelpLink(page):
    page.get_by_role("link", name="Help").click()

    dialog = page.get_by_role("dialog", name=REGISTRATION_FORM["modalHeaderText"])
    expect(dialog).to_be_visible()
    expect(dialog.get_by_role("heading", level=2, name=REGISTRATION_FORM["modalHeaderText"])).to_be_visible()

    dialogOkButton = dialog.get_by_role("button", name=REGISTRATION_FORM["modalButtonText"])
    expect(dialogOkButton).to_be_enabled()
    dialogOkButton.click()
    expect(dialog).to_be_hidden()


def validatePlaywrightDocsLink(page):
    docsLink = page.get_by_role("link", name="Playwright documentation")
    expect(docsLink).to_have_attribute("href", "https://playwright.dev/")
    expect(docsLink).to_have_attribute("target", "_blank")

    with page.expect_popup() as popupInfo:
        docsLink.click()

    popupInfo.value.close()