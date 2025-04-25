import sys
import ucs_factory


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
        # print(actor_name)
        print(f'{actor_name} ... {len(actor_ucss_map.get(actor_name))}件')
        # for ucs in actor_map.get(actor_name):
        #     print(f'    {ucs.scenario_id}')

    """
    # 条件一覧
    for ucs in ucs_list:
        print(f'UC: {ucs.scenario_id}')
        print('事前条件：')
        for cond in ucs.pre_conditions:
            print(cond)
        print('事後条件：')
        for cond in ucs.post_conditions:
            print(cond)
        print()
    """

    """
    # UCシナリオ詳細表示
    for ucs in ucs_list:
        print(ucs)
    """


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <filepath>')
        exit()

    main(sys.argv[1])
