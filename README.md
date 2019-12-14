# python_brainfuck_interpreter

https://github.com/white-silver/brainfuck_interpreter_by_python  
↑この方のコードをほぼほぼ使わせてもらって，PythonでBrainFuck言語用インタプリタを作ってみました  
もちろん少し改変，機能追加してます  
今のところできることは    
`・brainfuckファイル（.bf）をエンコードする`  
`・テキストファイルの内容をなんちゃってBrainFuck化する`  
の2点です

***

## 使い方
`python3 brainf**k.py [-b **.bs -t **.txt]`  
で使えます  
`-b` or `--brain` で指定した.bsファイルを変換してコマンドラインに出力します  
`-t` or `--txt` で指定した.txtファイルの内容をなんちゃってBrainFuck化して，output.txtファイルとして出力します
