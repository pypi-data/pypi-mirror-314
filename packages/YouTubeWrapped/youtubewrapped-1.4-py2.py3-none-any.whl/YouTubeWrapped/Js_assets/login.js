const { firefox } = require('playwright-extra')
const stealth = require('puppeteer-extra-plugin-stealth')()

firefox.use(stealth)


function sleep(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}


async function checkForRedirect(page) {
    const currentUrl = page.url();
    const pattern = /^https:\/\/www\.youtube\.com\//;
    return pattern.test(currentUrl);
}

(async () => {
    let redirected = false;
    const browser = await firefox.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F%253FthemeRefresh%253D1&ec=65620&hl=en&ifkv=AcMMx-daHv6eDtH9mVrBC9f-vKNb6QEhH3EsPN_4bOuBKMB9WTRGeINod_HG3fvsfL4VLYEs6rg&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1576614644%3A1733517986997732&ddm=1');

    while (!redirected) {
        redirected = await checkForRedirect(page);
        if (!redirected) {
            await sleep(1000);
        }
    }

    sleep(2000)
    const cookies = await page.context().cookies();
    const fs = require('fs');
    fs.writeFileSync('YT_cookies.json', JSON.stringify(cookies, null, 2));

    
    await browser.close();
})();
