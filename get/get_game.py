from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import sys

def get_from_url(url):
    html = urlopen(url).read()
    html = html.replace(b"&lt;", b"<")
    html = html.replace(b"&gt;", b">")
    soup = BeautifulSoup(html)
    table = soup.select_one('div#jeopardy_round').select_one('table.round')
    pull_from_table(table, url[-4:] + "_jeopardy_game.csv")
    table = soup.select_one('div#double_jeopardy_round').select_one('table.round')
    pull_from_table(table, url[-4:] + "_double_jeopardy_game.csv")
    final_table = soup.select_one("table.final_round")
    final_category = final_table.select_one("td.category_name").text
    final_clue = soup.select_one("td#clue_FJ").text
    final_str = str(final_table)
    final_answer = clean_str(final_str[final_str.index('correct_response')+16:final_str.index('/em')])
    with open('/tmp/' + url[-4:] + "_final_jeopardy.txt", "w") as f:
        f.write("\n".join((final_category, final_clue, final_answer)))
    return soup.select_one("div#game_title").select_one("h1").text

def clean_str(s):
    s = s.replace("lt;", "").replace("gt;", "").replace("quot", "").replace("\\", "").replace("&", "").replace(";", "") 
    if s[0] == 'i' and s[-2:] == '/i':
        s = s[1:-2]
    return s

def pull_from_table(table, filename):
    categories = [td.text for td in table.select("td.category_name")]
    print(categories)
    double = False
    for tr in table.select("tr"):
        if tr.find("td", {'class': 'clue'}):
            for td in tr.select("td.clue"):
                print(str(td.find('td', {'class': 'clue_text'})))
    clues = [[("Double Jeopardy: " if 'clue_value_daily_double' in str(td) else "") + td.select_one("td.clue_text").text if td.find('td', {'class': 'clue_text'}) else 'This clue was missing' for td in tr.select("td.clue") ] for tr in table.select("tr") if tr.find("td", {'class': 'clue'})]

    answers = [[clean_str(str(td)[str(td).index('correct_response')+16:str(td).index('/em')]) if 'correct_response' in str(td) else 'This answer was missing' for td in tr.select("td.clue")] for tr in table.select("tr") if tr.find("td", {'class': 'clue'})]
    with open('/tmp/' + filename, "w") as f:
        wr = csv.writer(f)
        wr.writerow(categories)
        wr.writerows(clues)
    with open('/tmp/' + filename[:-4] + "_answers.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(categories)
        wr.writerows(answers)
