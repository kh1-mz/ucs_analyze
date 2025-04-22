"""ユースケースシナリオクラス
"""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Actor:
    name: str = ''


@dataclass
class UseCaseScenario:
    excel_path: Path = None          # 入力となったExcelファイルのパス
    scenario_id: str = ''            # シナリオID
    related_request_id: str = ''     # 関連要求ID
    abstract: str = ''               # 概要、場面
    actors: list = field(default_factory=list)  # アクター
    stakeholder_requirement: str = ''  # ステークホルダー要求
    related_requirement: str = ''      # 関連要件（制約）

    def _get_actor_names(self):
        pass

    def __str__(self):
        msg = f'''UseCaseScenario
シナリオID： {self.scenario_id}
関連要求ID： {self.related_request_id}
概要、場面： {self.abstract}
アクター  ：
'''

        for actor in self.actors:
            msg += f'  {actor.name}\n'

        msg += '''ステークホルダー要求： {self.stakeholder_requirement}
関連要件（制約）    ： {self.related_requirement}
'''
        return msg
