"""アクター情報を表示o
"""
import sys
import ucs_factory


def main(pathname):
    ucs_list = ucs_factory.create_ucs_list(pathname)

    # アクター一覧集計
    actor_set = set()
    actor_ucss_map = {}  # アクター名:UCシナリオ
    for ucs in ucs_list:
        for actor in ucs.actors:
            actor_set.add(actor.name)
            if actor.name in actor_ucss_map:
                actor_ucss_map[actor.name].append(ucs)
            else:
                actor_ucss_map[actor.name] = [ucs]

    print('アクター一覧（使用しているUCシナリオ件数）')
    actor_name_list = sorted(list(actor_set))
    for actor_name in actor_name_list:
        print(f'  {actor_name} ... {len(actor_ucss_map.get(actor_name))}件')
    print()

    print('アクター一覧（使用しているUCシナリオ）')
    actor_name_list = sorted(list(actor_set))
    for actor_name in actor_name_list:
        print(f'  {actor_name}')
        for ucs in actor_ucss_map.get(actor_name):
            print(f'    [{ucs.scenario_id}] : {ucs.excel_path.name}')
    print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <filepath>')
        exit()

    main(sys.argv[1])
