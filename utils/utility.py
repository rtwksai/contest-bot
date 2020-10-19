import discord

class Embeds():
    def __init__(self, platform, url, embed_description, thumbnail_url):
        self.platform = platform 
        self.url = url
        self.embed_description = embed_description
        self.thumbnail_url = thumbnail_url
        self.embed = discord.Embed(title=platform, 
                        colour=discord.Colour(0x4a90e2), 
                        url=self.url, 
                        description=self.embed_description)
        self.embed.set_thumbnail(url=self.thumbnail_url)

    def create_embed(self, name, value, date):
        '''For filling the data inside the embeds using the parameters'''
        self.embed.add_field(name=name, 
                             value=value, 
                             inline=True)

        self.embed.add_field(name="Date", 
                             value=date, 
                             inline=True)

    def get_embed(self):
        '''Returns the embed'''
        return self.embed