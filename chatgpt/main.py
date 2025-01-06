from pyrogram import Client, filters, enums
from pyrogram.types import *
from HorridAPI import Mango
from config import ADMINS, LOG_CHANNEL, FSUB_ID
from database.db import *
from .fsubb import not_subscribed

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(c, m):
    k = users.count_documents({})
    await m.reply_text(f"**Total user**: {k}")

@Client.on_message(filters.command("broadcast") & filters.reply & filters.private & filters.user(ADMINS))
async def broadcast(client, message):
    try:        
        userr = users.find()  
        broadcast_msg = message.reply_to_message

        total_broadcast_count = 0
        failed_count = 0

        for user in userr:
            try:              
                await broadcast_msg.copy(chat_id=user["user"])
                total_broadcast_count += 1
            except Exception as e:
                print(f"Failed to send message to {user}: {str(e)}")
                failed_count += 1

        await message.reply(f"Broadcast complete! Sent to {total_broadcast_count} users. Failed to send to {failed_count} users.")

    except Exception as e:
        await message.reply(f"Error: {str(e)}")

mango = Mango()

START = """👋 Hey there! I’m an Advanced ChatGPT Bot.

**🎭 Text Models:**

» `/mode` - Add your preferred mode.
» `settings` - Change the AI model or add your favorite AI.

You can use this to reply with text and also support replies to images.

If the group replies to the bot using text, you can also use commands such as @{botusername} hi or hello @{botusername}.

**📜 LLM Models:**

» `/llama` - LLAMA by meta.
» `/claude` - Better ai claude by Anthropic.
» `/gpt` - Gpt-3.5-Turbo by Openai.
» `/gpt4` - GPT-4 by Openai.
» `/gemma` - Gemma Ai by Google.
» `/blackbox` - Real time Ai by Blackbox.
» `/google` - Gemini by Google.

**📋 Misc:**

» `/img` - image Download.

Feel free to ask me anything for free! 

**💬 Support: @TELLYCLOUD_BOTS**"""

@Client.on_callback_query()
async def callback(client, query):
    user_id = query.from_user.id
    if query.data.startswith("set"):
        chat = query.data.split(":")[1]
        users.update_one({"user": user_id}, {"$set": {"chat": chat}})
        await query.answer(f"has been set to {chat}.")
    elif query.data.startswith("mode"):
        mode = query.data.split(":")[1]
        # Custom prompts for specific modes
        if mode == "Tanjiro":
            custom = "You are Tanjiro, a helpful assistant from Demon Slayer. Your goal is to support and guide users in their inquiries, showcasing determination and kindness."  
        elif mode == "assistant":
            custom = "You are a helpfull assistant"
        elif mode == "dev":
            custom = "You are a pro Developer, You are help in coding, You are a pro in coding, You like assist in coding, You clear doubts in coding, You are a helpfull assistant in coding"
        elif mode == "naru":
            custom = "You are Naruto, You from Naruto Anime, You make emoji in response, You are shiboni blood and 7th hokage, You wifi is hinata, Minato sell Nine tail in Yours, You are a Nine tail Jinchuriki"
        elif mode == "ElonMusk":
            custom = "You are elon musk you act like elon musk, you are founder or Tesla, also space x, You are a billionaire person, You are rich"
        elif mode == "AlbertEinstein":
            custom = "You are Albert Einstein You act like Albert Einstein, You are A helpfull assistant also you make emoji in response, You are a pro, You are a intelligent 🤓, You IQ is 999999+"
        users.update_one({"user": user_id}, {"$set": {"mode": custom}})        
        await query.answer(f"Your mode has been set to {mode}.")

@Client.on_message(filters.command("start"))
async def start(client, message):
    if FSUB_ID and not await not_subscribed(client, message):
        invite_link = await client.create_chat_invite_link(int(FSUB_ID))
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ", url=invite_link.invite_link)]]
        text = f"Hey {message.from_user.mention}\n You are not joined this channel"
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        return 
    user_id = message.from_user.id
    if not users.find_one({"user": user_id}):
        users.insert_one({"user": user_id, "mode": "assistant", "chat": "gpt-3.5"})
        await client.send_message(chat_id=LOG_CHANNEL, text=f"#Newuser\nName: {message.from_user.mention}")
    await message.reply_text(START)        

@Client.on_message(filters.command("settings"))
async def settings(client, message):
    if FSUB_ID and not await not_subscribed(client, message):
        invite_link = await client.create_chat_invite_link(int(FSUB_ID))
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ", url=invite_link.invite_link)]]
        text = f"Hey {message.from_user.mention}\n You are not joined this channel"
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        return 
    user_id = message.from_user.id
    btns = [
        [InlineKeyboardButton("Gpt-3.5-turbo", callback_data="set:gpt-3.5-turbo")],
        [InlineKeyboardButton("Llama", callback_data="set:llama3-70b")],
        [InlineKeyboardButton("Gpt-4o-mini", callback_data="set:gpt-4o-mini")],
        [InlineKeyboardButton("Gpt-4o", callback_data="set:gpt-4o")],
        [InlineKeyboardButton("Gpt-4-turbo", callback_data="set:gpt-4o-turbo")],
        [InlineKeyboardButton("Gemini-1.5-flash", callback_data="set:gemini-1.5-flash")],
        [InlineKeyboardButton("Gemma-2", callback_data="set:gemma-2")]
    ]
    reply_markup = InlineKeyboardMarkup(btns)
    await message.reply_text("Select your Ai model:", reply_markup=reply_markup)

@Client.on_message(filters.command("mode"))
async def mode(client, message):    
    if FSUB_ID and not await not_subscribed(client, message):
        invite_link = await client.create_chat_invite_link(int(FSUB_ID))
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ", url=invite_link.invite_link)]]
        text = f"Hey {message.from_user.mention}\n You are not joined this channel"
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        return 
    btns = [
        [InlineKeyboardButton("🧑‍🎤 Albert Einstein", callback_data="mode:AlbertEinstein")],
        [InlineKeyboardButton("🪄 Assistant", callback_data="mode:assistant")],
        [InlineKeyboardButton("🚀 Elon Musk", callback_data="mode:ElonMusk")],       
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="mode:dev")],
        [InlineKeyboardButton("👨‍🎤 Naruto", callback_data="mode:naru")],
        [InlineKeyboardButton("🗡️ Tanjiro", callback_data="mode:Tanjiro")]
    ]
    reply_markup = InlineKeyboardMarkup(btns)
    await message.reply_text("Please choose a mode:", reply_markup=reply_markup)

@Client.on_message()
async def chats(client, message):    
    if FSUB_ID and not await not_subscribed(client, message):
        invite_link = await client.create_chat_invite_link(int(FSUB_ID))
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ", url=invite_link.invite_link)]]
        text = f"Hey {message.from_user.mention}\n You are not joined this channel"
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        return 
    if f"@{client.me.username}" in message.text:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        user_id = message.from_user.id    
        user_data = users.find_one({"user": user_id})        
        if user_data is None:
            await message.reply_text("You are not started me. So please start me.")
            return    

        l = message.reply_to_message    
        if l:
            prompt = f"Old conversation: {l.text}\n\nNew conversation: {message.text}"
        else:
            prompt = message.text
    
        if user_data["mode"] == "assistant":  
            payload = [{"role": "user", "content": prompt}]
        else:
            payload = [
                {"role": "system", "content": user_data['mode']},  
                {"role": "user", "content": prompt}                   
            ]
        
        response = mango.chat.completions.create(
            model=user_data["chat"], 
            messages=payload
        )
        await message.reply_text(response.text)
        return 
    if message.chat.type != enums.ChatType.PRIVATE:        
        if message.reply_to_message.from_user.id == client.me.id:  
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
            user_id = message.from_user.id    
            user_data = users.find_one({"user": user_id})        
            if user_data is None:
                await message.reply_text("You are not started me. So please start me.")
                return    

            l = message.reply_to_message     
            prompt = f"Old conversation: {l.text}\n\nNew conversation: {message.text}"
    
            if user_data["mode"] == "assistant":  
                payload = [{"role": "user", "content": prompt}]
            else:
                payload = [
                    {"role": "system", "content": user_data['mode']},  
                    {"role": "user", "content": prompt}                   
                ]
        
            response = mango.chat.completions.create(
                model=user_data["chat"], 
                messages=payload
            )
            await message.reply_text(response.text)
    if message.chat.type == enums.ChatType.PRIVATE:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        user_id = message.from_user.id
        if not users.find_one({"user": user_id}):
            users.insert_one({"user": user_id, "mode": "assistant", "chat": "gpt-3.5"})

        user_data = users.find_one({"user": user_id})
        
        if user_data is None:
            await message.reply_text("Error: Please try again in few seconds.")
            return    

        l = message.reply_to_message   
        if l:
            prompt = f"Old conversation: {l.text}\n\nNew conversation: {message.text}"
        else:
            prompt = message.text
        if user_data["mode"] == "assistant":  
            payload = [{"role": "user", "content": prompt}]
        else:
            payload = [
                {"role": "system", "content": user_data['mode']},  
                {"role": "user", "content": prompt}                   
            ]
        
        response = mango.chat.completions.create(
            model=user_data["chat"], 
            messages=payload
        )
        await message.reply_text(response.text)
