# telegram-chat-full-media-download
this script is used to download all media from any amount of chats from telegram
## Configuration
Getting your API Keys: The very first step requires you to obtain a valid Telegram API key (API id/hash pair):

Visit https://my.telegram.org/apps and log in with your Telegram Account.
Fill out the form to register a new Telegram application.
Done! The API key consists of two parts: api_id and api_hash.
put this into the the variable api_id and the api_hash inside the code

folder id the folder where the the media will be downloaded

Getting chat id from the chat the media will be downloaded:

Open https://web.telegram.org
Now go to the chat/channel and you will see the URL as something like
https://web.telegram.org/#/im?p=u853521067_2449618633394 here 853521067 is the chat id.
https://web.telegram.org/#/im?p=@somename here somename is the chat id.
https://web.telegram.org/#/im?p=s1301254321_6925449697188775560 here take 1301254321 and add -100 to the start of the id => -1001301254321.

it also accepts the "@" from the user and the phone number

it have to be used as an array like: `["@bot","@chat","+5500000000000000"]` 

the amount of threads will define the amount of concurrent downloads,if you put an high value the pc could lag and if you put low value it will take much time to download

the proxy settings is not tested yet,so it has been disabled by now
`PROXYHOST=""`
`PROXYUSERNAME=""`
`PROXYPASSWORD=""`
this values are self descritives

## files saved

the files saved are inside the folder definded into config,the filenames are renamed as the message id and file name
this is done to avoid to download different files with same names , later will be made activate an variable to remove this message id
