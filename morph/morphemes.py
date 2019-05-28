class Morpheme:
    def __init__( self, base, inflected, pos, subPos, read ):
        """ Initialize morpheme class.

        Example morpheme infos for the expression "歩いて":

        :param str base: 歩く
        :param str inflected: 歩い  [mecab cuts off all endings, so there is not て]
        :param str pos: 動詞
        :param str subPos: 自立
        :param str read: アルイ

        """
        # values are created by "mecab" in the order of the parameters and then directly passed into this constructor
        # example of mecab output:    "歩く     歩い    動詞    自立      アルイ"
        # matches to:                 "base     infl    pos     subPos    read"
        self.pos    = pos # type of morpheme detemined by mecab tool. for example: u'動詞' or u'助動詞', u'形容詞'
        self.subPos = subPos
        self.read   = read
        self.base   = base
        self.inflected = inflected

class AnkiDeck(  ):
    def __init__( self, noteId, fieldName, fieldValue, guid, maturities ):
        self.noteId     = noteId
        self.fieldName  = fieldName # for example u'Expression'
        self.fieldValue = fieldValue # for example u'それだけじゃない'
        self.guid       = guid
        self.maturities = maturities # list of intergers, one for every card -> containg the intervals of every card for this note
        self.maturity   = max( maturities ) if maturities else 0