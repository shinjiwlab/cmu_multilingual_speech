from pathlib import Path

lang_lst = """abk  asm  cat  chv  cym  ell  est  fin  gle  hin  ind  jpn  kaz  lav  luo  nld  pol  rus  slv  swe  tgl  ukr  wen
amh  ben  ceb  cmn  deu  eng  eus  fra  gug  hun  ita  kab  kin  lit  mlt  ori  por  sah  spa  tam  tha  vie  yue
arb  bre  ces  cnh  div  epo  fas  fry  hat  ina  jav  kat  kir  lug  mon  pan  ron  sin  swa  tat  tur  vot  zul""".split()

if __name__ == '__main__':

    for lang_id in lang_lst:
        
        lang = Path('/home/xinjianl/Git/cmu_multilingual_speech/corpus') / lang_id
        lang.mkdir(exist_ok=True, parents=True)
        
        w = open(lang / 'README.md', 'w')
        w.write('# ' + lang_id + '\n')
        w.write('## ASR\n\n')
        w.write('## TTS\n\n')
        w.close()