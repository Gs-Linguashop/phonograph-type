# 形聲輸入法

基於形聲字形的[Rime](https://rime.im)傳統漢字/简体汉字輸入方案

## 簡介

本輸入法圍繞通過字形輸入形聲字的**聲**部分設計。
比如「輸」字的聲音由「俞」字決定，那麼它的編碼邏輯就是

* `輸`（字）&rarr;`俞`（聲音部分）&rarr;`亼月刀`（拆分）&rarr;`入夕戈`（編碼）

對於諸多漢字組件，本輸入法主要通過它們的**含義**歸類編碼爲26個鍵，鍵盤請參考[這裏](layout.txt)。按對應字母順序，這些漢字組件分別是
* `犬不人勺王口田止一又山皿冂入二三隹夕水也屮卩戈大木目`

組件單獨成字时，請儘量按字形強行拆分成其它更小的組件。

具體組件分類請參照[這裏](src_encode/basic.txt)

按“`”鍵使用[朙月拼音](https://github.com/rime/rime-luna-pinyin)反查上古音

在iOS上使用[倉hamster](https://github.com/imfuxiao/Hamster)App部署諧聲雙拼輸入法時，可以安裝[專用鍵盤](phongraph_keyboard.custom.yaml)；鍵盤文件可以在設置中導入，新手請參考[倉wiki](https://github.com/imfuxiao/Hamster/wiki)；配套iOS的鍵盤保留了上下劃常用數字和標點，請劃一劃試試；上劃Space切換英文，橫向劃動字母可以實現首字母拼寫；使用反查功能請確認反查用的字典也已安裝

授權條款：見 [LICENSE](LICENSE.txt)

## 待辦

* 調整鍵位
* 調用phonograph關係庫
* 根據更完善的部首參考，目前除聲首外部首是按Unicode康熙部首排列處理的