from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Go to https://www.amazon.com/Acer-C27-1655-UA91-i5-1135G7-Graphics-Wireless/dp/B0983XHMFM/ref=sr_1_1_sspa?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079006&sprefix=desktop%2Caps%2C262&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExRDFSQllYUEYzNjUxJmVuY3J5cHRlZElkPUExMDMwMTU3MjBSRDlDTEI2TDMyMiZlbmNyeXB0ZWRBZElkPUEwNjk5MTIwVU5WVk45RVVXMzdKJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==
    page.goto("https://www.amazon.com/Acer-C27-1655-UA91-i5-1135G7-Graphics-Wireless/dp/B0983XHMFM/ref=sr_1_1_sspa?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079006&sprefix=desktop%2Caps%2C262&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExRDFSQllYUEYzNjUxJmVuY3J5cHRlZElkPUExMDMwMTU3MjBSRDlDTEI2TDMyMiZlbmNyeXB0ZWRBZElkPUEwNjk5MTIwVU5WVk45RVVXMzdKJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==")

    # Click text=Ships from
    page.click("text=Ships from", button="right")

    # Click text=Visit the Acer Store
    page.click("text=Visit the Acer Store", button="right")

    # Click #productTitle
    page.click("#productTitle")

    # Click text=Ships from
    page.click("text=Ships from", button="right")

    # Go to https://www.amazon.com/s?k=desktop&crid=3NYHNFHUKRRBM&sprefix=desktop%2Caps%2C262&ref=nb_sb_noss
    page.goto("https://www.amazon.com/s?k=desktop&crid=3NYHNFHUKRRBM&sprefix=desktop%2Caps%2C262&ref=nb_sb_noss")

    # Click text=Lenovo ThinkCentre M625Q Thin Client Desktop Computer, AMD A9-9420e Processor, 4
    # with page.expect_navigation(url="https://www.amazon.com/Lenovo-10TF002WUS-M625q-A9-9420e-W10p/dp/B07YLY6PH5/ref=sr_1_5?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-5"):
    with page.expect_navigation():
        page.click("text=Lenovo ThinkCentre M625Q Thin Client Desktop Computer, AMD A9-9420e Processor, 4")
    # assert page.url == "https://www.amazon.com/Lenovo-10TF002WUS-M625q-A9-9420e-W10p/dp/B07YLY6PH5/ref=sr_1_5?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-5"

    # Go to https://www.amazon.com/s?k=desktop&crid=3NYHNFHUKRRBM&sprefix=desktop%2Caps%2C262&ref=nb_sb_noss
    page.goto("https://www.amazon.com/s?k=desktop&crid=3NYHNFHUKRRBM&sprefix=desktop%2Caps%2C262&ref=nb_sb_noss")

    # Open new page
    page1 = context.new_page()
    page1.goto("https://www.amazon.com/HP-8300-Business-Desktop-Windows/dp/B07RGQZKXV/ref=sr_1_6?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-6")

    # Go to https://www.amazon.com/HP-8300-Business-Desktop-Windows/dp/B07RGQZKXV/ref=sr_1_6?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-6
    page1.goto("https://www.amazon.com/HP-8300-Business-Desktop-Windows/dp/B07RGQZKXV/ref=sr_1_6?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-6")

    # Click text=HP Elite 8300 Business Desktop, Intel Quad Core i7 3770 3.4Ghz, 32GB DDR3 RAM, 2
    page.click("text=HP Elite 8300 Business Desktop, Intel Quad Core i7 3770 3.4Ghz, 32GB DDR3 RAM, 2", modifiers=["Control"])

    # Open new page
    page2 = context.new_page()
    page2.goto("https://www.amazon.com/ASUS-Anti-glare-Processor-Kensington-V241EA-ES001/dp/B094KMRJRD/ref=sr_1_7_sspa?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-7-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTVFHWFFZOThYOVZRJmVuY3J5cHRlZElkPUEwNjU2MTI0MVpIUjBJWjJGOUMyNCZlbmNyeXB0ZWRBZElkPUEwNTQyODgyMklIVEpDREkwSzI0WCZ3aWRnZXROYW1lPXNwX210ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=")

    # Click text=ASUS AiO All-in-One Desktop PC, 23.8” FHD Anti-glare Display, Intel Pentium Gold
    # with page.expect_navigation(url="https://www.amazon.com/ASUS-Anti-glare-Processor-Kensington-V241EA-ES001/dp/B094KMRJRD/ref=sr_1_7_sspa?crid=3NYHNFHUKRRBM&keywords=desktop&qid=1640079880&sprefix=desktop%2Caps%2C262&sr=8-7-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTVFHWFFZOThYOVZRJmVuY3J5cHRlZElkPUEwNjU2MTI0MVpIUjBJWjJGOUMyNCZlbmNyeXB0ZWRBZElkPUEwNTQyODgyMklIVEpDREkwSzI0WCZ3aWRnZXROYW1lPXNwX210ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="):
    with page.expect_navigation():
        page.click("text=ASUS AiO All-in-One Desktop PC, 23.8” FHD Anti-glare Display, Intel Pentium Gold", modifiers=["Control"])

    # Click #tabular-buybox >> :nth-match(div:has-text("TekRefurbs"), 3)
    page1.click("#tabular-buybox >> :nth-match(div:has-text(\"TekRefurbs\"), 3)", button="right")

    # Click a:has-text("TekRefurbs")
    page1.click("a:has-text(\"TekRefurbs\")", button="right")

    # Click text=Sold by
    page1.click("text=Sold by")

    # Click a:has-text("TekRefurbs")
    page1.click("a:has-text(\"TekRefurbs\")", button="right")

    # Click a:has-text("TekRefurbs")
    page1.click("a:has-text(\"TekRefurbs\")", button="right")

    # Close page
    page1.close()

    # Close page
    page2.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
