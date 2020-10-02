from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.font_manager as fm

text = ""
with open("KakaoTalk.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[1:]:
        if ',"' in line:
            line = line.split(',"')[2].replace('ㅋ', "").replace('감사합니다', "").replace('저는', "")\
                .replace('근데', "").replace('그래서', "").replace('그냥', "").replace('사진', "").replace('이모티콘\n', "")\
                .replace('이모티콘', "").replace('ㅠ', "").replace('어떻게', "").replace('제가', "").replace('저기', "")\
                .replace('여기', "").replace('ㅎ', "").replace('저도', "").replace('저거', "").replace('그거', "")\
                .replace('거의', "").replace('이거', "").replace('안에', "").replace('혹시', "").replace('저렇게', "")
            text += line

print(text)
#
# wc = WordCloud(font_path='/System/Library/Fonts/AppleSDGothicNeo.ttc', background_color="white", width=600, height=400)
# wc.generate(text)
# wc.to_file("result.png")
#


mask = np.array(Image.open('cloud.png'))
wc = WordCloud(font_path='/System/Library/Fonts/AppleSDGothicNeo.ttc', background_color="white", mask=mask)
wc.generate(text)
wc.to_file("result_masked.png")

#
# # 이용 가능한 폰트 중 '고딕'만 선별
# for font in fm.fontManager.ttflist:
#     if 'Gothic' in font.name:
#         print(font.name, font.fname)