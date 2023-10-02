// Définition des comptes Instagram
const accounts = ["lpo_remibelleau", "radio2b_", "mdl_lrb", "lrb_cord"];

// Définition des compteurs de publication Instagram
const counters = new Array(accounts.length).fill(0);

// Identifiant du serveur
const server_id = '1026168999173697647';

// Identifiant du canal de notification
const notification_channel_id = '1136689538484424776';

// Identifiant du canal des logs
const log_channel_id = '1136689586886680628';

// Identifiant du rôle à mentionner
const role_id = '1151520022439665696';

// Intervalle de temps entre 2 requêtes (aléatoire pour éviter le flood)
const counter_time_min = 15000; // 15 secondes en millisecondes
const counter_time_max = 30000; // 30 secondes en millisecondes

// Jeton du bot
const token = 'MTE0ODk1NDI2NDkyNDg2MDQ4Ng.GKTjFX.yfYFKHtmGan95YHWGVsUeP6jkvPyvft3vWItk4';