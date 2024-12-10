from .NizimaRequest import NizimaRequest
import os


class NizimaPlugin(NizimaRequest):

    def __init__(self, plugin_infos, **kwargs):
        self.plugin_infos = plugin_infos
        self.plugin_name = plugin_infos['Name']
        self.token = ''
        self.connection = False
        NizimaRequest.__init__(self, **kwargs)

    async def connect_nizima(self, token_path='', token_filename=None):

        if not token_filename:
            token_filename = os.path.join(token_path, f'token_{self.plugin_name}.txt')

        self.token = self.load_token(token_filename)
        if not self.token:
            # if user delete plugin in nizima, user would need a new token
            await self.register_plugin(name=self.plugin_name, developer=self.plugin_infos['Developer'])
            self.save_token(self.token, token_filename)

        # no token : register plugin and save token
        # connect to nizima
        while not self.connection:
            response = await self.establish_connection(name=self.plugin_name, token=self.token)
            # if user delete plugin in nizima, user would need a new token (if old token will make an invalidMethod
            if response['Data']['Enabled']:
                self.connection = True
                return True

        return False

    def save_token(self, token, token_filename):
        """
        Save a token to a file.
        :param token: The token to save (string).
        """
        with open(token_filename, 'w') as file:
            file.write(token)

    def load_token(self, token_filename):
        """
        Retrieve a token from a file. Load the existing token if available
        :return: The retrieved token (string) or None if the file does not exist.
        """
        if os.path.exists(token_filename):
            with open(token_filename, 'r') as file:
                return file.read().strip()
        else:
            print(f"File not found: {token_filename}")
            return None
