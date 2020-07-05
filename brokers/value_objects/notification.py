from brokers.onesignal.languages import LANGUAGES


class Notification:

    def __init__(self, url, app_id):

        self.__url = url
        self.__app_id = app_id
        self.__contents = dict()
        self.__headings = dict()

        self.__include_player_ids = list()

        self.django_notification_id = None

        self.errors = dict()
        self._check_errors()

    @property
    def url(self):
        return self.__url

    @property
    def app_id(self):
        return self.__app_id

    @property
    def contents(self):
        return self.__contents

    @property
    def headings(self):
        return self.__headings

    @property
    def include_player_ids(self):
        return self.__include_player_ids

    def add_heading(self, language, plain_text):
        self.headings[language] = plain_text

    def add_content(self, language, plain_text):
        self.contents[language] = plain_text

    def add_player_id(self, player_id: str):
        self.__include_player_ids.append(player_id)

    def is_valid(self):
        self._check_errors()
        return len(self.errors) == 0

    def _check_errors(self):
        accepted_languages = LANGUAGES.keys()

        for lang in self.headings.keys():
            if lang not in accepted_languages:
                self.errors['headings'] = f'Language not accepted: {lang}'

        for lang in self.contents.keys():
            if lang not in accepted_languages:
                self.errors['contents'] = f'Language not accepted: {lang}'

    def __iter__(self):
        if self.is_valid() is False:
            msg = 'Notification not valid:'

            for k, v in self.errors.items():
                msg += ' {}: {}.'.format(k, v)

            raise Exception(msg)

        iters = {
            'app_id': self.__app_id,
            'url': self.__url,
            'headings': self.__headings,
            'contents': self.__contents,
            'include_player_ids': self.__include_player_ids,
        }

        # now 'yield' through the items
        for x, y in iters.items():
            yield x, y
