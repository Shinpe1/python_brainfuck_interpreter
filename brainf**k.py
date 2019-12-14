# -*- coding: utf-8 -*-
import sys
import argparse
import os

"""
BrainFuck言語のインタプリタ
BrainFuck言語は+や-，>, <など8種類のコマンドだけで記述するチューリング完全の言語
指定したサイズのメモリ配列を用意して，用意した配列の各インデックスにasciiコードを格納
"""

# >: メモリポインタをインクリメント.
# <: メモリポインタをデクリメント.
# +: 配列要素をインクリメント.
# -: 配列要素をデクリメント
# .: 配列要素を出力．print()．
# ,: 1バイトの入力を受け付けて，配列の要素として格納.
# [: 現在のポインタの指す要素が0なら次の]までスキップ．用はwhile
# ]: 現在のポインタが0を指すなら，次の文字を処理する．0以外なら直前の[に戻る


class BrainFuck:
	def __init__(self, memory_size=30000):
		self.memory_size = memory_size

	def decode(self, code):
		"""
		ファイル（.bf）を読み込んで，CLIに出力する
		"""
		pointer = 0  # メモリ配列用ポインタ
		head = 0  # code読み込み用ポインタ
		memory = [0 for i in range(self.memory_size)]  # memory_size長の0配列を作成．ここにasciiコードの文字を格納していく
		code_length = len(code)

		while head < code_length:
			if code[head] == '+':
				memory[pointer] += 1
			elif code[head] == '-':
				memory[pointer] -= 1

			elif code[head] == '[':
				if memory[pointer] == 0:
					count = 1
					while count != 0:
						head += 1
						if head >= code_length:
							print("']' is missing")
							sys.exit(1)  # プログラム終了
						if code[head] == '[':
							count += 1
						elif code[head] == ']':
							count -= 1

			elif code[head] == ']':
				if memory[pointer] != 0:
					count = 1
					while count != 0:
						head -= 1
						if head < 0:
							print("'[' is missing")
						if code[head] == ']':
							count += 1
						elif code[head] == '[':
							count -= 1

			elif code[head] == '.':
				print(chr(memory[pointer]), end = "")  # 1文字ずつ要素を出力

			elif code[head] == ',':
				memory[pointer] = ord(sys.stdin.buffer.read(1))  # 標準入力で1バイト受け付ける．受け付けた文字をasciiコードに変換

			elif code[head] == '>':
				pointer += 1
				if pointer > self.memory_size:
					print("memory over flow")
					sys.exit(1)

			elif code[head] == '<':
				if pointer == 0:
					print("can't decrement anymore")
				pointer -= 1

			else:
				pass  # 他の文字は全てコメントとして無視する

			head += 1

		return memory


	def encode(self, string):
		"""
		テキストファイル（.txt）を読み込んで(擬似)BrainFuck言語にエンコードする
		使用するのは +, -, >, <, ], [ だけ
		ascii文字列にのみ対応（unicodeとかまで含めると変換に時間がかかりそうなので）
		"""
		string_length = len(string)
		memory = []
		prev = 0
		curr = prev + 1
		pointer = 0

		while curr < string_length:
			t = ord(string[prev]) if ord(string[prev]) <= 127 else None
			if not t: 
				print('non ascii character found')
				continue  # ascii文字列以外は飛ばす

			if ord(string[curr]) == t:  # 同じ文字列が続く際はループ（ [...] ）で記述
				nex = ord(string[curr])
				count = 1
				while ord(string[curr]) == t:
					count += 1
					curr += 1

				for i in range(count):  # 同じ文字が続いた分だけ+を追加（ループ回数の制御）
					memory.append('+')

				memory.append('[')  # ループ開始
				memory.append('>')  # メモリポインタをずらす

				for i in range(t):  # 文字コードを格納
					memory.append('+')

				memory.append('<')  # ループ制御要素にポインタを戻す
				memory.append('-')  # ループ制御要素をデクリメント
				memory.append(']')  # ループ終了

			else:
				for i in range(t):
					memory.append('+')  # 文字コード分だけ+を追加

			prev  = curr
			curr = prev + 1
			memory.append('>')

		memory.pop()  # 最後の余分な>を除外
		return memory



if __name__ == '__main__':
	bf = BrainFuck(memory_size=30000)

	parser = argparse.ArgumentParser()
	parser.add_argument("-b", "--brain", help="bs file you use here", type=str)
	parser.add_argument("-t","--txt", help="txt file you'd like to f**k here", type=str)
	args = parser.parse_args()

	bf_path = args.brain
	if bf_path:
		with open(bf_path) as f:
			code = f.read()
			code = list(code)
		bf.decode(code)

	txt_path = args.txt
	output_file = 'output.txt'  # .bsでも可

	if txt_path:
		with open(txt_path, mode='r') as f:
			strings = f.readlines()

		for string in strings:
			s = bf.encode(string)
			s.append('\n')
			with open(output_file, mode='a') as f:
				f.writelines(s)
