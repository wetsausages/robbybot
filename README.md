<h1 align="center">
  robbybot
</h1>
<p align="center">
  <a href="https://discord.gg/3xBDxAsXwR">
    <img alt="robbybot" src="./src/robby.png" width="60" />
  </a>
</p>

<p align="center"> A multipurpose Discord bot for AVAS.cc </p>

# Features
- Mute/unmute, ban
- Moderator action logging
- Smart auto FAQ
- Easy poll creation

## Moderation Permission Management
robbybot checks command permissions against a list of chosen roles as opposed to member-specific permissions. This is to make adding and removing mods (and their permissions with this bot) easier to manage. Administrators must use `!setmod [moderator role]` to add a role to moderator list.

## AutoFAQ
robbybot AutoFAQ works with 2 components: a key:response entry, and a confidence value. Keys are keywords that relate to their corresponding response. For example, the `[keyword]` 'version' would have the `[response]` 'The server is version 1.18'.

Whether or not the bot responds to a message is decided based on confidence and whether or not a key was heard. If the bot thinks the message was a question and hears a keyword, it will respond with that keyword's response.

## Admin commands
`!setmod [role]`
Adds selected role to list of moderator roles.

`!removemod [role]`
Removes selected role from list of moderator roles.

`!modlog`
Sets the moderation logging channel to the current channel.

## Moderator commands
`!mute [member] [duration]* [reason]`
Mutes member for specified duration. Duration examples: 12d, 6hr, 30m, 59s, or omit for permanent mute. Adds members to muted role, which must be named "Muted" until I can be bothered to add !setmutedrole.

`!unmute [member]`
Unmutes muted member.

`!ban [member] [reason]`
Bans member.

`!faq`
AutoFAQ explaination.

`!poll`
Poll explaination.

## AutoFAQ
`!faq toggle`
Toggles autoFAQ on/off.

`!faq days [n]`
Only responds to players with less than [n] days on the server.

`!faq keys`
Show current list of keywords the bot looks for to respond to.

`!faq add [key] [response]`
Add a new key:response entry. If the bot sees the `[key]` and has confidence its a question worth responding to, it will respond with `[response]`.

`!faq remove [key]`
Removes [key]:response entry.

## Poll
`!poll [question]`
Creates a yes or no poll.

`!poll [question]; [option]; [option]; [option]...`
Creates a poll with multiple responses. Up to 12.

`!pollrole [role]`
Sets role to ping when polls are created.
