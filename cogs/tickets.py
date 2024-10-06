import disnake, datetime
from disnake.ext import commands
from localization import localised_command, get_command_data
from services.database import Database
from services.config import Config
from services import embeds
import aiosqlite

class TicketCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @localised_command('t_group')
    async def ticket(self, inter):
        pass

    @ticket.sub_command()
    async def set_category(self, inter: disnake.ApplicationCommandInteraction, category: disnake.CategoryChannel):
        await inter.response.defer()
        data = {
            'guild': inter.guild.id,
            'category': category.id
        }
        async with aiosqlite.connect(Config["paths"]["database"]) as db:
            await db.execute("""
                             INSERT INTO guilds (guild_id, ticket_category_id)
                             VALUES (:guild, :category)
                             ON CONFLICT (guild_id) DO
                             UPDATE SET ticket_category_id = :category
                             """, data)
            await db.commit()
        await inter.send(embed=embeds.Success(locale=inter.locale, description='Ticket category set to ' + category.mention))

    @ticket.sub_command()
    async def set_role(self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        await inter.response.defer()
        data = {
            'guild': inter.guild.id,
            'role': role.id
        }
        async with aiosqlite.connect(Config["paths"]["database"]) as db:
            await db.execute("""
                             INSERT INTO guilds (guild_id, ticket_role_id)
                             VALUES (:guild, :role)
                             ON CONFLICT (guild_id) DO
                             UPDATE SET ticket_role_id = :role
                             """, data)
            await db.commit()
        await inter.send(embed=embeds.Success(locale=inter.locale, description='Ticket role set to ' + role.mention))

    @ticket.sub_command('t_create')
    async def create(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        data = get_command_data("t_create", inter.locale)
        if not inter.guild:
            await inter.send(embed=embeds.Error(locale=inter.locale, description=data["dm"]))
        async with aiosqlite.connect(Config["paths"]["database"]) as db:
            if guild := await Database.Guilds.get_configs(inter.guild.id):
                category = inter.guild.get_channel(guild['ticket_category_id']) if guild['ticket_category_id'] else None
                support = inter.guild.get_role(guild['ticket_role_id']) if guild['ticket_role_id'] else None
            else:
                await db.execute("INSERT INTO guilds (guild_id) VALUES (?)", (inter.guild.id,))
                await db.commit()
                category = None
                support = None
            cursor = await db.execute('SELECT COUNT(*) FROM tickets WHERE guild_id=?', (inter.guild.id,)) # count all tickets on this server
            ticket_id: int = (await cursor.fetchone())[0] + 1
            overwrites = {
                inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                inter.guild.me: disnake.PermissionOverwrite(read_messages=True),
                inter.user: disnake.PermissionOverwrite(read_messages=True)
            }
            if support is not None:
                overwrites[support] = disnake.PermissionOverwrite(read_messages=True)
            ticket = await inter.guild.create_text_channel(name=f"ticket{str(ticket_id).zfill(4)}", category=category, overwrites=overwrites)
            await db.execute("INSERT INTO tickets (guild_id, channel_id, member) VALUES (?, ?, ?)", (inter.guild.id, ticket.id, inter.user.id))
            await db.commit()
        await inter.send(embed=embeds.Success(locale=inter.locale, description=data["success"].format(ticket=ticket.mention)))
        await ticket.send(data['greet'].format(user=inter.user.mention) if not support else data['greet_support'].format(user=inter.user.mention, support=support.mention))

def setup(bot: commands.Bot):
    bot.add_cog(TicketCog(bot))