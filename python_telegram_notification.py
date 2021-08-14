import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from termcolor import colored
import yaml

class telegram_notification:
    def __init__(self, path_to_confidential_file='confidential_do_not_upload_to_github.yaml', add_prefix=''):
        in_ = ''
        self.add_prefix = add_prefix
        if not os.path.exists(path_to_confidential_file):
            in_ = input(colored('if you would like to set up telegram notifications press Enter. If you just Want to continue write \"NO\": \n',
                                color='yellow', attrs=['underline', 'bold', 'blink', 'reverse']))

            if in_.upper() != 'NO':
                with open(path_to_confidential_file, 'w') as confidential_yaml_file:
                    confidential_yaml_file.write('bot_token: xxxx\n')
                    confidential_yaml_file.write('chat_id: xxxx')
                print(colored(
                    'Create a telegram bot. this is done by: \
                    \n1) downloading and signing into telegram.  \
                    \n2) starting a chat with \"BotFather\" \
                    \n3) send him the text "/newbot", then follow the "BotFather" instraction to create the bot \
                    \n4) when you are done you will receive a the new bot token. enter the token into the file: "' + path_to_confidential_file + '" which was create in the current directory',
                    color='red', attrs=['underline', 'bold', 'blink', 'reverse']))
                input(colored('when you are done press Enter \n', color='yellow', attrs=['underline', 'bold', 'blink', 'reverse']))

        if in_.upper() != 'NO':
            confidential_conf = get_config(path_to_confidential_file)
            while confidential_conf['bot_token'] == 'xxxx':
                print(colored('telegram bot TOKEN not defined yet', color='yellow', attrs=['underline', 'bold', 'blink', 'reverse']))
                print(colored(
                    'Create a telegram bot. this can be done by \
                    \n1) downloading and signing into telegram.  \
                    \n2) starting a chat with \"BotFather\" \
                    \n3) send him the text "/newbot", then follow the "BotFather" instraction to create the bot \
                    \n4) when you are done you will receive a the new bot token. enter the token into the file: "' + path_to_confidential_file + '" which was create in the current directory',
                    color='red', attrs=['underline', 'bold', 'blink', 'reverse']))
                input(colored('when you are done press Enter \n', color='yellow', attrs=['underline', 'bold', 'blink', 'reverse']))
                print('...')
                confidential_conf = get_config(path_to_confidential_file)

            def telegram_command(update, context):
                context.bot.sendMessage(update.message.chat_id,
                                        text='enter chat_id in to: ' + path_to_confidential_file + ' as:')
                context.bot.sendMessage(update.message.chat_id, text='chat_id: ' + str(update.message.chat_id))

            def telegram_start(update, context):
                context.bot.sendMessage(update.message.chat_id,
                                        text='enter chat_id in to: ' + path_to_confidential_file + ' as:')
                context.bot.sendMessage(update.message.chat_id, text='chat_id: ' + str(update.message.chat_id))

            updater = Updater(token=confidential_conf['bot_token'], use_context=True)
            dispatcher = updater.dispatcher
            dispatcher.add_handler(MessageHandler(Filters.text, telegram_command))
            dispatcher.add_handler(CommandHandler('start', telegram_start))
            updater.start_polling()
            while confidential_conf['chat_id'] == 'xxxx':
                print(colored(
                    'CHAT ID is not defined send your telegram bot a random message to get your chat id, then enter it into the file:' + path_to_confidential_file,
                    color='red', attrs=['underline', 'bold', 'blink', 'reverse']))
                input(colored('when you are done press Enter \n', color='yellow', attrs=['underline', 'bold', 'blink', 'reverse']))
                print('...')
                confidential_conf = get_config(path_to_confidential_file)
            updater.stop()
            try:
                self.telegram_bot = telegram.Bot(token=confidential_conf['bot_token'])
                self.bot_token = confidential_conf['bot_token']
                self.chat_id = confidential_conf['chat_id']
                print(colored('Telegram notification active \n', color='green', attrs=['underline', 'bold', 'blink', 'reverse']))
            except Exception as e:
                print(colored('Failed to set up Telegram notification \n \n', color='red', attrs=['underline', 'bold', 'blink', 'reverse']))
                print(colored(str(e), color='red', attrs=['underline', 'bold', 'blink', 'reverse']))

    def send_message(self, bot_message):
        try:
            self.telegram_bot.send_message(chat_id=self.chat_id, text=self.add_prefix + bot_message)
        except:
            print('telegram send_message Failed')

    # def send_photo(self, bot_image, caption=None):
    #     try:
    #         caption = caption if caption is not None else bot_image.split('/')[-1]
    #         caption = self.add_prefix + caption
    #         self.telegram_bot.send_photo(chat_id=self.chat_id, photo=bot_image, caption=caption)
    #     except:
    #         print('telegram send_photo Failed')

    def send_document(self, bot_document_path, filename=None):
        try:
            filename = filename if filename is not None else bot_document_path.split('/')[-1]
            filename = self.add_prefix + filename
            self.telegram_bot.send_document(chat_id=self.chat_id, document=open(bot_document_path, 'rb'), filename=filename)
        except:
            print('telegram send_document Failed')

def get_config(config):
    with open(config, 'r') as stream:
        return yaml.safe_load(stream)