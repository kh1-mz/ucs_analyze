"""UCシナリオのアクターごとのアクションを表示する
"""
import sys
from ucs_factory import create_ucs_list
import morph


def get_actions_from_actor(tk, ucs, actor_name):
    """actor_nameが主語のアクションを取り出す
    """

    actions = []
    for action in ucs.get_actions():
        print(action.detail)
        """
        if morph.is_subject(tk, action.detail, actor_name):
            actions.append(action)
        """

    return actions


def main(pathname):
    # UCシナリオリストの作成
    ucs_list = create_ucs_list(pathname)

    # アクター名を取り出す
    actor_names = set()
    for ucs in ucs_list:
        for actor_name in [actor.name for actor in ucs.actors]:
            actor_names.add(actor_name)

    # カスタム辞書に登録
    morph.add_morph_dict(actor_names)

    # 形態素解析おアナライザーを作成
    analyzer = morph.get_analyzer()

    # アクターごとのアクションを表示
    for ucs in ucs_list:
        print(ucs.scenario_id)
        for actor in ucs.actors:
            print(f'ACTOR: {actor.name}')
            for action in ucs.get_actions():
                phrase = action.detail
                if morph.is_subject(analyzer, phrase, actor.name):
                    print(morph.remove_subject(analyzer, phrase))
        print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <filepath>')
        exit()

    main(sys.argv[1])
