from bs4 import BeautifulSoup
import urllib.request
import time


def handle_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    return urllib.request.Request(url=url, headers=headers)


def parse_content(content):
    # 生成soup对象
    soup = BeautifulSoup(content, 'lxml')
    # 找到所有的标题和链接
    a_title_href_list = soup.select('.book-mulu > ul > li > a')
    # print(a_title_href_list)
    # print(len(a_title_href_list))
    # 遍历列表，获取标题和链接
    for oa in a_title_href_list:
        # 获取标题
        title = oa.string
        # 获取链接
        href = 'http://www.shicimingju.com' + oa['href']
        # 向这个href发送请求
        text = get_chapter_text(href)

        string = title + '\n' + text + '\n'
        print(string)
        with open('sanguo.txt', 'a', encoding='utf8') as fp:
            fp.write(string)

        time.sleep(1)


def get_chapter_text(href):
    # 构建请求对象
    request = handle_request(href)
    #
    content = urllib.request.urlopen(request).read().decode('utf8')
    soup = BeautifulSoup(content, 'lxml')
    # 获取指定内容
    text = soup.find('div', class_='chapter_content').text
    return text


def main():
    url = 'http://www.shicimingju.com/book/sanguoyanyi.html'
    request = handle_request(url)
    # 发送请求，获取响应
    content = urllib.request.urlopen(request).read().decode('utf8')
    # 解析内容
    parse_content(content)


if __name__ == '__main__':
    main()
