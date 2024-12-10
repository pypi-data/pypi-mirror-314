from deep_translator import GoogleTranslator
def translator(txt,dest,src='auto'):
    if dest=='ch':dest = 'zh-CN'
    try:return GoogleTranslator(source=src, target=dest).translate(txt)
    except Exception as e:print(e)

