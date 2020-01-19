import bs4
import requests
import os
import urllib.request, urllib.error
import argparse
import datetime
import json


def get_soup(url, header):
    return bs4.BeautifulSoup(requests.get(url, headers=header).text, 'html.parser')


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', type=str)
    parser.add_argument('-n', '--num_images', default=10, type=int)
    parser.add_argument('-d', '--directory', type=str)

    args = parser.parse_args()
    print(args)

    if not args.search:
        print('検索ワードを指定してください')
        return

    if not args.directory:
        print('ディレクトリを指定してください')
        return

    query = args.search.split()
    query = "+".join(query).replace('"', '')
    max_images = args.num_images

    save_directory = "data/" + args.directory
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    url = "https://www.google.co.jp/search?q=" +query+ "&source=lnms&tbm=isch"
    header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    soup = get_soup(url, header)
    ActualImages = []

    for i, a in enumerate(soup.find_all('div', {'class': 'rg_meta'})):
        link, Type = json.loads(a.text)['ou'], json.loads(a.text)['ity']
        if Type == "png" or Type == "jpg":
            ActualImages.append((link, Type))
    print(f"number of find images is {len(ActualImages)}")
    print(ActualImages[0][0][:10])

    count = 0
    uuid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for i, (img, Type) in enumerate(ActualImages):
        try:
            print(f'Downloading image {i} ({img}), type is {Type}')
            raw_img = urllib.request.urlopen(img).read()
            print(type(raw_img))
            with open(os.path.join(save_directory, f"img_{uuid}_{str(i)}.{Type}"), 'wb') as f:
                f.write(raw_img)
                count += 1
                if count == max_images:
                    print(f"COUNT: {count}")
                    break
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    from sys import argv
    main(argv)
