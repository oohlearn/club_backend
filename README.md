# 社團全家桶專案 - 後端

使用框架 Django

## 安裝管理套件 Poetry

### `curl -sSL https://install.python-poetry.org | python3 -`

## 開啟虛擬環境

### `poetry shell`

## 安裝專案相關套件

### `poetry install`

進行遷移

### `python manage.py migrate`

建立 superuser

### `python manage.py createsuperuser`

在本地執行專案

### `python manage.py runserver`

瀏覽 API
http://127.0.0.1:8000/api/

後台管理系統
http://127.0.0.1:8000/admin

---

#資料建立
共分三個區塊，『樂團資料』、『購物商城』以及『購票活動』

##樂團資料

- Home contents 會自動建立一個，直接在裡面選擇要顯示在首頁的內容即可

_影片
_ 網址列分兩種
_ youtube 網址：會直接開啟新分頁，連到 youtube 網站去
_ 內嵌網址：會直接在網頁瀏覽
*文章
*僅有發布狀態選擇「已發布」，才會顯示在頁面

*相簿
*目前增加照片僅能一張一張增加，無法一次增加多張照片

##購物商城

*商品建立
*商品標籤目前會以文字顯示在頁面上，之後會想辦法顯示在圖片上

\*其他皆還沒完成

##購票活動
**請按照順序建立活動**

1. 建立 venues
2. 建立活動
   - 若外部售票系統網址有填寫，則不會使用內建的售票系統
   - 座位分區有兩種形式可以選擇，僅能擇一
     - Zones：若『排號』名稱是以『字母』，如 A、B、C
     - Zones for number rows：若座位號是『號碼』，如 1、2
3. 建立座位表，選擇剛剛上方所使用的座位分區方式
   - 在每個分區裡面建立座位
   - Zones，請以以下格式輸入：A1、A2
   - Zones for number rows，請用下拉式選擇「排數」，座號僅需要寫數字即可
   - 票價及座位顯示顏色若沒有填寫，會自動帶入「當前分區」的資料，無須每個一一填寫。需要調整個別座位再填寫即可。
   - 篩選功能：若有多場活動，可使用篩選功能選出該場演出的座位分區
