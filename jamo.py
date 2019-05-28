import math
hangul_dict = {
	'initial':{
	'ᄀ':0,		'ㄸ':4,		'ㅃ':8,		'ㅈ':12,		'ㅌ':16,
'ㄲ':1,		'ㄹ':5,		'ㅅ':9,		'ㅉ':13,		'ㅍ':17,
'ㄴ':2,		'ㅁ':6,		'ㅆ':10,		'ㅊ':14,		'ㅎ':18,
'ㄷ':3,		'ㅂ':7,		'ㅇ':11,		'ㅋ':15
},
	'medial':{'ㅏ':0,		'ㅖ':7,		'ㅝ':14,
'ㅐ':1,		'ㅗ':8,		'ㅞ':15,
'ㅑ':2,		'ㅘ':9,		'ㅟ':16,
'ㅒ':3,		'ㅙ':10,		'ㅠ':17,
'ㅓ':4,		'ㅚ':11,		'ㅡ':18,
'ㅔ':5,		'ㅛ':12,		'ㅢ':19,
'ㅕ':6,		'ㅜ':13,		'ㅣ':20,
},
	'final':{'':0,		'ㄷ':7,		'ㄿ':14,		'ㅇ':21,
'ㄱ':1,		'ㄹ':8,		'ㅀ':15,		'ㅈ':22,
'ㄲ':2,		'ㄺ':9,		'ㅁ':16,		'ㅊ':23,
'ㄳ':3,		'ㄻ':10,		'ㅂ':17,		'ㅋ':24,
'ㄴ':4,		'ㄼ':11,		'ㅄ':18,		'ㅌ':25,
'ㄵ':5,		'ㄽ':12,		'ㅅ':19,		'ㅍ':26,
'ㄶ':6,		'ㄾ':13,		'ㅆ':20,		'ㅎ':27,
}
}

def get_hangul(initial, medial, final):
	try:
		return initial * 588 + medial * 28 + final + 44032
	except TypeError:
		return hangul_dict['initial'][initial] * 588 + hangul_dict['medial'][medial] * 28 + hangul_dict['final'][final] + 44032


def get_jamo(hangul):
	value = ord(hangul)
	value = value - 44032
	initial = math.floor(value/588)
	value = value - initial*588
	medial = math.floor(value/28)
	value = value - medial*28
	final = value
	result = reverse_hangul_dict['initial'][initial],reverse_hangul_dict['medial'][medial],reverse_hangul_dict['final'][final]
	if result == 'ᄀ': result = 'ㄱ'
	return result

reverse_hangul_dict = {
	'initial': {},
	'medial': {},
	'final': {}
}
for k in reverse_hangul_dict:
	reverse_hangul_dict[k] = {v: k for k, v in hangul_dict[k].items()}

#### TESTING
# number = get_hangul('ㄸ','ㅏ','')
# hangul = '자'
# print(get_jamo(hangul))
# print(chr(number))
# print(get_jamo(hangul[0])[0])