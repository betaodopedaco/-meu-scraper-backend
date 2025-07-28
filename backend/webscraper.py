from playwright.sync_api import sync_playwright
from geolocation import getcoords


MAIN_TAB_XPATH = '//a[contains(@href, "https://www.google.com/maps/place")]'

data = None


def scrape_maps(search_term, city, state, num_items):

    lat, lon = getcoords(f"{city}, {state}")

    URL = f"https://www.google.com/maps/@{lat},{lon},12z?entry=ttu"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(URL)

        searchbox = page.locator("#searchboxinput")
        searchbox.click()
        searchbox.fill(f"{search_term} near me")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        page.hover(MAIN_TAB_XPATH)

        results = page.locator(MAIN_TAB_XPATH).all()

        while len(results) < num_items:
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(2000)

            results = page.locator(MAIN_TAB_XPATH).all()
            print(len(results))

            if len(results) >= num_items:
                break

        titles = []
        webs = []
        phones = []
        addrs = []

        for result in results:
            result.click()

            page.wait_for_timeout(2000)

            response = page.get_by_role("main").last

            title = address = website = phone = ""

            if response.locator("h1").last.is_visible():
                title = response.locator("h1").last.inner_text()

            if response.locator("[data-item-id='address']").locator(".fontBodyMedium").is_visible():
                address = response.locator(
                    "[data-item-id='address']").locator(".fontBodyMedium").inner_text()

            if response.locator("[data-item-id='authority']").is_visible():
                website = response.locator(
                    "[data-item-id='authority']").get_attribute("href")

            if response.locator("[data-tooltip='Copy phone number']").locator(".fontBodyMedium").is_visible():
                phone = response.locator(
                    "[data-tooltip='Copy phone number']").locator(".fontBodyMedium").inner_text()

            titles.append(title)
            addrs.append(address)
            webs.append(website)
            phones.append(phone)

        # Combina os dados em uma lista de dicionários para retorno JSON
        results_list = []
        for i in range(len(titles)):
            results_list.append({
                "name": titles[i],
                "address": addrs[i],
                "website": webs[i],
                "phone": phones[i]
            })

        browser.close()

    return results_list # Retorna a lista de dicionários
