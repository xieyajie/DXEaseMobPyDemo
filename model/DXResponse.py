#coding = 'utf-8'

__author__ = 'xieyajie'

class DXResponse(object):

    def __init__(self, aCode = 0, aDescription = '', aData = None):
        self.code = aCode
        self.description = aDescription
        self.data = aData