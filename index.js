'use strict';

// Require the necessary discord.js classes
const { Client, GatewayIntentBits } = require('discord.js');
const { startListening, stopListening } = require('./insta');
const { Account } = require('./utils.js');

// Used to load the .env file and use the TOKEN env
require('dotenv').config();

// The bot prefix, used to trigger commands, could be anything.
const BOT_PREFIX = '!';

// Create a new client instance
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ],
});

// List accounts to follow
let accounts = [
    new Account("lpo_remibelleau")
];

// When the client is ready, run this code (only once)
// We use 'c' for the event parameter to keep it separate from the already defined 'client'
client.once('ready', (c) => {
    console.log(`Ready! Logged in as ${c.user.tag}`);
    // startListening(client.channels.cache.first(),1,accounts)
});

// When someone sends a message
client.on('messageCreate', (message) => {
    console.log(`${message.author.username} sent: ${message.content}`);
    // Stop the function if the message author is a bot (including itself)
    if (message.author.bot) return;
    // Stop the function if the message doesn't start with the prefix
    if (!message.content.startsWith(BOT_PREFIX)) return;

    /**
     * Example boilerplate which replies to a message
     * Please note that when the bot grows you may need to move the command logic into separate files
     */
    if (message.content === '!hi') {
        // Will reply 'Hey @yourname !'
        message.reply(`Hey ${message.author} !`);
    }

    if (message.content.startsWith('!listen')) {
        let frequency = Number(message.content.split(' ')[1]);
        if (isNaN(frequency)) {
            message.reply('Message is not a number, defaulted to 15');
            frequency = 15
        }
        startListening(message.channel, frequency, accounts);
    }
    if(message.content.startsWith("!stop")){
        stopListening()
        message.reply("Stopped listening")
    }
});

// Log in to Discord with your client's token
client.login(process.env.TOKEN);
