"""ユースケースシナリオクラス
"""
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum, auto


@dataclass
class Actor:
    name: str = ''


@dataclass
class Condition:
    target: str = ''            # 対象
    detail: str = ''            # 内容

    def __str__(self):
        return f'{self.target}: {self.detail}'


@dataclass
class Action:
    step: str = ''              # ステップ（ExcelのフローID）
    detail: str = ''            # アクション内容（Excelのシナリオ）
    branch_ids: list = field(default_factory=list)  # 分岐先フローID
    branches: list = field(default_factory=list)  # 分岐フロー
    note: str = ''                                # 備考

    def __str__(self):
        msg = f'{self.step}: {self.detail}: {self.note}'
        if self.branches:
            msg += ': ' + str([flow.flow_id for flow in self.branches])
        return msg


class FlowType(Enum):
    NONE = auto()               # 未指定
    MAIN = auto()               # 基本フロー
    ALTERNATIVE = auto()        # 代替フロー
    EXCEPTION = auto()          # 例外フロー


@dataclass
class Flow:
    flow_id: str = ''
    flow_type: FlowType = FlowType.NONE
    actions: list = field(default_factory=list)  # アクション

    def __init__(self, flow_type=FlowType.MAIN, flow_id='MF'):
        """デフォルトで基本フロー
        """
        self.flow_type = flow_type
        self.flow_id = flow_id
        self.actions = []

    def __str__(self):
        msg = f'{self.flow_type}: {self.flow_id}\n'
        for action in self.actions:
            msg += f'  {str(action)}\n'

        return msg

    def add_action(self, step, detail, branch, note):
        """アクション（Excelのシナリオ）を追加
        """
        branches = []
        if branch:
            branches = branch.split('\n')
        self.actions.append(Action(step, detail, branches, [], note))

    def traverse_actions(self, flow_map):
        """アクションのブランチを登録する
        """
        for action in self.actions:
            for flow_id in action.branch_ids:
                flow = flow_map.get(flow_id)
                if flow:
                    action.branches.append(flow)
                else:
                    print(f'ERROR: {action.step}/{flow_id}: Unknown flow ID')


@dataclass
class UseCaseScenario:
    excel_path: Path = None          # 入力となったExcelファイルのパス
    scenario_id: str = ''            # シナリオID
    related_request_id: str = ''     # 関連要求ID
    abstract: str = ''               # 概要、場面
    actors: list = field(default_factory=list)  # アクター
    stakeholder_requirement: str = ''  # ステークホルダー要求
    related_requirement: str = ''      # 関連要件（制約）
    pre_conditions: list = field(default_factory=list)   # 事前条件
    post_conditions: list = field(default_factory=list)  # 事後条件

    main_flow: Flow = None                               # 基本フロー
    alternative_flows: list = field(default_factory=list)  # 代替フロー
    exception_flows: list = field(default_factory=list)  # 例外フロー

    _flow_map: dict = field(default_factory=dict)   # フローIDとフローの対応表

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
事前条件           ：
'''
        for cond in self.pre_conditions:
            msg += f'  {cond.target}:{cond.detail}\n'

        msg += '事後条件           ：\n'
        for cond in self.post_conditions:
            msg += f'  {cond.target}:{cond.detail}\n'

        msg += '基本フロー：\n'
        msg += str(self.main_flow)
        msg += '代替フロー：\n'
        for flow in self.alternative_flows:
            msg += str(flow)
        msg += '例外フロー：\n'
        for flow in self.exception_flows:
            msg += str(flow)

        return msg

    def add_flow(self, flow):
        """フローの追加
        """
        match flow.flow_type:
            case FlowType.MAIN:
                self.main_flow = flow
            case FlowType.ALTERNATIVE:
                self.alternative_flows.append(flow)
            case FlowType.EXCEPTION:
                self.exception_flows.append(flow)

        self._flow_map[flow.flow_id] = flow

    def traverse_flow(self):
        """フローに登録されたアクションのブランチを調べ、リンクする
        """
        if self.main_flow:
            self.main_flow.traverse_actions(self._flow_map)
        for flow in self.alternative_flows:
            flow.traverse_actions(self._flow_map)
        for flow in self.exception_flows:
            flow.traverse_actions(self._flow_map)
