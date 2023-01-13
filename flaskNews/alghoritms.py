import spacy
import nltk
import pytextrank
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from nltk.tokenize import sent_tokenize

nlp = spacy.load('en_core_web_md')
nlp.add_pipe("textrank")

#Bütün özetleme algoritmaları bu sayfadadır.

def textrank(text):

    sentences = sent_tokenize(text)
    number = len(sentences)
    result = ""
    doc = nlp(text)
    if number > 20:
        for sent in doc._.textrank.summary(limit_phrases=40, limit_sentences=5):
            result += str(sent)
    elif number > 40:
        for sent in doc._.textrank.summary(limit_phrases=40, limit_sentences=8):
            result += str(sent)
    elif number > 60:
        for sent in doc._.textrank.summary(limit_phrases=40, limit_sentences=11):
            result += str(sent)
    else:
        for sent in doc._.textrank.summary(limit_phrases=40, limit_sentences=4):
            result += str(sent)
    return result


def luhn(metin, cumle_sayisi=3):

    ozet_luhn = LuhnSummarizer()
    parser = PlaintextParser.from_string(metin, Tokenizer("turkish"))
    b = str(metin).split(".")
    ozet = ozet_luhn(parser.document, cumle_sayisi)
    a = ""
    for cumle in ozet:
        a = a+str(cumle)
    return a


def all_in_one(metin):
    splitted_sentences = str(metin).split(".")
    a = ""
    for i in splitted_sentences:
        a = a+i

    if len(a) >= 4 and len(a) < 6:
        return lex_rank(lsa_summary(luhn(str(a), len(a)-1), len(a)-2), len(a)-3) + "."
    if len(a) >= 6:
        return textrank(lex_rank(lsa_summary(luhn(str(a), len(a)-1), len(a)-2), len(a)-3))+"."
    else:
        return lex_rank(metin)+"."


def lsa_summary(metin, cumle_sayisi=3):
    # Summarize using sumy LSA
    ozet_lsa = LsaSummarizer()
    parser = PlaintextParser.from_string(metin, Tokenizer("turkish"))
    ozet = ozet_lsa(parser.document, cumle_sayisi)
    lsa_summary = ""
    for sentence in ozet:
        lsa_summary += str(sentence)
    return lsa_summary


def ortayol(metin):

    luhnSet = set(str(luhn(metin)).split("."))
    lsaSet = set(str(lsa_summary(metin)).split("."))
    lexSet = set(str(lex_rank(metin)).split("."))
    textSet = set(str(textrank(metin)).split("."))

    same_sentences = luhnSet.intersection(
        lsaSet).intersection(lexSet).intersection(textSet)
    if str(same_sentences) == '{"}' or str(same_sentences) == "set()":
        return "Bu metin seçilen algoritma için uygun değil..."
    clipped_str = str(same_sentences).replace("{,", "").replace("{'", "").replace("}", "").replace(
        "{", "").strip("'").strip("',").replace("',", ".").replace("'", "").strip('"')
    if clipped_str == "" or len(clipped_str) < 3:
        return "Bu metin seçilen algoritma için uygun değil..."
    else:
        return clipped_str + "."


def giso(metin):
    splitted_sentences = str(metin).split(".")
    if len(splitted_sentences) >= 5 and len(splitted_sentences) <= 7:
        return str(splitted_sentences[0:2] + splitted_sentences[-1:-3]).replace("[,", "").replace("['", "").replace("]", "").replace("[", "").strip("'").strip("',").replace("',", ".").replace("'", "").strip('"')+"."
    if len(splitted_sentences) >= 8 and len(splitted_sentences) <= 12:
        return str(splitted_sentences[0:3] + splitted_sentences[-1:-4]).replace("[,", "").replace("['", "").replace("]", "").replace("[", "").strip("'").strip("',").replace("',", ".").replace("'", "").strip('"')+"."
    if len(splitted_sentences) >= 13:
        return str(splitted_sentences[0:4] + splitted_sentences[-1:-5]).replace("[,", "").replace("['", "").replace("]", "").replace("[", "").strip("'").strip("',").replace("',", ".").replace("'", "").strip('"')+"."
    else:
        return metin


def lex_rank(metin, cumle_sayisi=3):
    ozet_lex = LexRankSummarizer()
    parser = PlaintextParser.from_string(metin, Tokenizer("turkish"))
    ozet = ozet_lex(parser.document, cumle_sayisi)
    a = ""
    for cumle in ozet:
        a = a+str(cumle)
    return a
