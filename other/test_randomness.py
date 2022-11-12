from secrets import token_hex


max_shift = 106
nbytes = 3000
text_size = 500


def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        n = 3 * n + 1 if n & 1 else n // 2
        sequence.append(n)
    
    return sequence

def modified_collatz_sequence(int_key, size):
    seq = collatz_sequence(int_key)
    output = [x % max_shift for x in seq if not x & 1]
    if len(output) < size:
        output = (size // len(output) + 1) * output
    return output[0:size]


keys = modified_collatz_sequence(int(token_hex(nbytes), 16), text_size)
nb_keys = len(keys)
keys_list = list(set(keys))

keys_rates = {}
for key in keys_list:
    key_count = len([x for x in keys if x == key])
    keys_rates[str(key)] = round(key_count / nb_keys, 3)

print("Occurrence rates :")
print(keys_rates)
print()

print("Delta compared to real randomness :")
keys_delta = dict([(k,v-1/max_shift) for k,v in keys_rates.items()])
print(keys_delta)