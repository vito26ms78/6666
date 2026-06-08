V1.5

新增:
1. Google Translator Cache
2. Overlay 中文文字顯示

下一步:
main.py 改為建立 items:

{
  'box': box,
  'text': text,
  'translated': translated
}

然後呼叫:

overlay.update_items(items)

