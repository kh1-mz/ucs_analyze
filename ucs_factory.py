"""ユースケースシナリオファクトリークラス
"""
from use_case_scenario import Actor, UseCaseScenario
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
                pass
            case '事後条件':
                pass
            case 'フロー':
                break


def create(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.worksheets[0]
    ucs = UseCaseScenario()

    _set_header(ws, ucs)

    return ucs
