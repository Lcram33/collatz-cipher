#comes from https://en.wikipedia.org/wiki/List_of_Unicode_characters

excluded = [
    0x1F16,
    0x1F17,
    0x1F1E,
    0x1F1F,
    0x1F46,
    0x1F47,
    0x1F4E,
    0x1F4F,
    0x1F58,
    0x1F5A,
    0x1F5C,
    0x1F5E,
    0x1F7E,
    0x1F7F,
    0x1FB5,
    0x1FC5,
    0x1FD4,
    0x1FD5,
    0x1FDC,
    0x1FF0,
    0x1FF1,
    0x1FF5,
    0x1FFF,
    0x0378,
    0x0379,
    0x0380,
    0x0381,     
    0x0382,
    0x0383,
    0x038B,
    0x038D,
    0x03A2,
    0x0530,
    0x0557,
    0x0558,
    0x058B,
    0x058C,
    0x0590,
    0x070E,
    0x070F,
    0x074B,
    0x074C,
    0x085C,
    0x085D,
    0x085F,
    0x082E,
    0x082F,
    0x083F,
    0x218C,
    0x218D,
    0x218E,
    0x218F,
] + [int("05C" + x,16) for x in "89ABCDEF"] + [int("05E" + x,16) for x in "BCDEF"] + [int("05F" + x,16) for x in "56789ABCDEF"]

boundaries = [
    (0x0020, 0x007E),
    (0x00A0, 0x00FF),
    (0x0100, 0x017F),
    (0x0180, 0x024F),
    (0x1E00, 0x1EFF),
    (0x0250, 0x02AF),
    (0x02B0, 0x02FF),
    (0x0300, 0x036F),
    (0x0370, 0x03FF),
    (0x0400, 0x04FF),
    (0x07B0, 0x07B1),
    (0x20A0, 0x20AF),
    (0x20B0, 0x20BF),
    (0x2440, 0x2445)
]

hex_range = list(str(x) for x in range(10)) + list("ABCDEF")

for x in hex_range:
    boundaries.append((int("1F" + x + "0",16), int("1F" + x + "F",16)))

for x in [y for y in hex_range if y not in ['1', '2']]:
    boundaries.append((int("05" + x + "0",16), int("05" + x + "F",16)))

for x in [y for y in hex_range if y not in ['D', '1']]:
    boundaries.append((int("06" + x + "0",16), int("06" + x + "F",16)))

for x in range(5):
    boundaries.append((int("07" + str(x) + "0",16), int("07" + str(x) + "F",16)))
    boundaries.append((int("08" + str(x) + "0",16), int("08" + str(x) + "F",16)))

for x in "89A":
    boundaries.append((int("07" + str(x) + "0",16), int("07" + str(x) + "F",16)))

#really long to do so... Skipped to end

for w in "123":
    for x in hex_range:
        boundaries.append((int("2" + w + x + "0",16), int("2" + w + x + "F",16)))



for bounds in boundaries:
    print(u''.join(chr(x) for x in range(bounds[0],bounds[1]+1) if x not in excluded))