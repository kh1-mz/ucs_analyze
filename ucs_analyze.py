import sys
from dataclasses import asdict
import json
import ucs_factory


UCS_JSON_FILE = 'ucs.json'


def main(pathname):
    ucs_list = ucs_factory.create_ucs_list(pathname)

    # アクター一覧集計
    actor_set = set()
    actor_ucss_map = {}
    for ucs in ucs_list:
        for actor in ucs.actors:
            actor_set.add(actor.name)
            if actor.name in actor_ucss_map:
                actor_ucss_map[actor.name].append(ucs)
            else:
                actor_ucss_map[actor.name] = [ucs]

    # アクター一覧
    actor_name_list = sorted(list(actor_set))
    for actor_name in actor_name_list:
        print(f'{actor_name} ... {len(actor_ucss_map.get(actor_name))}件')

    # JSONで保存
    ucs_dict_list = []
    for ucs in ucs_list:
        # dict変換
        ucs_dict_list.append(asdict(ucs))

    with open(UCS_JSON_FILE, 'w', encoding='utf-8') as f:
        # ファイルに書き込み
        json.dump(ucs_dict_list, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <filepath>')
        exit()

    main(sys.argv[1])
