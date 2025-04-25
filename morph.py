"""形態素解析ルーチン
"""
from pathlib import Path
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer


DICT_FILE = '_noun_dict.csv'


def add_morph_dict(words):
    """単語リストを形態素解析用の辞書に登録
    words : 単語リスト
    """
    noun_map = {}

    # すでに登録している辞書データを読み込み
    dict_path = Path(DICT_FILE)
    if dict_path.exists():
        with open(dict_path, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                w = line.split(',')[0]
                noun_map[w] = line

    # 辞書データに単語リストを追加
    for word in words:
        noun_map[word] = f'{word},カスタム名詞,{word}'

    # 辞書データをファイル出力
    with open(dict_path, 'w') as f:
        for line in noun_map.values():
            f.write(line+'\n')


def get_analyzer():
    """Analyzerの取得
    """
    dict_path = Path(DICT_FILE)
    tk = None
    if dict_path.exists():
        # 辞書ファイルがある場合
        tk = Tokenizer(udic=DICT_FILE, udic_enc='utf-8', udic_type='simpledic')
    else:
        # 辞書ファイルがない場合
        tk = Tokenizer()

    analyzer = Analyzer(tokenizer=tk)

    return analyzer


def is_noun(token):
    """tokenが名詞ならTrueを返す
    """
    return '名詞' in token.part_of_speech


def is_particle(token):
    """tokenが助詞ならTrueを返す
    """
    return '助詞' == token.part_of_speech.split(',')[0]


def print_token_info(analyzer, sentence):
    for token in analyzer.analyze(sentence):
        print(token)


def get_subject(analyzer, sentence, target):
    """主部の名詞を取り出す
    """
    sub_words = []
    for token in analyzer.analyze(sentence):
        if is_noun(token):
            sub_words.append(token.surface)
        elif is_particle(token) and token.surface == 'は':
            break

    return sub_words


def is_subject(analyzer, sentence, target):
    """sentenseでtargetが主語か判定
    """
    sub_words = get_subject(analyzer, sentence, target)
    return target in sub_words


def remove_subject(analyzer, sentence):
    """主語（主部）を削除する
    """
    gen = analyzer.analyze(sentence)
    for token in gen:
        if is_particle(token) and token.surface == 'は':
            break

    res = ''
    token = next(gen)
    if token.surface != '、':
        res += token.surface

    for token in gen:
        res += token.surface

    return res
