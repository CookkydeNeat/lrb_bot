const { Client, Intents } = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
const { CommandTree } = require('discord-tree-commands');
const { get_info, get_post } = require('./insta');
const { server_id, log_channel_id, notification_channel_id, counter_time_min, counter_time_max, accounts, counters, token } = require('./setup');

const tree = new CommandTree(client);

let lookup = false;
let setup = false;

client.on('ready', () => {
    console.log(`${client.user.tag} is online!`);
    client.user.setActivity('being coded');

    // Synchronize slash commands
    tree.sync(server_id);
});

// Define the slash commands

tree.command({
    name: 'hello',
    description: 'Say hello',
    guild: server_id,
    handler: async (interaction) => {
        await interaction.reply(`Hello <@${interaction.user.id}>`);
        console.log('/hello =====> "hello" sent to ${interaction.user.tag}');
    }
});

tree.command({
    name: 'uwu',
    description: 'Say uwu',
    guild: server_id,
    handler: async (interaction) => {
        await interaction.reply('UwU!');
        console.log('/uwu =====> "uwu" sent to ${interaction.user.tag}');
    }
});

tree.command({
    name: 'shutdown',
    description: 'Kill the bot',
    guild: server_id,
    handler: async (interaction) => {
        await interaction.reply('Goodbye, sir!');
        process.exit();
    }
});


client.on('messageCreate', async (message) => {
    // Handle other events if needed
});

// Start the bot
client.login(token);
