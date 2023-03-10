from bs4 import BeautifulSoup
import requests
from flaskNews.alghoritms import luhn, textrank, all_in_one, lsa_summary, ortayol, giso, lex_rank
from flask import flash
import re


def sozcuData(url, haberClass, value):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    news = soup.find_all("div", attrs={"class": haberClass})
    myNews = []
    x = 0
    for new in news:
        x = x+1
        link = new.a.get("href")
        url = link
        head = new.find("img", attrs={"loading": "lazy"})
        header = head.get("alt")
        try:
            newPage = requests.get(link)
            soup = BeautifulSoup(newPage.content, "lxml")
            date = soup.find(
                "span", attrs={"class": "content-meta-date"}).text
            image = soup.find("div", attrs={"class": "img-holder"})
            imageUrl = image.img.get("src")
        except:
            imageUrl = head.get("src")
        content = getContent(link)

        if value == 1 or value == '1':
            sumContent = content
        elif value == '2':
            sumContent = luhn(content)
        elif value == '3':
            sumContent = lex_rank(content)
        elif value == '4':
            sumContent = textrank(content)
        elif value == '5':
            sumContent = lsa_summary(content)
        elif value == '6':
            sumContent = all_in_one(content)
        elif value == '7':
            sumContent = ortayol(content)
        elif value == '8':
            sumContent = giso(content)

        myNews.append({'header': header, 'imageUrl': imageUrl,
                      'date': date, 'url': url, 'content': sumContent})
        if x == 1:
            break
    return myNews


def getContent(url):

    url1 = requests.get(url)

    soup = BeautifulSoup(url1.content, "lxml")

    a = ""

    for p in soup.select('article>p'):
        a = a+p.getText()
    if (a != ""):
        return a

    if a == "":
        for i in soup.select('p:not(:has(*))'):
            a = a+i.getText()

        if (a != ""):
            a = a.strip("""Haberturk.com ekibi olarak T??rkiye???de ve d??nyada ya??anan ve haber de??eri ta????yan her t??rl?? geli??meyi sizlere en h??zl??, en objektif ve en doyurucu ??ekilde ula??t??rmak i??in ??al??????yoruz. Yo??un g??ndem i??erisinde sundu??umuz haberlerimizle ve olaylarla ilgili ele??tiri, g??r????, yorumlar??n??z bizler i??in ??ok ??nemli. Fakat kar????l??kl?? sayg?? ve yasalara uygunluk ??er??evesinde olu??turdu??umuz yorum platformlar??nda daha sa??l??kl?? bir tart????ma ortam??n?? temin etmek amac??yla ortaya koydu??umuz baz?? yorum ve moderasyon kurallar??m??za dikkatinizi ??ekmek istiyoruz.
            Sayfam??zda T??rkiye Cumhuriyeti kanunlar??na ve evrensel insan haklar??na ayk??r?? yorumlar onaylanmaz ve silinir. Okurlar??m??z taraf??ndan yap??lan yorumlar??n, (yorum yapan di??er okurlar??m??za y??nelik yorumlar da dahil olmak ??zere) ki??ilere, ??lkelere, topluluklara, sosyal s??n??flara ??rk, cinsiyet, din, dil ba??ta olmak ??zere ayr??mc??l??k unsurlar?? ta????mas?? durumunda yorum edit??rlerimiz yorumlar?? onaylamayacakt??r ve yorumlar silinecektir. Onaylanmayacak ve silinecek yorumlar kategorisinde a??a????lama, nefret s??ylemi, k??f??r, hakaret, kad??n ve ??ocuk istismar??, hayvanlara y??nelik ??iddet s??ylemi i??eren yorumlar da yer almaktad??r. Su??u ve su??luyu ??vmek, T??rkiye Cumhuriyeti yasalar??na g??re su??tur. Bu nedenle bu tarz okur yorumlar?? da do??al olarak Haberturk.com yorum sayfalar??nda yer almayacakt??r.
            Ayr??ca Haberturk.com yorum sayfalar??nda T??rkiye Cumhuriyeti mahkemelerinde do??rulu??u ispat edilemeyecek iddia, itham ve karalama i??eren, halk??n tamam??n?? veya bir b??l??m??n?? kin ve d????manl????a tahrik eden, provokatif yorumlar da yap??lamaz.
            Yorumlarda markalar??n ticari itibar??n?? zedeleyici, karalay??c?? ve herhangi bir ??ekilde ticari zarara yol a??abilecek yorumlar onaylanmayacak ve silinecektir. Ayn?? ??ekilde bir markaya y??nelik promosyon veya reklam ama??l?? yorumlar da onaylanmayacak ve silinecek yorumlar kategorisindedir. Ba??ka hi??bir siteden al??nan linkler Haberturk.com yorum sayfalar??nda payla????lamaz.
            Haberturk.com yorum sayfalar??nda payla????lan t??m yorumlar??n yasal sorumlulu??u yorumu yapan okura aittir ve Haberturk.com bunlardan sorumlu tutulamaz.
            Bizlerle ve di??er okurlar??m??zla yorum kurallar??na uygun yorumlar??n??z??, g??r????lerinizi yasalar, sayg??, nezaket, birlikte ya??ama kurallar?? ve insan haklar??na uygun ??ekilde payla??t??????n??z i??in te??ekk??r ederiz.
            ??ifrenizi s??f??rlamak i??in oturum a??arken kulland??????n??z e-posta adresinizi giriniz""")
            return a
        if a == "":
            for j in soup.select("p"):
                a = a+j.getText()
                return a


def search(myNews, text):
    news = []
    if text == bool:
        return myNews
    else:
        for new in myNews:
            text2 = new["header"]

            result = text2.find(text)
            if result == -1:
                flash("Bu aramaya ait haber bulunamad??", "danger")
            else:
                news.append(new)
    return news
