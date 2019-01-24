# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
from xml.dom import minidom
import nltk

def zh_segmentation():
    cutLineFlag = ["？", "！", "。", '……', '\n']
    sentenceList = []
    with open(sys.argv[2], "r", encoding="utf-8") as fileZh:
        for line in fileZh:
            words = line
            oneSentence = ""

            for word in words:              #add content to sentencelist
                if word not in cutLineFlag:
                    oneSentence = oneSentence + word
                else:
                    oneSentence = oneSentence + word
                    if oneSentence.__len__() > 4:
                        sentenceList.append(oneSentence.strip() + "\r")
                    oneSentence = ""
    fileZh.close()

    sentences = pretreatment(sentenceList)
    fileseg = './corpus/segmentation/' + sys.argv[2].strip('.txt').strip('/corpus') + '_seg.txt'
    with open(fileseg, "w", encoding="utf-8") as resultFile:
        print(sentenceList.__len__())
        print(sentenceList)
        resultFile.write(sentences)
    resultFile.close()

def en_segmentation():
    with open(sys.argv[1], 'r', encoding='utf-8') as fileEn:
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        paragraphs = fileEn.readlines()
        sentenceList = []
        for paragraph in paragraphs:
            for sentence in sent_tokenizer.tokenize(paragraph):
                sentenceList.append(sentence + '\r')
    fileEn.close()

    sentences = pretreatment(sentenceList)
    fileseg = './corpus/segmentation/' + sys.argv[1].strip('.txt').strip('/corpus') + '_seg.txt'
    with open(fileseg, "w", encoding='utf-8') as fileResult:
        fileResult.write(sentences)
    fileResult.close()

def pretreatment(sentenceList):
    sentences = ''
    for sentence in sentenceList[0:-1:1]:
        sentences += sentence
    return sentences + sentenceList[-1].strip()

def sentenceAlign():
    with open(sys.argv[1], "r", encoding='utf-8') as al_file:
        no_aligns = al_file.readlines()

    with open(sys.argv[2], "r", encoding='utf-8') as en_file:
        en_lines = en_file.readlines()

    with open(sys.argv[3], "r", encoding='utf-8') as zh_file:
        zh_lines = zh_file.readlines()

        sentencePairs = []
        for no_align in no_aligns:
            no_sentences = no_align.rstrip().lstrip(' ').replace(' ', '').split('<=>')
            no_sentence = []
            sentencePair = []

            for no in no_sentences:
                if ',' in no:
                    no_sentence = no.split(',')
                else:
                    no_sentence.append(no)

            if no_sentence[-1] != 'omitted' and no_sentence[0] != 'omitted':
                if len(no_sentence) == 2:
                    sentencePair.append(en_lines[int(no_sentence[0])-1].strip())
                    sentencePair.append(zh_lines[int(no_sentence[1])-1].strip())
                    sentencePairs.append(sentencePair)

                else:
                    sentencePair.append(en_lines[int(no_sentence[-2])-1].strip())
                    sentencePair.append(zh_lines[int(no_sentence[-1])-1].strip())
                    sentencePairs.append(sentencePair)

        generateTmx(sentencePairs)

def generateTmx(sentencePairs):
    dom = minidom.Document()
    tmx_node = dom.createElement('tmx')
    tmx_node.setAttribute('version', '1.4')
    dom.appendChild(tmx_node)

    header_node = dom.createElement('header')
    header_node.setAttribute('creationtool', 'self_create')
    header_node.setAttribute('adminlang', 'EN')
    header_node.setAttribute('srclang', 'EN')
    tmx_node.appendChild(header_node)

    body_node = dom.createElement('body')
    print(len(sentencePairs))
    for sentencePair in sentencePairs:

        tu_node = dom.createElement('tu')
        tu_node.setAttribute('creationdate', 'self_create')
        tu_node.setAttribute('creationid', 'self')
        tu_node.setAttribute('srclang', 'EN')
        prop_node = dom.createElement('prop')
        prop_node.setAttribute('tpye', 'Txt::Note')
        prop_value = dom.createTextNode(sys.argv[1].strip('.txt'))
        prop_node.appendChild(prop_value)
        tu_node.appendChild(prop_node)
        body_node.appendChild(tu_node)

        tuv_en_node = dom.createElement('tuv')
        tuv_en_node.setAttribute('xml:lang', 'EN')
        tuv_en_node.setAttribute('xml:lang', 'ZH')
        seg_en_node = dom.createElement('seg')
        seg_en_value = dom.createTextNode(sentencePair[0])
        seg_en_node.appendChild(seg_en_value)
        tuv_en_node.appendChild(seg_en_node)

        tuv_zh_node = dom.createElement('tuv')
        tuv_zh_node.setAttribute('xml:lang', 'EN')
        tuv_zh_node.setAttribute('xml:lang', 'ZH')
        seg_zh_node = dom.createElement('seg')
        seg_zh_value = dom.createTextNode(sentencePair[1])
        seg_zh_node.appendChild(seg_zh_value)
        tuv_zh_node.appendChild(seg_zh_node)

        body_node.appendChild(tuv_en_node)
        body_node.appendChild(tuv_zh_node)

    tmx_node.appendChild(body_node)

    tmx_file = './tmx/' + sys.argv[1].strip('.txt') + '.tmx'

    try:
        with open(tmx_file, 'w', encoding='utf-8') as f_tmx:
            dom.writexml(f_tmx, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        f_tmx.close()
    except Exception as err:
        print('error information：{0}'.format(err))

if __name__ == '__main__':
    en_segmentation()
    zh_segmentation()
    #sentenceAlign()