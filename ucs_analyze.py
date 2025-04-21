import sys
from pathlib import Path
import ucs_factory


def main(pathname):
    p = Path(pathname)
    if p.is_file():
        print(p)
        ucs = ucs_factory.create(p)
        print(ucs)
    elif p.is_dir():
        ucs_dict = {}
        actor_map = {}
        for xlfile in p.glob('**/*.xlsx'):
            ucs = ucs_factory.create(xlfile)
            ucs_dict[ucs.scenario_id] = ucs
            for actor in ucs.actors:
                ucs_list = actor_map.get(actor.name)
                if ucs_list is None:
                    actor_map[actor.name] = [ucs]
                else:
                    ucs_list.append(ucs)
            print(xlfile)

        # アクター一覧
        actor_name_list = sorted(actor_map.keys())
        for actor_name in actor_name_list:
            # print(actor_name)
            print(f'{actor_name} ... {len(actor_map.get(actor_name))}件')
            """
            for ucs in actor_map.get(actor_name):
                print(f'    {ucs.scenario_id}')
            """

    else:
        print(f'ERROR: {str(p)}: No such file or directory')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <filepath>')
        exit()

    main(sys.argv[1])
