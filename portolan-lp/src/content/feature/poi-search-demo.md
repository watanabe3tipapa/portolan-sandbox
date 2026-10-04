---
title: "ケーススタディ — OpenPOI API 検索デモ（認証なし・サーバーなし）"
description: "認証も API キーもサーバーも使わない POI 検索デモを公開する。OpenPOI API の実仕様と、ブラウザの fetch だけで完結する実装の落とし穴を整理します。"
pubDate: 2026-10-04
---

## 3 つの「不要」で動く検索デモ

公開済みのデモは **[/poi-search/](/poi-search/)** です。キーワードや現在地から日本の施設を探し、Leaflet で地図にプロットし、Portolan 形式で JSON を書き出せます。実装は Astro の静的ページ 1 枚と Leaflet の CDN 読み込みだけです。

この構成の意義は、**認証・API キー・サーバーという 3 つの「不要」を、Portolan の公開基盤（静的サイト + GitHub Pages）の上にそのまま載せられる**ことです。

<figure class="diagram">
  <iframe src="../../diagrams/poi-search-demo.html" title="OpenPOI 検索デモのワークフロー" loading="lazy"></iframe>
  <figcaption>図: OpenPOI 検索デモ — 入力から API 取得、地図表示、Portolan 形式の書き出しまで。認証もサーバーも介在しない</figcaption>
</figure>

## 使ったデータソース：OpenPOI API

| 項目 | 内容 |
|---|---|
| ベース URL | `https://api.openpoiapi.com/v1` |
| 認証 | 不要（API キーの発行なし） |
| CORS | 全オリジン許可（`access-control-allow-origin: *`） |
| 収録件数 | 約337万件（日本全国） |
| 内訳 | Overture Maps 約249万件 + 食品営業許可・届出オープンデータ（JFF）約88万件 |
| レート上限 | 利用者ごとの制限なし。API 全体で定常 200 req/s・バースト 600 req/s |
| 他の入口 | `POST /mcp`（`search_facilities` / `dataset_info` の2ツール）、`GET /openapi.json` |

## エンドポイントと使い分け

```text
GET /v1/search
  q        検索キーワード（スペース区切りは OR。省略可）
  center   中心座標「lng,lat」— 経度が先。指定すると近い順に返す
  radius   center からの半径（メートル。既定 50000）
  bbox     矩形「minLng,minLat,maxLng,maxLat」— center より優先
  limit    最大件数（1〜200 にクランプ）

GET /v1/suggest
  q        入力途中のキーワード（複数語は AND）
  bbox     先に探す地図範囲。0 件なら scope: nationwide へ自動で広げる
  fields   minimal を指定すると category / source / licenses を省いた軽量応答
```

使い分けは明快です。**入力補完は `/v1/suggest`、一覧取得は `/v1/search`** です。`/v1/suggest` は表記ゆれの吸収・重複除去・並び替えをサーバー側で済ませるため、候補を「返った順に描画」するだけです。`/v1/search` の複数語は OR で広く返す仕様なので、`東京スカイツリー` や `ラーメン 渋谷` のような検索では無関係な結果が先頭に並びます。近い順の結果が欲しければ `center` を指定します。デモの現在地検索は `center` + `radius=1000` の組み合わせです。

## 実装で踏んだ落とし穴

### `center` は「経度,緯度」の順

逆順で送ると、座標が範囲外と判定されて 400 になります。エラーメッセージが「緯度と経度が逆になっていませんか？」と教えてくれるので、原因特定は容易です。

```bash
# 正しい（lng,lat）
curl 'https://api.openpoiapi.com/v1/search?center=141.3545,43.0618&radius=1000&limit=1'
# → 200

# 逆（lat,lng）
curl 'https://api.openpoiapi.com/v1/search?center=43.0618,141.3545&radius=1000&limit=1'
# → 400 {"error":"center の緯度が範囲外です（-90〜90）: 141.3545。緯度と経度が逆になっていませんか？（経度,緯度 の順で、経度が先です）"}
```

### 1文字の入力では補完が返らない

実測すると、1文字（`ラ`、`薬`）では候補が 0 件、2文字（`喫茶`）では全国へ広げて 3 件返りました。補完を出す最小文字数は 2 文字とするのが安全です。

### `address` や `prefecture` が空の記録がある

Overture Maps 由来のレコードには住所が入っていないことがあり、空文字で返ってきます。検索結果を「住所 + 都道府県 + 市区町村」で表示する実装は、**空文字の行が並びます**。デモでは名称が空のときに住所を、住所も空なら「（名称不明）」を代替表示しています。書き出し側の GeoJSON は API が返した値のまま残すのが正しいので、表示と書き出しで挙動を変えてあります。

保存した結果を使うときは、**`licenses` と `attributions` をレコードと一緒に保存**します。後から出典を示せる状態にしておく必要があります。

### `lat` / `lng` は文字列にも空文字にもなる

仕様上 `number | string` で、座標を持たない施設は空文字です。`Number()` で変換して `Number.isFinite()` で除外しないと、`fitBounds` に空文字が渡って地図が壊れます。デモでは座標のないレコードをリストには出しつつ、地図と GeoJSON からは外しています。

### 429 は CORS エラーとして見える

レート超過（429）は API Gateway が返すため、CORS ヘッダが付かず、ブラウザからは**ネットワークタブで CORS エラー**として現れます。`try / catch` で「レート上限を超過しました」と表示していますが、これは API 側の仕様なので、CORS を無効にして回避するのではなく、表示して待つのが正解です。

### 地図の初期化は一度だけ

Leaflet は同じコンテナを二度 `L.map()` すると例外を投げます。検索のたびに `L.map('map')` を呼ぶ実装は、2 回目以降で壊れます。デモでは Leaflet のインスタンスを保持し、マーカーレイヤーを remove して差し替えています。

## 実装の要点

### 認証ヘッダーなしで呼べる

```js
const API = 'https://api.openpoiapi.com/v1';

// キーワード検索
const url = `${API}/search?q=${encodeURIComponent(q)}&limit=20`;

// 近傍検索（center は経度,緯度の順）
const near = `${API}/search?center=${lng},${lat}&radius=1000&limit=20`;

const response = await fetch(url, { headers: { Accept: 'application/json' } });
const data = await response.json();   // { count, results: [...] }
```

### 補完はデバウンスして `/v1/suggest` に任せる

```js
input.addEventListener('input', () => {
	clearTimeout(timer);
	timer = setTimeout(async () => {
		const data = await fetch(`${API}/suggest?q=${encodeURIComponent(q)}&limit=8`).then((r) => r.json());
		renderCandidates(data.suggestions);   // 返った順に描画
		renderVocabulary(data.vocabulary);     // 業種・ブランド・地名の語彙
		renderGhostText(data.completion);      // 入力欄に重ねる補完文字列
	}, 250);
});
```

`/v1/suggest` は辞書で表記ゆれを吸収する（`すたーば` → `スターバックス`）ので、地名やチェーン名を利用者側が個別に対応付ける必要はありません。`vocabulary` は入力の先頭に前方一致した語彙で、1文字でも返ってきます。

### 地図は一度だけ初期化する

```js
let map = null;
let markers = null;

function ensureMap() {
	if (map) return map;
	map = L.map(mapEl).setView([43.0618, 141.3545], 12);   // 初期表示は札幌市
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; OpenStreetMap contributors',
	}).addTo(map);
	return map;
}

function drawMarkers(records) {
	const current = ensureMap();
	if (markers) markers.remove();
	markers = L.layerGroup().addTo(current);
	const points = [];
	for (const r of records) {
		if (!Number.isFinite(r.lat) || !Number.isFinite(r.lng)) continue;  // 空文字を除外
		points.push([r.lat, r.lng]);
		L.marker([r.lat, r.lng]).bindPopup(popupNode(r)).addTo(markers);
	}
	if (points.length > 0) current.fitBounds(L.latLngBounds(points).pad(0.15));
}
```

検索語は入力欄に残したまま、現在地検索は別のクエリとして発行します。現在地検索のラベルで入力欄を上書きすると、次のキーワード検索が壊れます。

## Portolan 形式で書き出す

結果リストには「表示する」だけでなく、**機械可読な JSON に落とす**ボタンを置いています。出力は 2 種類です。

`collection.json`（カタログ）

```json
{
  "stac_version": "1.0.0",
  "type": "Collection",
  "id": "openpoi-世田谷区",
  "description": "OpenPOI API キーワード検索「世田谷区」の結果 20 件",
  "license": "various",
  "extent": { "spatial": { "bbox": [[139.589409681, 35.6032342, 139.682888842, 35.66782735]] } },
  "summaries": {
    "languages": ["ja"],
    "categories": ["restaurant", "cafe", "bakery", "retail_other", "service_other", "unknown"]
  },
  "providers": [
    { "name": "OpenPOI API", "roles": ["producer"], "url": "https://openpoiapi.com/attribution.html" }
  ],
  "links": [
    { "rel": "items", "type": "application/geo+json", "href": "items.geojson" },
    { "rel": "license", "type": "text/html", "href": "https://openpoiapi.com/attribution.html" },
    { "rel": "via", "type": "text/html", "href": "https://watanabe3tipapa.github.io/portolan-sandbox/poi-search/" }
  ]
}
```

`items.geojson`（1 件 = 1 Feature）

```json
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [139.682204, 35.648873] },
  "properties": {
    "name": "",
    "name_kana": "",
    "address": "東京都世田谷区池尻",
    "prefecture": "東京都",
    "city": "世田谷区",
    "category": "restaurant",
    "business_type": "restaurant",
    "level": null,
    "source": "jff",
    "licenses": ["公共データ利用規約（第1.0版, PDL1.0）"],
    "attributions": ["厚生労働省 食品衛生申請等システム（オープンデータ）"]
  }
}
```

`extent.spatial.bbox` は結果の包围箱、`providers` と `rel: license` は出典です。Feature の `licenses` / `attributions` は API が返した配列をそのまま保持しているので、**このファイルを渡せば AI エージェントは出典付きの施設を扱えます**。サーバーもビルドも介さず、ブラウザの `Blob` だけで生成しています。

## 出典・ライセンス

OpenPOI API の配信データは、由来ごとにライセンスと表記が違います。API はレコードごとに `licenses` と `attributions` を返すので、**表示も書き出しもその配列のまま**扱います。

| 由来 | ライセンス | 表記 |
|---|---|---|
| Overture Maps Places（Meta・Microsoft・PinMeTo・Krick・RenderSEO・DAC・BrightQuery 提供分） | CDLA-Permissive-2.0 | Overture Maps Foundation, overturemaps.org |
| Overture Maps Places（Foursquare 提供分） | Apache-2.0 | Overture Maps Foundation / Copyright 2024 Foursquare Labs, Inc. |
| Overture Maps Places（AllThePlaces 提供分） | CC0-1.0 | 表示義務なし |
| Japan Food Facilities（自治体・厚生労働省のオープンデータ、81ソース） | CC BY 2.0 / 2.1 JP / 3.0 / 4.0（76ソース）、公共データ利用規約 PDL1.0（4ソース）、CC0 1.0（1ソース） | ソースごとに異なる |
| コード表: geolonia/japanese-addresses | CC BY 4.0 | Geolonia Inc. |

実測した 20 件では、`licenses` に「公共データ利用規約（第1.0版, PDL1.0）」「CC BY 4.0」「CDLA-Permissive-2.0」「Apache-2.0」が混在していました。**1 つの検索結果の中に複数のライセンスが混ざる**ため、1 つのライセンスとしてまとめることはできません。レコード単位の `licenses` と `attributions` を残す実装にしたのはこのためです。

Foursquare 由来（Apache-2.0）は、API の形でデータを配信する場合に NOTICE.txt の内容をその API の開発者向けドキュメントに目立つ形で含めることが求められます。OpenPOI API は自身の出典・ライセンスのページで全文を転記して要件を満たしています。本デモはブラウザで結果を引くだけなので、この要件は直接及びません。このデータを含む API を自分で公開する場合は、同じ記載が自分の API のドキュメントに必要です。

公共データ利用規約 PDL1.0 は、「出典とは別に、編集・加工を行ったこと及びその主体」の記載を求めます。OpenPOI API は加工の主体を「OpenPOI API」と明記しています。本デモは表示とダウンロードのみを行い、データを加工して再配布しないため、新たな主体の記載は発生しません。保存した結果を加工して公開する場合は、その加工の主体を明記してください。

デモページと本記事の両方で、出典として OpenPOI API と `https://openpoiapi.com/attribution.html` へのリンクを掲載しています。地図タイルは &copy; OpenStreetMap contributors です。

## このケースが示すこと

Portolan が公開しているものが示しているのは、**データをどこかに集めることではない**ということです。

- API 側が認証と CORS を開いているだけで、ブラウザからの直接アクセスが成立する
- 検索結果には「表示する」と「機械に読ませる」の 2 面があり、片方を捨てても情報量は変わらない
- 出典は**取得する時点ではなく保存する時点**で確定する。`licenses` / `attributions` を受け取ったまま保存しておけば、あとから加工して公開できる

公開基盤（静的サイト + GitHub Pages）とデータソース（認証不要 API）を、どちらもオープンなまま重ね合わせることができる。どちらか一方が閉じていれば成立しない構成です。

## さらなる発展

- **`/v1/suggest` の `vocabulary` 活用**: 業種・ブランド・地名の語彙を検索フィルターに使える
- **`POST /mcp` 経由のエージェント経路**: `search_facilities` ツールを MCP クライアントに公開し、「近くのラーメン屋」のような要求をエージェントに直接させた
- **`bbox` 連動**: 地図を動かしたまま補完の範囲を変える（`/v1/suggest` は `bbox` 指定を受け付ける）