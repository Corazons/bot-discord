import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
import requests
import pdf2docx

load_dotenv()

permissions = nextcord.Permissions()
permissions.update(manage_messages=True, manage_emojis=True)
token_api = os.getenv("token_api")
intents = nextcord.Intents.all()
intents.members = True
client = nextcord.Client()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'🚀 {bot.user.name} has connected to Discord! 🚀')


@bot.command(name='hi')
async def hello(ctx):
    await ctx.send(f'Hallo, saya {bot.user.name} 👋 \napa yang bisa saya bantu?')


@bot.command()
async def meme(ctx):
    respMeme = requests.get(
        'https://meme-api.com/gimme')
    meme = respMeme.json()['url']
    embed = nextcord.Embed(title="Meme Tanpa K")
    embed.set_image(url=meme)
    message = await ctx.send(embed=embed)
    for emoji in ['😂', '👍', '👎', '❤️']:
        await message.add_reaction(emoji)


@bot.command(name='joke')
async def joke(ctx):
    response = requests.get(
        'https://official-joke-api.appspot.com/jokes/random')
    setup = response.json()['setup']
    punch = response.json()['punchline']
    await ctx.send(f'{setup} \n{punch}')


@bot.command()
async def gambar(ctx):
    embed = nextcord.Embed(
        title='Gambar kucing',
        description='Ini adalah gambar kucing yang imut',
        color=nextcord.Color.yellow()
    )

    embed.set_image(url='https://source.unsplash.com/random/200x200')

    await ctx.send(embed=embed)


@bot.command()
async def checkbutton(ctx):
    question = 'mencoba mengubah warna tekan tombol dibawah '
    embed = nextcord.Embed(
        title='warna', description=question, color=nextcord.Color.blue())
    message = await ctx.send(embed=embed)

    for emoji in ['🔴', '🟢']:
        await message.add_reaction(emoji)


@bot.event
async def on_reaction_add(reaction, user):
    embed = reaction.message.embeds[0]
    new_embed = nextcord.Embed.from_dict(embed.to_dict())
    if user.bot:
        return

    if reaction.emoji == '🔴':
        print('{0} reacted with 🔴'.format(user.name))
        new_embed.colour = nextcord.Colour.red()

    elif reaction.emoji == '🟢':
        print('{0} reacted with 🟢'.format(user.name))
        new_embed.colour = nextcord.Colour.green()

    await reaction.message.edit(embed=new_embed)
    # Memastikan reaction tidak ditambahkan oleh bot

    # Mengambil pesan yang menerima reaction
    message = reaction.message
    # Memeriksa apakah reaction sebelumnya sudah ada
    for prev_reaction in message.reactions:

        if prev_reaction.emoji != reaction.emoji:
            # Mengambil daftar pengguna yang memberikan reaction pada reaction sebelumnya
            users = await prev_reaction.users().flatten()

            # Memeriksa apakah user yang memberikan reaction pada reaction sebelumnya
            # adalah user yang baru memberikan reaction
            if user in users:
                # Menghapus reaction sebelumnya
                await message.remove_reaction(prev_reaction.emoji, user)


@bot.command()
async def userinfo(ctx, member: nextcord.Member):
    embed = nextcord.Embed(title="User Info")
    embed.add_field(name="Name", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def pdf2word(ctx):
    # ambil pesan terkait
    message = ctx.message

    # pastikan pesan memiliki lampiran
    if not message.attachments:
        await ctx.send("⚠️Tidak ditemukan lampiran pada pesan ini.⚠️")
        return

    # ambil lampiran PDF dari pesan
    pdf_file = message.attachments[0]
    print(f'ini adalah pdf_fil = {pdf_file}')
    # pastikan bahwa lampiran PDF ditemukan pada pesan
    if not pdf_file.filename.endswith(".pdf"):
        await ctx.send("Tidak ada file PDF yang ditemukan.")
        return

    # download lampiran PDF
    with open(pdf_file.filename, "wb") as file:
        await pdf_file.save(file)

    # buka file PDF dan konversi ke file Word
    docx_filename = os.path.splitext(pdf_file.filename)[0] + ".docx"
    pdf2docx.parse(f"{pdf_file.filename}", f"{docx_filename}")

    # simpan file Word sebagai lampiran

    await message.reply(file=nextcord.File(docx_filename))
    os.remove(pdf_file.filename)
    os.remove(docx_filename)


bot.run(f'{token_api}')
