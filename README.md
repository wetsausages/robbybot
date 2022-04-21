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
- Mute/Unmute, Ban
- Moderator action logging
- AutoFAQ

## Moderation Management
robbybot checks command permissions against a list of chosen roles as opposed to member-specific permissions. This is to make adding and removing mods (and their permissions with this bot) easier to manage. Administrators must use !setmod [moderator role] to add a role to moderator list.

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
Configure AutoFAQ.

`!poll`
Poll explaination.

## AutoFAQ
`I cannot be fucked to explain this just run !faq pls`

## Poll
`!poll [question]`
Creates a yes or no poll.

`!poll [question]; [option]; [option]; [option]...`
Creates a poll with multiple responses. Up to 12.

`!pollrole [role]`
Sets role to ping when polls are created.
