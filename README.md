# LINEBOT
---

## 使用技術及環境
環境 : Heroku、LINE、Azure<br>
技術 : Linebot api、NLP語意分析、Azure資料庫、基礎爬蟲、Random隨機取樣。

## 架構
Bot會動態連結至Azure資料庫進行語意分析，查找合適答案。<br>
也能夠查看所有使用者提問(參考 資料庫LOG.png)，以優化資料庫。<br>
(資料庫能夠手動新增語句也能直接上傳CSV檔)。<br>
<div><img width="500" height="750" src="https://github.com/jellyfish4757/linebot/blob/master/%E6%9E%B6%E6%A7%8B%E7%B0%A1%E4%BB%8B.jpg"/></div>

## 使用須知:
1.看到的所有按鈕點擊後皆會產生不同效果。<br>
2.可以詢問電影類的問題。<br>
3.輸入"新聞"來得知即時資訊(預設爬取蘋果新聞)。<br>
4.傳送貼圖會隨機回傳貼圖。<br>
<br>
HINT : <br>
詢問電影時，第一次回傳極慢為正常現象，(Azure免費方案須從休眠喚醒)，<br>
等待約15秒後多發幾次即會收到回復，<br>
若回復為No good match found in KB，<br>
即為資料庫無最佳答案，<br>
試試不同問法即可。

## 對話畫面:
<div><img width="400" height="800" src="https://i.imgur.com/Kvnjybn.jpg"/></div><br>
<div><img width="400" height="800" src="https://i.imgur.com/bjMFFHS.jpg"/></div><br>
<div><img width="400" height="800" src="https://i.imgur.com/geKyru4.jpg"/></div>


## 期待改進方面:
若是一直call自己的function維持喚醒狀態，即能很快回覆，卻會違反Heroku條款，須付費。<br>
資料庫會隨使用者提問多寡而慢慢完備，初期資料庫資訊不足。(參考 資料庫data.png)<br>
能夠增加連續對話功能。(接續上一話題)
