// Importation des modules
const { setup } = require('./setup');
const { Builder, By, Key, until } = require('selenium-webdriver');

// Initialisation de nest_asyncio
const nestAsyncio = require('nest-asyncio');
nestAsyncio.apply();

// Fonction pour obtenir des informations : obtient le nombre de publications d'un compte Instagram
async function get_info(username) {
    const account = await fetch(`https://www.instagram.com/${username}`);
    const text = await account.text();

    if (text.includes("Posts")) {
        const location = text.indexOf("Posts") - 8;
        let result = "";
        for (let i = 0; i < 10; i++) {
            if (!isNaN(parseInt(text[location + i]))) {
                result += text[location + i];
            }
        }
        return parseInt(result);
    } else {
        return 0;
    }
}

// Fonction pour obtenir la dernière publication d'un compte Instagram
async function get_post(user) {
    const url = `https://www.instagram.com/${user}`;
    let result = "";

    const browser = await new Builder().forBrowser('chrome').build();
    await browser.get(url);
    await browser.sleep(2000); // Attendre 2 secondes

    const html = await browser.getPageSource();

    if (!html.includes("/p/")) {
        return "Une erreur s'est produite, veuillez réessayer dans quelques minutes.";
    } else {
        const location = html.indexOf("/p/");
        for (let i = 0; i < 14; i++) {
            result += html[location + i];
        }
        return `https://www.instagram.com${result}/`;
    }
}

module.exports = { get_info, get_post };