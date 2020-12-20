import asyncio
import os
#import socks
import telethon
from telethon import TelegramClient, sync
#import logging
api_id=0000000
api_hash='2343478g762347g4uhdvfcueru'
folder="./"
chanels=["@bot","@chat"]
total_threads=10
PROXYHOST=""
PROXYUSERNAME=""
PROXYPASSWORD=""
show_progress=True
#logging.basicConfig(level=logging.DEBUG)


def clean_temporary():
    files_in_directory = os.listdir(folder)
    filtered_files = [file for file in files_in_directory if file.endswith(".tmp")]
    for file in filtered_files:
        path_to_file = os.path.join(folder, file)
        os.remove(path_to_file)
        
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def order(element):
    return element.document.size

async def get_messages(client):
    messages=[]
    for chanel in chanels:
        tmp1=0
        total_messages=await client.get_messages(chanel)
        total_messages=total_messages.total
        async for a in client.iter_messages(chanel):
            if type(a.media) is telethon.tl.types.MessageMediaDocument:
                for i in a.media.document.attributes:
                    if type(i) is telethon.tl.types.DocumentAttributeFilename:
                        if not os.path.isfile(folder+str(a.id) + "_" + str(i.file_name)):
                            messages.append(a)
            print("processed "+str(tmp1)+" of "+str(total_messages)+" messages", end="\r")
            tmp1+=1
        print("processed "+str(tmp1)+" of "+str(total_messages)+" messages", end="\r")
        print()
    messages.sort(key=order)
    
    return messages

async def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total), end="\r")
    if (current / total)> 99:
        print("\n")

async def download(client,message):
    file = ""
    #print(message)
    for i in message.media.document.attributes:
        if type(i) is telethon.tl.types.DocumentAttributeFilename:
            file = folder+str(message.id) + "_" + str(i.file_name)
            if not os.path.isfile(file):
                try:
                    if show_progress:
                        await client.loop.create_task(message.download_media(progress_callback=callback, file=file + ".tmp"))
                        os.rename(file + ".tmp", file)
                        print("\n"+str(file))
                    else:
                        await client.loop.create_task(message.download_media(file=  file + ".tmp"))
                        os.rename(file + ".tmp",  file)
                        print("\n"+str(file))

                except Exception as e:
                    print("\n\n\n"+str(e)+"\n\n\n")
                    try:
                        if show_progress:
                            await client.loop.create_task(message.download_file(progress_callback=callback, file= file + ".tmp"))
                            os.rename( file + ".tmp", file)
                            print("\n"+str(file))
                        else:
                            await client.loop.create_task(message.download_file(file= file + ".tmp"))
                            os.rename( file + ".tmp",  file)
                            print("\n"+str(file))
                    except:
                        pass
                        
async def download_list(client,messages):
    for message in messages:
        await download(client,message)

async def main_splited_array(threads):
#    if PROXYHOST == PROXYUSERNAME == PROXYPASSWORD == "":
#        client = TelegramClient("session_file", api_id, api_hash,
#                            proxy=(socks.SOCKS5, PROXYHOST, PORT, PROXYUSERNAME, PROXYPASSWORD)
#                            )
#    else:
    client = TelegramClient("session_file", api_id, api_hash)
    await client.start()
    messages=await get_messages(client)
    #splited_array=chunks(messages,total_elements)
    process=[]
    init=0
    final=int(len(messages)/threads)
    for i in range(threads):
        process.append(asyncio.ensure_future(download_list(client,messages[init:final])))
        print("init=" + str(init) + "  final=" + str(final))
        init=final
        final=int(final+len(messages)/threads)
    print("total threads="+str(len(process)))
    print("total elements="+str(len(messages)))
    await asyncio.gather(*process)

async def main_single_array(threads):
#    if PROXYHOST == PROXYUSERNAME == PROXYPASSWORD == "":
#        client = TelegramClient("session_file", api_id, api_hash,
#                            proxy=(socks.SOCKS5, PROXYHOST, PORT, PROXYUSERNAME, PROXYPASSWORD)
#                            )
#    else:
    client = TelegramClient("session_file", api_id, api_hash)
    await client.start()
    messages=await get_messages(client)
    process=[]
    total_elements=len(messages)
    print("total elements="+str(total_elements))
    last_processed=0
    while last_processed<=total_elements:
        print(messages[last_processed])
        print(len([task for task in asyncio.all_tasks() if not task.done()]))
        if len([task for task in asyncio.all_tasks() if not task.done()])<threads:
            loop.run_until_complete(asyncio.create_task(download(client,messages[last_processed])))
            last_processed+=1
        else:
            while not len([task for task in asyncio.all_tasks() if not task.done()])<threads:
                time.sleep(1)
            #for task in asyncio.all_tasks():
            #    if task.done():
            #        process.remove(task)
    #await asyncio.gather(*process)

if __name__ == "__main__":
    loop=asyncio.get_event_loop()
    while True:#due to an telegram life time of session or something like that this is necessary to completly download media
        # the error shows this return code : The file reference has expired and is no longer valid or it belongs to self-destructing media and cannot be resent (caused by GetFileRequest)
        # to avid this,just restart the script or wait until it finishes each while loop run
        clean_temporary()
        loop.run_until_complete(main_splited_array(total_threads))
    loop.close()
        
