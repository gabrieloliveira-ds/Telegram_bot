from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import myfunctions as myfunc
import myfilters 

###CALLBACKS

def setup(app):
    @app.on_callback_query()
    async def callbacks(client, callback_query):

        #recuperando dados da mensagem
        callback_msg=callback_query.message
        callback_chat=callback_msg.chat
        
        #pegando informações do link 
        #formatado do dado -> {msg_id}'|'{msg_from}{msg_type}  
        #msg_id: id unico da mensagem que contem o link 
        #link_from: a plataforma que o link veio('y': youtube | 'i': instagram)
        #media_type: 'informa o formato que deseja fazer o download('a': audio |'v': video|'0': none)'
        msg_id=int(callback_query.data.split('|')[0]) 
        link_from=callback_query.data.split('|')[1][0]
        media_type=callback_query.data.split('|')[1][1]

        #recuperando link atravez do id da mensagem
        message = await app.get_messages(chat_id = callback_chat.id, message_ids=msg_id)
        link=message.text
        
        #downlod media
        user=(message.from_user)
        if link_from == 'y':#pega do youtube        
            if(media_type=='a'):# se for pra baixar só o audio
                print('🔊',message.chat.username, 'solicitou um download de audio')
                await message.reply('Baixando pro servidor!')
                path=myfunc.download_audio(link=link,user=user.username,id=user.id)
                await message.reply('Enviando...')
                await app.send_audio(message.chat.id ,audio=path)
                print('🔊',message.chat.username, 'Recebeu o audio')
            if(media_type=='v'):# se for pra baixar só o video
                print('🎥',message.chat.username, 'solicitou um download de video')
                await message.reply('Baixando pro servidor!')
                path=myfunc.download_video(link=link,user=user.username,id=user.id) 
                await message.reply('Enviando...')
                await app.send_video(message.chat.id ,video=path)
                print('🎥',message.chat.username, 'Recebeu o video') 
            
        if link_from == 'i':#pega do instagram
            if(media_type=='d'):#se for para baixar o post
                print('📱',message.chat.username, 'solicitou um download de um post')
                await message.reply('Baixando pro servidor!')
                path=myfunc.download_post(user=user.username, id=user.id, IG=IG_obj, url=link)
                await message.reply('Enviando...')
                for item in path:
                    await app.send_photo(message.chat.id,photo=item)
                #myfunc.send_post(app,message.chat.id ,path)
                
            if(media_type=='i'):#se for para pear as informações
                await message.reply('⚠ função não realizada ainda ⚠')
                pass
            

    ###FILTERS
    #media
    @app.on_message(filters.photo)
    async def filter_photo(client, message):
        
        user=(message.from_user) 
        print('📷', f'@{message.chat.username}', f"(dimensions:{message.photo.width}x{message.photo.height} size:{message.photo.file_size})")
        await message.reply('nice foto :)')

        dir_path = myfunc.savepictures(message.chat.username,user.id)
        img_path = await message.download(dir_path+'/')
        sticker_path = myfunc.make_sticker(img_path)

        await app.send_sticker(message.chat.id,sticker_path)

    #commands
    @app.on_message(filters.command('help'))
    async def command_help(client, message):
        print(message.chat.username, message.text)
        await message.reply('COMO USAR:\n -> Envie o link do video do youtube que você deseja e ele irá enviar para você na maior resolução possivel\n -> Envie uma foto e receba uma figurinha')
        await message.reply('Esse server é um projeto em andamento ! Nem sempre ele esta ligado, apenas quando eu ligo meu pc e inicio o script')
        await message.reply('❗ cuidado com oque você manda ❗')
        await message.reply('❗ toda a conversa e videos ficam salvos no meu pc ❗')
        await message.reply('Não baixe videos muito grandes, pois eles pegam muito espaço de memoria do meu pc, use com moderação 👍')

    #links
    @app.on_message(myfilters.YTlink)
    async def download_youtube(client, message):
        
        link_info=myfunc.info_media(message.text)
        print('🔗',f'@{message.chat.username}', '(title:',link_info['title'],'|FROM: YOUTUBE)')
        origin='y'

        # converting string to bytes
        # essa mensagem será enviada para o botão do telegram que retornará o valor(callback_data) contido dentro 
        # do botal. É preciso fazer essa economia de espaço, pois o telegram só aceita no máximo 64bytes 
        msgvideo_id = (f"{message.id}|{origin}v").encode()#informa com o 'v' que é um formato de video
        msgaudio_id = (f"{message.id}|{origin}a").encode()#informa com o 'a' que é um formato de audio

        botoes = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Video',callback_data=msgvideo_id),
                    InlineKeyboardButton('Audio',callback_data=msgaudio_id)
                ]
            ]
        )
        await message.reply('Qual formato deseja o donwload?', reply_markup = botoes)

    @app.on_message(myfilters.IGlink)
    async def download_instagram(client,message):
        print('🔗',f'@{message.chat.username}', '|FROM: INSTAGRAM)')
        origin='i'

        # converting string to bytes
        # essa mensagem será enviada para o botão do telegram que retornará o valor(callback_data) contido dentro 
        # do botal. É preciso fazer essa economia de espaço, pois o telegram só aceita no máximo 64bytes 
        msgdownload_id = (f"{message.id}|{origin}d").encode()#informa com o 'v' que é um formato de video
        msginfo_id = (f"{message.id}|{origin}i").encode()#informa com o 'v' que é um formato de video
        botoes = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('donwload',callback_data=msgdownload_id),
                    InlineKeyboardButton('info',callback_data=msginfo_id)
                ]
            ]
        )
        await message.reply('Oque você quer do post?', reply_markup = botoes)

    #None
    @app.on_message()
    async def msg(client, message):
        print('📩',f'@{message.chat.username}', message.text,)
        teclado = ReplyKeyboardMarkup(
            [
                ['/help']
            ],resize_keyboard=True
        )
        await message.reply(
            'Digita/help',
            reply_markup = teclado
        )
