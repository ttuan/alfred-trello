 # encoding: utf-8

import os
import sys
import pdb
from workflow import Workflow, ICON_WEB, web

API_KEY = 'your-api-key'
API_TOKEN = 'your-api-token'

# Need more refactor =]]
def get_doing_lists():
    url = 'https://trello.com/1/members/me'
    params = dict(token=API_TOKEN, key=API_KEY, boardStars='true')
    r = web.get(url, params)
    r.raise_for_status()

    result = r.json()
    starredBoards = result['boardStars']

    doing_lists = []
    for board in starredBoards:
        url = 'https://trello.com/1/boards/' + board['idBoard'] + '/lists'
        params = dict(token=API_TOKEN, key=API_KEY)
        rq = web.get(url, params)
        board_lists = rq.json()
        for l in board_lists:
            if l['name'] == 'DOING':
                doing_lists.append(l)
    return doing_lists

def get_doing_cards():
    doing_lists = wf.cached_data('doing_lists', get_doing_lists, max_age=9999999)
    cards = []
    for l in doing_lists:
        url = 'https://trello.com/1/lists/' + l['id'] + '/cards'
        params = dict(token=API_TOKEN, key=API_KEY)
        rq = web.get(url, params)
        cards += rq.json()
    return cards

def main(wf):
    cards = wf.cached_data('cards', get_doing_cards, max_age=3600)

    for card in cards:
        wf.add_item(title=card['name'],
                 subtitle=card['url'],
                 arg=card['url'],
                 valid=True,
                 icon=ICON_WEB)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
