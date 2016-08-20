from bs4 import BeautifulSoup
import re

#Problem 1
# Part 1
print 'html', 'head', 'title', 'meta', 'style', 'body', 'div', 'h1', 'p', 'a'

# Part 2
print "text/css"


#Problem 2
html_doc = """
<html><head><title>The Three Stooges</title></head>
<body>
<p class="title"><b>The Three Stooges</b></p>
<p class="story">Have you ever met the three stooges? Their names are
<a href="http://example.com/larry" class="stooge" id="link1">Larry</a>,
<a href="http://example.com/mo" class="stooge" id="link2">Mo</a> and
<a href="http://example.com/curly" class="stooge" id="link3">Curly</a>;
and they are really hilarious.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc)
print(soup.prettify())

#Problem 3
soup.p

#Problem 4
# Part 1
soup.a.next_sibling.next_sibling.string   #if you use print, you get Mo, not u'Mo'

# Part 2
soup.body.contents[5]
#or
soup.p.next_sibling.next_sibling.next_sibling.next_sibling

# Part 3
example_soup = BeautifulSoup(open('example.htm'),'html.parser')
example_soup.a.string
example_soup.p.next_sibling.next_sibling.a.string

#Problem 5
example_soup = BeautifulSoup(open('example.htm'),'html.parser')
example_soup.find(href=True)['href']
example_soup.a['href']

#Problem 6
SOUP = BeautifulSoup(open('SanDiegoWeather.htm'))

# Part 1
SOUP.find(class_='history-date')

# Part 2
SOUP.find(class_='previous-link').a
SOUP.find(class_='next-link').a
#or
SOUP.find(string=re.compile('Previous Day')).parent
SOUP.find(string=re.compile('Next Day')).parent

# Part 3
SOUP.find(text='Max Temperature').parent.parent.next_sibling.next_sibling.span.span
#or
SOUP.find(text='Max Temperature').parent.parent.parent.find(class_='wx-value')

#Problem 7
dates_soup = BeautifulSoup(open('Big Data dates.htm'))

dates_soup.find_all(href=re.compile('[01]/default.htm')) #this would give all websites that have a date in the directory path. Could accidentally include files from years outside the allowed range 2003-2014
#or
dates_soup.find_all(href=re.compile('((200[3-9])|(201[0-4])).*/default.htm')) #restricts the years to the correct range 2003-2014