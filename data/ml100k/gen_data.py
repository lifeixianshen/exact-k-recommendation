import random

data_raw_pos = {}
data_raw_neg = {}
file_in = 'u.data'

with open(file_in, 'r') as fin:
    first_line = True
    for line in fin:
        if first_line:
            first_line = False
            continue

        strs = line.strip().split('\t')
        user_id = int(strs[0])
        item_id = int(strs[1])
        label = float(strs[2])

        if label == 5.0:
            if user_id not in data_raw_pos:
                data_raw_pos[user_id] = []
            data_raw_pos[user_id].append(item_id)
        else:
            if user_id not in data_raw_neg:
                data_raw_neg[user_id] = []
            data_raw_neg[user_id].append(item_id)

print("pos user num: ", len(data_raw_pos))
print("neg user num: ", len(data_raw_neg))

with open('rerank_data', 'w') as file_out:
    for user_id, pos_list in data_raw_pos.items():
        if user_id not in data_raw_neg:
            continue

        neg_list = data_raw_neg[user_id]

        print(f'user: {str(user_id)}')
        print(f'pos_list_len: {len(pos_list)}, neg_list_len: {len(neg_list)}')

        if len(neg_list) < 19 or len(neg_list) < 3:
            continue

        for item_id in pos_list:
            dis_pos = []
            neg_sample = random.sample(neg_list, 3)
            dis_pos = [item_id]
            dis_pos.extend(neg_sample)
            gen_cand = set(dis_pos)
            while len(gen_cand) < 20:
                random.shuffle(neg_list)
                for item_id in neg_list:
                    if item_id in gen_cand:
                        continue
                    if random.random() < 0.5:
                        gen_cand.add(item_id)
                        break

            file_out.write(str(user_id) + '\t' + ','.join([str(x) for x in dis_pos]) + '\t' + ','.join([str(x) for x in gen_cand]) + '\n')
            file_out.flush()