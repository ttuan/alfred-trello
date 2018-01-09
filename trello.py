 # encoding: utf-8

import os
import sys
import pdb
from workflow import Workflow, ICON_WEB, web

API_KEY = os.environ['TRELLO_API_KEY']
API_TOKEN = os.environ['TRELLO_API_TOKEN']

# Need more refactor =]]

def main(wf):
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

    cards = []
    for l in doing_lists:
        url = 'https://trello.com/1/lists/' + l['id'] + '/cards'
        params = dict(token=API_TOKEN, key=API_KEY)
        rq = web.get(url, params)
        cards += rq.json()

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
