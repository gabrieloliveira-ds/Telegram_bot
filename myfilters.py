from pyrogram import filters

async def YTlink_filter(_,__, m):
    substrings= ['http://www.youtu','https://www.youtu','https://youtu','http://youtu']
    
    for item in substrings:
        if item in m.text:
            return True
    return False

YTlink = filters.create(YTlink_filter)

async def IGlink_filter(_,__, m):
    substrings= ['http://www.instagram.com','https://www.instagram.com']
    
    for item in substrings:
        if item in m.text:
            return True
    return False

IGlink = filters.create(IGlink_filter)