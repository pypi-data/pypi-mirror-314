# coding: utf8

import requests as r

from .aes import AESCipher
from .services import TRELLO_CREDENTIALS, WEKAN_CREDENTIALS


class TrelloCard(object):
    """."""

    def __init__(self, board, list, card):
        """."""
        self.board_name = board
        self.list_name = list
        self.card_name = card
        self.params = {k: AESCipher().decrypt(v)
                       for (k, v) in TRELLO_CREDENTIALS.items()}
        self.base_url = "https://trello.com/1/"
        self.__get_board_id()
        self.__get_list_id()
        self.__get_card_id()

    def __get_board_id(self):
        """."""
        url = self.base_url + "organizations/sisap1/boards"
        boards = {board["name"]: board["id"]
                  for board in r.get(url, params=self.params).json()}
        self.board_id = boards[self.board_name]
        url = self.base_url + "members/me"
        response = r.get(url, params=self.params).json()
        myself_id = response["id"]
        url = self.base_url + "boards/{}/members/{}".format(self.board_id,
                                                            myself_id)
        args = {"type": "normal"}
        response = r.put(url, params=self.params, data=args).json()  # noqa

    def __get_list_id(self):
        """."""
        url = self.base_url + "boards/{}/lists".format(self.board_id)
        lists = {list["name"]: list["id"]
                 for list in r.get(url, params=self.params).json()}
        if self.list_name in lists:
            self.list_id = lists[self.list_name]
        else:
            args = {"name": self.list_name}
            response = r.post(url, params=self.params, data=args).json()
            self.list_id = response["id"]

    def __get_card_id(self):
        """."""
        url = self.base_url + "lists/{}/cards".format(self.list_id)
        cards = {card["name"]: card["id"]
                 for card in r.get(url, params=self.params).json()}
        if self.card_name in cards:
            self.card_id = cards[self.card_name]
        else:
            url = self.base_url + "cards"
            args = {"name": self.card_name, "idList": self.list_id}
            response = r.post(url, params=self.params, data=args).json()
            self.card_id = response["id"]

    def __update_card(self, key, value):
        """."""
        url = self.base_url + "cards/{}".format(self.card_id)
        args = {key: value}
        response = r.put(url, params=self.params, data=args).json()  # noqa

    def add_description(self, text):
        """."""
        self.__update_card("desc", text)

    def add_members(self, *names):
        """."""
        url = self.base_url + "organizations/sisap1/members"
        all_members = {member["username"]: member["id"]
                       for member in r.get(url, params=self.params).json()}
        url = self.base_url + "boards/{}/members".format(self.board_id)
        board_members = [member["id"]
                         for member in r.get(url, params=self.params).json()]
        card_members = [all_members[name] for name in names]
        for member in card_members:
            if member not in board_members:
                url = self.base_url + "boards/{}/members/{}".format(
                                                                self.board_id,
                                                                member)
                args = {"type": "normal"}
                response = r.put(url, params=self.params, data=args)  # noqa
        self.__update_card("idMembers", card_members)

    def add_labels(self, *labels):
        """."""
        url = self.base_url + 'boards/{}/labels'.format(self.board_id)
        params = self.params.copy()
        params["limit"] = 1000
        card_labels = [label['id']
                       for label in r.get(url, params=params).json()
                       if label['name'] in labels]
        self.__update_card('idLabels', card_labels)

    def add_date(self, dat):
        """."""
        self.__update_card('due', dat)

    def add_comment(self, text):
        """."""
        url = self.base_url + "cards/{}/actions/comments".format(self.card_id)
        args = {"text": text}
        response = r.post(url, params=self.params, data=args)  # noqa

    def add_to_checklist(self, checklist_name, item_name):
        """."""
        url = self.base_url + "cards/{}/checklists".format(self.card_id)
        checklists = {checklist["name"]: checklist["id"]
                      for checklist in r.get(url, params=self.params).json()}
        if checklist_name in checklists:
            checklist_id = checklists[checklist_name]
        else:
            args = {"name": checklist_name}
            response = r.post(url, params=self.params, data=args).json()
            checklist_id = response["id"]
        url = self.base_url + "checklists/{}/checkItems".format(checklist_id)
        items = {item["name"]: (item["id"], item["state"])
                 for item in r.get(url, params=self.params).json()}
        if item_name not in items:
            args = {"name": item_name}
            response = r.post(url, params=self.params, data=args).json()
        else:
            id, state = items[item_name]
            if state == "complete":
                s = "cards/{}/checklist/{}/checkItem/{}"
                url = self.base_url + s.format(self.card_id, checklist_id, id)
                args = {"state": "incomplete"}
                response = r.put(url, params=self.params, data=args)  # noqa


class WekanCard(object):
    """."""

    def __init__(self, board, swimlane, list, card):
        """."""
        self.board_name = board.decode('utf8')
        self.swimlane_name = swimlane.decode('utf8')
        self.list_name = list.decode('utf8')
        self.card_name = card.decode('utf8')
        self.base_url = "http://eines.portalics/wekan/"
        self.__get_token()
        self.__get_board_id()
        self.__get_swimlane_id()
        self.__get_list_id()
        self.__get_card_id()

    def __get_token(self):
        """."""
        url = self.base_url + "users/login"
        url = "http://eines.portalics/wekan/users/login"
        data = {"username": WEKAN_CREDENTIALS["usr"],
                "password": AESCipher().decrypt(WEKAN_CREDENTIALS["pwd"])}
        response = r.post(url, json=data).json()
        token = response["token"]
        self.headers = {"Accept": "application/json",
                        "Authorization": "Bearer {}".format(token)}

    def __get_user_id(self, user):
        """."""
        url = self.base_url + "api/users/{}".format(user)
        response = r.get(url, headers=self.headers).json()
        return (response["_id"])

    def __get_board_id(self):
        """."""
        self.user_id = self.__get_user_id(WEKAN_CREDENTIALS["usr"])
        url = "http://eines.portalics/wekan/api/users/{}/boards".format(self.user_id)  # noqa
        response = r.get(url, headers=self.headers).json()
        boards = {board["title"]: board["_id"] for board in response}
        self.board_id = boards[self.board_name]

    def __get_swimlane_id(self):
        """."""
        url = self.base_url + "/api/boards/{}/swimlanes".format(self.board_id)
        response = r.get(url, headers=self.headers).json()
        swimlanes = {swimlane["title"]: swimlane["_id"]
                     for swimlane in response}
        self.swimlane_id = swimlanes[self.swimlane_name]

    def __get_list_id(self):
        """."""
        url = self.base_url + "/api/boards/{}/lists".format(self.board_id)
        response = r.get(url, headers=self.headers).json()
        lists = {_list["title"]: _list["_id"] for _list in response}
        self.list_id = lists[self.list_name]

    def __get_card_id(self):
        """."""
        url = self.base_url + "/api/boards/{}/lists/{}/cards".format(self.board_id, self.list_id)  # noqa
        response = r.get(url, headers=self.headers).json()
        cards = {card["title"]: card["_id"] for card in response}
        if self.card_name in cards:
            self.card_id = cards[self.card_name]
        else:
            data = {"title": self.card_name, "authorId": self.user_id,
                    "description": "", "swimlaneId": self.swimlane_id}
            response = r.post(url, headers=self.headers, data=data).json()
            self.card_id = response["_id"]

    def __update_card(self, key, value):
        """."""
        url = self.base_url + "api/boards/{}/lists/{}/cards/{}".format(self.board_id, self.list_id, self.card_id) # noqa
        data = {key: value}
        response = r.put(url, headers=self.headers, data=data)  # noqa

    def add_description(self, text):
        """."""
        self.__update_card("description", text)

    def add_members(self, *users):
        """."""
        members = [self.__get_user_id(user) for user in users]
        self.__update_card("members", members)
        self.__update_card("assignees", members)

    def add_labels(self, *labels):
        """."""
        url = self.base_url + 'api/boards/{}'.format(self.board_id)
        response = r.get(url, headers=self.headers).json()["labels"]
        existents = {label["name"]: label["_id"] for label in response}
        ids = [existents[label.decode("utf-8")] for label in labels]
        self.__update_card('labelIds', ids)

    def add_date(self, dat):
        """."""
        self.__update_card('dueAt', dat)

    def add_comment(self, text):
        """."""
        url = self.base_url + "api/boards/{}/cards/{}/comments".format(self.board_id, self.card_id)  # noqa
        data = {"authorId": self.user_id, "comment": text}
        response = r.post(url, headers=self.headers, data=data)  # noqa

    def add_to_checklist(self, checklist_name, item_name):
        """."""
        # checklist
        url = self.base_url + "api/boards/{}/cards/{}/checklists/".format(self.board_id, self.card_id)  # noqa
        response = r.get(url, headers=self.headers).json()
        checklists = {checklist["title"]: checklist["_id"]
                      for checklist in response}
        if checklist_name in checklists:
            checklist_id = checklists[checklist_name]
        else:
            data = {"title": checklist_name}
            response = r.post(url, headers=self.headers, data=data).json()
            checklist_id = response["_id"]
        # existents
        url += checklist_id
        response = r.get(url, headers=self.headers).json()["items"]
        existents = {item["title"]: item["_id"] for item in response}
        # item
        url += "/items/"
        if item_name in existents:
            r.delete(url + existents[item_name], headers=self.headers)
        data = {"title": item_name}
        response = r.post(url, headers=self.headers, data=data).json()

    def add_peticionari(self, peticionari):
        """."""
        url = self.base_url + "api/boards/{}/custom-fields/".format(self.board_id)  # noqa
        response = r.get(url, headers=self.headers).json()
        field_id = [field["_id"] for field in response
                    if field["name"] == "Peticionari"][0]
        url += field_id
        response = r.get(url, headers=self.headers).json()["settings"]["dropdownItems"]  # noqa
        options = {option["name"]: option["_id"] for option in response}
        url = self.base_url + "api/boards/{}/lists/{}/cards/{}/customFields/{}".format(self.board_id, self.list_id, self.card_id, field_id)  # noqa
        data = {"value": options[peticionari]}
        response = r.post(url, headers=self.headers, data=data).json()
