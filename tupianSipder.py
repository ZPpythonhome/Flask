from bs4 import BeautifulSoup
import lxml
soup = BeautifulSoup(open('soup_test.html', encoding='utf8'), 'lxml')
print(soup.a)
print(soup.a['href'])
print(soup.a['title'])