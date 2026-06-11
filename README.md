# ok-script

## Downloads

![downloads](./assets/downloads.svg)

---
* ok-script 鏄熀浜庡浘鍍忚瘑鍒妧鏈? 绾疨ython瀹炵幇鐨? 鏀寔Windows绐楀彛鍜屾ā鎷熷櫒鐨勮嚜鍔ㄥ寲娴嬭瘯妗嗘灦銆?* 妗嗘灦鍖呭惈UI, 鎴浘, 杈撳叆, 璁惧鎺у埗, OCR, 妯℃澘鍖归厤, 妗嗘Debug娴眰, 鍩轰簬Github Action鐨勬祴璇? 鎵撳寘, 鍗囩骇/闄嶇骇銆?* 鍩轰簬寮€鍙戜竴涓伐涓氱骇鐨勮嚜鍔ㄥ寲杞欢浠呴渶鍑犵櫨琛屼唬鐮併€?
## 浼樺娍

1. 绾疨ython瀹炵幇, 鍏嶈垂寮€婧? 渚濊禆搴撳潎涓哄紑婧愭柟妗?2. 鏀寔pip install浠讳綍绗笁鏂瑰簱, 鍙互鏂逛究鏁村悎yolo绛夋鏋?3. 涓€濂椾唬鐮佸嵆鍙敮鎸乄indows瀹夊崜妯℃嫙鍣?ADB杩炴帴鐨勮櫄鎷熸満, Windows瀹㈡埛绔父鎴?4. 鑷€傚簲鍒嗚鲸鐜?5. 浣跨敤coco绠＄悊鍥剧墖鍖归厤绱犳潗, 浠呴渶涓€涓垎杈ㄧ巼涓嬬殑鎴浘灏? 鏀寔涓嶅悓鍒嗚鲸鐜囪嚜閫傚簲
6. 鍙墦鍖呯绾?鍦ㄧ嚎瀹夎setup.exe, 鏀寔閫氳繃Pip/Git鍥藉唴闀滃儚鍦ㄧ嚎澧為噺鏇存柊. 鍦ㄧ嚎瀹夎鍖呬粎3M
7. 鏀寔Github Action涓€閿瀯寤?8. 鏀寔澶氳瑷€鍥介檯鍖?
## [浣跨敤鍩轰簬ok-script鐨勬寜閿簿鐏? 蹇€熷涔犲拰寮€濮媇(https://github.com/ok-oldking/ok-py)

**API鍒楄〃, 鑴氭湰褰曞埗**
![image_scripting](docs/ok_py/image_scripting.png)

**鏀寔澶氱鎴浘浠ュ強浜や簰鏂瑰紡**
![image_screenshot](docs/ok_py/image_capture.png)

**鏍囨敞绠＄悊 (Template Matching)**
![image_template](docs/ok_py/image_template.png)
![image_markup](docs/ok_py/image_markup.png)

### 浣跨敤 鎺ㄨ崘浣跨敤Python 3.12

* 鍦ㄤ綘鐨勯」鐩腑閫氳繃pip渚濊禆浣跨敤
```commandline
pip install ok-script
```

* 缂栬瘧鍥介檯鍖栨枃浠?```commandline
compile_i18n.cmd
```

* 杞欢鍚姩鏃惰嚜鍔ㄩ儴缃插墠绔〉闈㈠埌 Web锛堥粯璁ょ鍙?10086锛?```python
config = {
  "browser": {
    "frontend_path": "./dist",
    "port": 10086
  }
}
```

## 鏂囨。鍜岀ず渚嬩唬鐮?
* [娓告垙鑷姩鍖栧叆闂╙(docs/intro_to_automation/README.md)
  - [1銆佸熀鏈師鐞嗭細璁＄畻鏈哄浣曗€滅帺鈥濇父鎴廬(docs/intro_to_automation/README.md#涓€鍩烘湰鍘熺悊璁＄畻鏈哄浣曠帺娓告垙)
    - [鏍稿績寰幆锛氫笁姝ヨ蛋](docs/intro_to_automation/README.md#鏍稿績寰幆涓夋璧?
    - [鍥惧儚鍒嗘瀽锛氫粠鍍忕礌鍒板喅绛朷(docs/intro_to_automation/README.md#鍥惧儚鍒嗘瀽浠庡儚绱犲埌鍐崇瓥)
        - [浼犵粺鍥捐壊绠楁硶 (OpenCV 搴?](docs/intro_to_automation/README.md#1-浼犵粺鍥捐壊绠楁硶-opencv-搴?
        - [绁炵粡缃戠粶鎺ㄧ悊 (Inference)](docs/intro_to_automation/README.md#2-绁炵粡缃戠粶鎺ㄧ悊-inference)
    - [2銆佺紪绋嬭瑷€閫夋嫨](docs/intro_to_automation/README.md#浜岀紪绋嬭瑷€閫夋嫨)
        - [甯哥敤搴撴瑙圿(docs/intro_to_automation/README.md#甯哥敤搴撴瑙?
    - [3銆佸紑鍙戝伐鍏穄(docs/intro_to_automation/README.md#涓夊紑鍙戝伐鍏?
* [蹇€熷紑濮媇(docs/quick_start/README.md)
* [API鏂囨。](docs/api_doc/README.md)
  - [Box](docs/api_doc/README.md#box)
  - [BaseTask](docs/api_doc/README.md#basetask)
    - [鎴浘 (Screenshot)](docs/api_doc/README.md#鎴浘-screenshot)
    - [杈撳叆 (Input)](docs/api_doc/README.md#杈撳叆-input)
    - [OCR](docs/api_doc/README.md#ocr)
    - [鎵惧浘 (Image finding)](docs/api_doc/README.md#鎵惧浘-image-finding)
* [杩涢樁浣跨敤](docs/after_quick_start/README.md)
  - [1. 妯℃澘鍖归厤 (Template Matching)](docs/after_quick_start/README.md#1-妯℃澘鍖归厤-template-matching)
  - [2. 澶氳瑷€鍥介檯鍖?(i18n)](docs/after_quick_start/README.md#2-澶氳瑷€鍥介檯鍖?i18n)
  - [3. 鑷姩鍖栨祴璇昡(docs/after_quick_start/README.md#3-鑷姩鍖栨祴璇?
  - [4. 浣跨敤 GitHub Action 鑷姩鍖栨墦鍖呬笌鍙戝竷](docs/after_quick_start/README.md#4-浣跨敤-github-action-鑷姩鍖栨墦鍖呬笌鍙戝竷)
* 寮€鍙戣€呯兢: 938132715
* pip [https://pypi.org/project/ok-script](https://pypi.org/project/ok-script)


## 浣跨敤ok-script鐨勯」鐩細

* 楦ｆ疆 [https://github.com/ok-oldking/ok-wuthering-wave](https://github.com/ok-oldking/ok-wuthering-waves)
* 鍘熺(涓嶅湪缁存姢,
  浣嗘槸鍚庡彴杩囧墽鎯呭彲鐢? [https://github.com/ok-oldking/ok-genshin-impact](https://github.com/ok-oldking/ok-genshin-impact)
* 灏戝墠2 [https://github.com/ok-oldking/ok-gf2](https://github.com/ok-oldking/ok-gf2)
* 鏄熼搧 [https://github.com/Shasnow/ok-starrailassistant](https://github.com/Shasnow/ok-starrailassistant)
* 鏄熺棔鍏遍福 [https://github.com/Sanheiii/ok-star-resonance](https://github.com/Sanheiii/ok-star-resonance)
* 浜岄噸铻烘棆 [https://github.com/BnanZ0/ok-duet-night-abyss](https://github.com/BnanZ0/ok-duet-night-abyss)
* 鐧借崋鍥炲粖(鍋滄鏇存柊) [https://github.com/ok-oldking/ok-baijing](https://github.com/ok-oldking/ok-baijing)
* 缁堟湯鍦?[https://github.com/AliceJump/ok-end-field](https://github.com/AliceJump/ok-end-field)
* 寮傜幆 [https://github.com/BnanZ0/ok-nte](https://github.com/BnanZ0/ok-nte)
