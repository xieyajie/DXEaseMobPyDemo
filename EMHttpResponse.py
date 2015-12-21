#coding = 'utf-8'

__author__ = 'xieyajie'

class EMHttpResponse:
    code = 0

    def __init__(self, aCode, aData):
        self.code = aCode
        self.data = aData