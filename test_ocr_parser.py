import re

def parse_parking_text(raw):
    """Current parser logic (mirrored from index.html _parseParkingText)"""
    t = raw.upper()
    # Pre-correct common OCR misreads
    t = re.sub(r'\b8\s{0,2}([1-9])\b', r'B\1', t)  # 82→B2 (8 looks like B)
    t = re.sub(r'\bI([1-9])\b', r'1\1', t)           # I2→12
    t = re.sub(r'\s+', ' ', t)
    floor = None
    zone = None

    mb = re.search(r'\bB\s{0,2}([1-9])', t)
    if mb:
        floor = f'B{mb.group(1)}'
    if not floor:
        mf = re.search(r'\b([1-8])\s{0,2}F\b', t)
        if mf:
            floor = f'{mf.group(1)}F'
    if not floor and 'ROOF' in t:
        floor = '옥상'

    used_letter = floor[0] if floor else None
    mz = re.search(r'\b([A-Z])\s*-\s*(\d{1,3})\b', t)
    if mz and mz.group(1) != used_letter:
        zone = f'{mz.group(1)}-{mz.group(2)}'

    return floor, zone


# (input, expected_floor, expected_zone, description)
TESTS = [
    # Normal cases
    ('B2',                   'B2',   None,   '단순 B2'),
    ('B 2',                  'B2',   None,   'OCR 공백 삽입 B 2'),
    ('B1 PARKING',           'B1',   None,   'B1 + 뒷글자'),
    ('PARKING B3',           'B3',   None,   'B3 앞글자'),
    ('2F',                   '2F',   None,   '지상 2F'),
    ('3 F',                  '3F',   None,   '공백 3 F'),
    ('LEVEL 2F',             '2F',   None,   'LEVEL 접두'),
    ('B2 A-15',              'B2',   'A-15', '층+구역 B2 A-15'),
    ('B3 C-27',              'B3',   'C-27', 'C구역'),
    ('1F A-3',               '1F',   'A-3',  '지상 1F + 구역'),
    ('ROOF',                 '옥상', None,   '옥상'),
    ('B4',                   'B4',   None,   'B4'),
    ('B2F',                  'B2',   None,   'B2F 혼합 표기'),
    ('SUBLEVEL B2',          'B2',   None,   'SUBLEVEL 접두'),
    ('P2 B2',                'B2',   None,   'P2 라벨 포함'),
    ('- B2 -',               'B2',   None,   '대시 둘러싸인 B2'),
    ('FLOOR B2',             'B2',   None,   'FLOOR 접두'),
    ('A-15 B2',              'B2',   'A-15', '구역이 앞에 올 때'),
    # OCR misread correction cases (8→B, now fixed)
    ('82',                   'B2',   None,   'B2→82 OCR 오인식 보정'),
    ('83 A-5',               'B3',   'A-5',  '83+구역 보정'),
    # OCR misread / guard cases
    ('BRAKE 2',              None,   None,   'BRAKE단어 오매칭 방어'),
    ('28F',                  None,   None,   '28F→8F 잘못 추출 방어'),
    ('F2',                   None,   None,   'F2 역순 (층수 아님)'),
    # Boundary
    ('',                     None,   None,   '빈 문자열'),
    ('ABCDEF',               None,   None,   '의미없는 텍스트'),
    ('B0',                   None,   None,   'B0 없는 층'),
    ('B9',                   'B9',   None,   'B9 최대값'),
    ('9F',                   None,   None,   '9F 범위 밖'),
    ('B2 B3',                'B2',   None,   '두 층수 - 첫번째 우선'),
    ('B 2F',                 'B2',   None,   'B 2F 혼합'),
]

def run():
    passed = 0
    failed = 0
    bugs = []

    for inp, exp_floor, exp_zone, desc in TESTS:
        floor, zone = parse_parking_text(inp)
        ok = floor == exp_floor and zone == exp_zone
        mark = 'PASS' if ok else 'FAIL'
        if ok:
            passed += 1
        else:
            failed += 1
            bugs.append((desc, inp, exp_floor, exp_zone, floor, zone))

    print(f'=== _parseParkingText 테스트 ({passed+failed}건) ===\n')
    for inp, exp_floor, exp_zone, desc in TESTS:
        floor, zone = parse_parking_text(inp)
        ok = floor == exp_floor and zone == exp_zone
        if ok:
            print(f'  OK  {desc}')
        else:
            print(f'  !!  {desc}')
            print(f'      입력: "{inp}"')
            print(f'      기대: floor={exp_floor!r}  zone={exp_zone!r}')
            print(f'      실제: floor={floor!r}  zone={zone!r}')

    print(f'\n결과: {passed}/{passed+failed} 통과,  {failed}건 실패')

    if bugs:
        print('\n=== 수정 필요 항목 ===')
        for b in bugs:
            print(f'  - {b[0]}  |  입력: "{b[1]}"  →  실제: floor={b[4]!r} zone={b[5]!r}')

if __name__ == '__main__':
    run()
