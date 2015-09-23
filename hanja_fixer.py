import json
from pprint import pprint
filename = 'hanja/hanja_8.json'
with open(filename) as outfile:
	data = json.load(outfile)

manual_fix = [
	{'id': 8, '字': '呂', '訓': '성씨;법칙', '音': '려(여)'},
 {'id': 13, '字': '謨', '訓': '꾀', '音': '모'},
 {'id': 15, '字': '裵', '訓': '성씨;치렁치렁할;고을 이름', '音': '배;비'},
 {'id': 20, '字': '錫', '訓': '주석;줄;다리', '音': '석;사;체'},
 {'id': 21, '字': '燮', '訓': '불꽃', '音': '섭'},
 {'id': 37, '字': '祚', '訓': '복', '音': '조'},
 {'id': 39, '字': '采', '訓': '풍채;캘', '音': '채'},
 {'id': 40, '字': '阪', '訓': '언덕', '音': '판'},
 {'id': 41, '字': '扁', '訓': '작을', '音': '편'},
 {'id': 42, '字': '杓', '訓': '북두 자루;구기', '音': '표;작'},
 {'id': 45, '字': '爀', '訓': '불빛', '音': '혁'},
 {'id': 48, '字': '薰', '訓': '향풀', '音': '훈'},
 {'id': 50, '字': '嬉', '訓': '아름다울', '音': '희'}
]

fixed = False
errors = []
for hanja in data:
	if hanja['訓'] == "ERROR":
		errors.append(hanja)
if(len(errors) > 0):
	pprint(errors)

if fixed:
	for hanja in data:
		if hanja['訓'] == "ERROR":
			for h_fix in manual_fix:
				if h_fix['字'] == hanja['字']:
					for val in h_fix:
						hanja[val] = h_fix[val]
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)