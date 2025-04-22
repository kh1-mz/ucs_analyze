"""ユースケースシナリオファクトリークラス
"""
from use_case_scenario import Actor, UseCaseScenario, Condition
import openpyxl


def _get_string(cell):
    """セルから文字列を取り出す
    """
    val = cell.value
    if val is None:
        val = ''
    return val


def _create_actors(line):
    """文字列からアクターを生成
    """
    actors = []
    for prim in line.split('、'):
        for prim2 in prim.split('\n'):
            actors.append(Actor(prim2))
    return actors


def _set_header(ws, ucs):
    """ヘッダー情報をセット
    """
    is_pre_cond = False
    is_post_cond = False
    for row in ws.iter_rows():
        val = _get_string(row[2])
        match _get_string(row[0]):
            case 'シナリオID':
                ucs.scenario_id = val
            case '関連要求ID':
                ucs.related_request_id = val
            case '概要、場面':
                ucs.abstract = val
            case 'アクター':
                ucs.actors = _create_actors(val)
            case 'ステークホルダ要求':
                ucs.stakeholder_requirement = val
            case '関連要求（制約）':
                ucs.related_requirement = val
            case '事前条件':
                is_pre_cond = True
                is_post_cond = False
            case '事後条件':
                is_pre_cond = False
                is_post_cond = True
            case 'フロー':
                break

        if is_pre_cond and val:
            # 事前条件処理
            cond = Condition(_get_string(row[1]), val)
            ucs.pre_conditions.append(cond)
        elif is_post_cond and val:
            # 事後条件処理
            cond = Condition(_get_string(row[1]), val)
            ucs.post_conditions.append(cond)


def create(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.worksheets[0]
    ucs = UseCaseScenario()
    ucs.excel_path = excel_file

    _set_header(ws, ucs)

    return ucs
