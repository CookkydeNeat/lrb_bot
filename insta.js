'use strict'
const { Account, Listener } = require("./utils.js")
const { Channel, Client } = require("discord.js");
const pt = require('puppeteer');

/**
 * @type {Listener}
 */
let listener = null
/**
 * Do you really need explanation here ?
 * @type {String}
 */
const instagramUrl = "https://www.instagram.com"

/**
 * The minimum update frequency,  
 * I do not accept to fetch instagram more often than that, 
 * because this could lead to timeout from instagram servers
 */
const MIN_UPDATE_FREQUENCY = 1000 * 60 * 15;

/**
 * Start a intervall loop which check every instagram accounts and process them
 * @param {Channel} channel 
 * @param {number} frequency 
 * @param {Account[]} accounts 
 */
exports.startListening = async function startListening(channel, frequency, accounts) {
    console.log("Started listening")
    if(listener){
        channel.send("I am already listening !")
        channel.send(`Next fetch ${listener.theoreticalTimeUntilNextFetch()}`)
        return
    }
    // First time check
    checkAllAccounts(accounts,channel)
    frequency = frequency*1000*60
    //Don't allow to set a value smaller than MIN_UPDATE_FREQUENCY
    if (frequency < MIN_UPDATE_FREQUENCY) {
        frequency = MIN_UPDATE_FREQUENCY
    }
    let intervalId = setInterval(checkAllAccounts, frequency,accounts,channel);
    listener = new Listener(intervalId,frequency)
}

exports.stopListening =  function stopListening() {
    clearInterval(listener.id)
    listener = null
    console.log("Stopped listening")
}

/**
 * Check all accounts
 * @param {Account} accounts 
 * @param {Channel} channel 
 */
async function checkAllAccounts(accounts,channel){
    for (let account of accounts) {
        console.log(`Checking: ${account.name}`)
        await checkAccount(account,channel)
    }
}

/**
 * 
 * @param {Account} account 
 * @param {Channel} channel 
 */
async function checkAccount(account, channel) {
    const href = await extractLatestPost(account.name)
    if(href != account.lastPost){
        account.lastPost = href
        sendNewPost(account,channel)
    }
    
}

/**
 * 
 * @param {string} name 
 */
async function extractLatestPost(name){
    const browser = await pt.launch({headless:"new"})
   
    //browser new page
    const p = await browser.newPage();
    console.log("Loading page...");
    //set viewpoint of browser page
    await p.setViewport({ width: 1000, height: 500 })
    //launch URL
    await p.goto(`${instagramUrl}/${name}`)
    
    // Wait for the page to load
    await p.waitForSelector('a img'); // Wait for an img element within a link

    // Extract the href attribute of the first link with an img element
    const href = await p.$eval('a img', (img) => {
        let limit = 10
        let elem = img
        while (limit > 0){
            elem = elem.parentElement
            if(elem.tagName === "A"){
                limit = -1
            }
            limit-=1
        }
        return elem.href
    });
    console.log('The href of the first link with an img element is:', href);
    
    //browser close
    await browser.close()
    return href
}

/**
 * Send the new post in the designated channel
 * @param {Account} account 
 * @param {Client} client 
 * @param {Channel} channel 
 */
async function sendNewPost(account, channel) {
    await channel.send(account.lastPost);
    console.log(`Sent post in ${channel.name}`)
}

// function delay(time) {
//     return new Promise(function(resolve) { 
//         setTimeout(resolve, time)
//     });
//  }