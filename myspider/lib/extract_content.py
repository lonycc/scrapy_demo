#!/usr/bin/env python3
# coding=utf-8

import re
import socket

reBODY = r'<body.*?>([\s\S]*?)<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG  = r'<[\s\S]*?>|[ \t\r\f\v]'
reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')

class Extractor():
    """根据文本密度提取正文区"""
    def __init__(self, blockSize=3, image=False, rawPage=''):
        self.blockSize = blockSize
        self.saveImage = image
        self.rawPage = rawPage
        self.ctexts = []
        self.cblocks = []

    def processTags(self):
        self.body = re.sub(reCOMM, '', self.body)
        self.body = re.sub(reTRIM.format('script'), '', re.sub(reTRIM.format('style'), '', self.body))
        self.body = re.sub(reTRIM.format('SCRIPT'), '', re.sub(reTRIM.format('STYLE'), '', self.body))
        self.body = re.sub(reTAG, '', self.body)

    def processBlocks(self):
        self.ctexts   = self.body.split('\n')
        self.textLens = [len(text) for text in self.ctexts]
        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))
        maxTextLen = max(self.cblocks)
        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1
        return ''.join(self.ctexts[self.start:self.end])

    def processImages(self):
        self.body = reIMG.sub(r'{{\1}}', self.body)

    def getContext(self):
        body = re.findall(reBODY, self.rawPage)
        self.body = ''
        if body:
            self.body = body[0]
        if self.saveImage:
            self.processImages()
        self.processTags()
        return self.processBlocks()
