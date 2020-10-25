import discord

class Embeds():
    def __init__(self, platform, url, embed_description, thumbnail_url, color=0x4a90e2):
        self.platform = platform 
        self.url = url
        self.embed_description = embed_description
        self.thumbnail_url = thumbnail_url
        self.embed = discord.Embed(title=platform, 
                        colour=discord.Colour(color), 
                        url=self.url, 
                        description=self.embed_description)
        self.embed.set_thumbnail(url=self.thumbnail_url)

    def create_embed(self, name, value, date):
        '''For filling the data inside the embeds using the parameters'''
        desc = '{0}\nDate: {1}\nTime: {2}'.format(value, 
                                                  date.strftime("%A, %d %B %Y"), 
                                                  date.strftime("%I:%M %p"))
        self.embed.add_field(name=name, 
                             value=desc, 
                             inline=False)

        # self.embed.add_field(name="Date", 
        #                 value=date.strftime("%A, %d %B %Y"), 
        #                 inline=True)

        # self.embed.add_field(name="Time", 
        #                      value=date.strftime("%I:%M %p"), 
        #                      inline=True)

    def get_embed(self):
        '''Returns the embed'''
        return self.embed