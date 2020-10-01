from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import dload

driver = webdriver.Chrome('./chromedriver')


wb = Workbook()
ws1 = wb.active
ws1.title = "articles"
ws1.append(["제목", "링크", "신문사", "썸네일"])

url = f"https://search.naver.com/search.naver?&where=news&query=추석"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

newsList = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li')
i = 1
for item in newsList:
    title = item.dl.a.text
    link = item.dl.a['href']
    comp = item.dl.dd.span.text.split(' ')[0].replace('언론사', '')
    thumbnail = item.div.img['src']
    dload.save(thumbnail, f'imgs_chu/{i}.jpg')
    i += 1
    ws1.append([title, link, comp, thumbnail])

wb.save(filename='articles.xlsx')
driver.quit()

me = "보내는 메일@gmail.com"
my_password = "비밀번호"

# 로그인하기
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

# 받는 사람 정보
you = "받는 이메일@gmail.com"


# 메일 기본 정보 설정
msg = MIMEMultipart('alternative')
msg['Subject'] = '기사 스크랩'
msg['From'] = me
msg['To'] = you

# 메일 내용 쓰기
content = "추석 관련 기사"
part2 = MIMEText(content, 'plain')
msg.attach(part2)

# 파일 첨부하기
part = MIMEBase('application', "octet-stream")
with open("articles.xlsx", 'rb') as file:
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment", filename="articles.xlsx")
    msg.attach(part)

# 메일 보내고 서버 끄기
s.sendmail(me, you, msg.as_string())
s.quit()
