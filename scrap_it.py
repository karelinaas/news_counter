import sqlite3
import datetime
import sched
import sys
import time
from sqlite3 import Cursor

import requests
from bs4 import BeautifulSoup as bs

s = sched.scheduler(time.time, time.sleep)
minutes = sys.argv[3]


def scrap_it(sc):
    """
    Method gets page and scrapes titles.

    :param sc:
    :return:
    """
    # script params
    url = sys.argv[1]
    div_id = sys.argv[2]

    # initial variables values
    new_last_title = title = ''
    delta = 0
    end = False
    today = datetime.date.today().strftime('%Y-%m-%d')

    # get last title
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    row = cur.execute('SELECT * FROM last_titles ORDER BY date DESC LIMIT 1').fetchone()
    last_title = row[1] if row and len(row) > 1 else ''

    # get list of available proxies
    proxy_list = cur.execute('SELECT * FROM proxies').fetchall()

    # change proxy once per hour
    proxy = proxy_list[datetime.datetime.now().hour % len(proxy_list)][0]

    session = requests.Session()
    session.proxies = {
        'http': 'http://{0}'.format(proxy),
        'https': 'https://{0}'.format(proxy),
    }

    # html scrapper
    soup = bs(session.get(url).content, 'html.parser')
    for row in soup.find('div', attrs={'id': div_id}).find_all('div', attrs={'class': 'post'}):
        try:
            title_a = row.find('div', attrs={'class': 'title'}).find('a')
            title = title_a.text.strip()
        except Exception:
            # the last div.post doesn't have title
            end = True

        if not new_last_title:
            new_last_title = title

        if last_title and not end:
            if last_title == title:
                # add delta for now
                # save last filename
                insert_values(cur, 'updates', (today + ' ' + datetime.datetime.now().strftime('%H:%M:%S'), delta))

                if new_last_title != last_title:
                    insert_values(
                        cur,
                        'last_titles',
                        (today + ' ' + datetime.datetime.now().strftime('%H:%M:%S'), new_last_title),
                    )
                break

            delta += 1
        else:
            insert_values(cur, 'updates', (today + ' ' + datetime.datetime.now().strftime('%H:%M:%S'), delta))

            if title != last_title:
                insert_values(
                    cur,
                    'last_titles',
                    (today + ' ' + datetime.datetime.now().strftime('%H:%M:%S'), title),
                )
            break

    con.commit()
    con.close()
    s.enter(int(minutes) * 60, 1, scrap_it, (sc,))


def insert_values(cur: Cursor, table_name: str, values: tuple) -> None:
    """
    Method inserts values into table.

    :param cur:
    :param table_name:
    :param values:
    :return:
    """
    values_replacement = ', '.join(['?'] * len(values))
    query = 'INSERT INTO {0} VALUES ({1})'.format(table_name, values_replacement)

    cur.execute(query, values)


s.enter(int(minutes) * 60, 1, scrap_it, (s,))
s.run()
