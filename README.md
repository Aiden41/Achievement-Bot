Achievement Bot

This bot is meant to be used with the Halo Completionist Discord server. 
The bot uses the OpenXBL API to access achievements progress on Halo games for users.
When the game is complete, it gives the respective role.
If the game is not complete, it provides the user with progress.

Uses a simple database system where the dictionary key is the Discord account ID and the value is the Xbox account ID.

To use this bot: 
1. Change the role IDs for each command to your respective role
2. Create a bot application on the discord developer page and create an account with OpenXBL and get your tokens. Create an .env file with them
3. Use the +gt command first to ensure your database is created.
