# DEV-MEMO.md

portolan-sandbox 開発メモ。「AI が直接読める空間インフラ Portolan」を多くの人に身近に使ってもらうための手法を開拓する実験リポジトリ。ASTRO で構築した LP とチュートリアル・特集ページを GitHub Pages で公開する。

## 構想(PLAN.md から移行)

- できるだけ多くの人々が Portolan を身近に使えるようにするための手法の開拓
- Google アカウントだけで全ての操作(認証・デプロイなど)に対応したい
- 考察していること: Portolan と Google Colaboratory との連携手法 / Colab MCP server(パーソナル・開発サーバーとしての位置付け)の利活用
- 直接読める空間インフラの啓発活動と、その具体的な活用方法の検討

## ゴール

- **Portolan という新しいオープン仕様を広めるためのランディングページ(LP)を GitHub Pages で公開**
- **チュートリアル・特集コーナーを追加**し、「作って・公開するところまで」を学べるコンテンツを提供
- **Google アカウントだけで**認証・デプロイまで完結させる構成を将来実現(構想)
- 日英 2 言語の README でプロジェクトの入口を整える(現行 v0.1.2)

## 決定事項

1. **ポートフォリオ構成**: ルートに `Portolan_要約.html`(GeoAI 第16回 要約)・LP 用 ASTRO プロジェクト(`portolan-lp/`)を共存。構想は本ファイル(DEV-MEMO.md)の「構想」節に集約
2. **LP は ASTRO(basics テンプレート)で構築** → 静的出力で GitHub Pages にデプロイ
3. **デプロイは GitHub Actions**(`deploy.yml`)に一本化。main への push で自動ビルド・公開
4. **チュートリアルはコンテンツコレクション(`tutorial`)で管理**。番号(order)付きで学習順を明示
5. **特集コーナーはコンテンツコレクション(`feature`)で管理**。Google Maps×OSM 連携・共通プロトコル・実証デモ・Colab MCP server を収録
6. README は okf-seedling に倣って **日英 2 版**(メインは日本語)
7. **ライセンスは MIT**。LICENSE ファイルをリポジトリ配布(okf-seedling と同形式)
8. **共有・引用する URL には必ず `/portolan-sandbox/` を付ける**。プロジェクトサイト(`base: /portolan-sandbox/`)のため、ドメイン直下の URL は別サイト管辖で 404 になる

## 技術制約(検証済み)

1. **Astro 7 では `type: 'content'` が機能しない**。コンテンツコレクション定義は `glob()` ローダーを使うこと
   - `type: 'content'` 指定だと sync は通るが、ビルド時に `is empty` 警告が出て記事が出力されない
   - → `import { glob } from 'astro/loaders';` + `loader: glob({ pattern: '**/*.md', base: './src/content/<collection>' })` で解決
2. **サブディレクトリのページから Layout への import パスは 2 階層上がる**
   - `src/pages/tutorial/index.astro` 等は `import Layout from '../../layouts/Layout.astro'`(1 階層では失敗)
3. **GitHub Pages 用の base 設定が必要**
   - `astro.config.mjs` で `site: 'https://watanabe3tipapa.github.io'`・`base: '/portolan-sandbox'` を指定
   - dev 時の URL は `/portolan-sandbox/` 配下になる(base 反映)
4. **GitHub Actions のワークフローはリポジトリルートの `.github/workflows/` に置く**
   - ASTRO プロジェクトがサブディレクトリ(`portolan-lp/`)なので、`working-directory: portolan-lp` を各 step に指定
   - アップロード artifact は `./portolan-lp/dist`

## リポジトリ構造

```
portolan-sandbox/                    ← GitHub Pages 公開元(リポジトリ)
├── .github/workflows/
│   └── deploy.yml                   # ASTRO build → GitHub Pages deploy
├── Portolan_要約.html               # GeoAI 第16回「地図データを配る」時代の終わり 要約
├── README.md / README_en.md         # プロジェクト README(日本語メイン / 英語)
├── DEV-MEMO.md                      # 本ドキュメント(構想の source of truth)
├── LICENSE                          # MIT ライセンス(2026 watanabe3tipapa)
├── demos/
│   └── colab-mcp-server/            # Colab MCP server 検証プロジェクト(fastmcp)
│       ├── server.py                # MCP ツール(read/write/convert/validate/deploy)
│       ├── colab_portolan_mcp.ipynb # Colab で動くノートブック
│       └── fixtures/collection.json # 検証用コレクション
└── portolan-lp/                     # ASTRO 製 LP
    ├── astro.config.mjs             # site / base(GitHub Pages 用)・output: static
    ├── src/
    │   ├── content.config.ts        # コレクション定義(tutorial / feature、glob ローダー)
    │   ├── components/
    │   │   └── PoiSearch.astro      # 公開デモの検索 UI(Leaflet・補完・書き出し)
    │   ├── content/
    │   │   ├── tutorial/            # 6 本(order 0〜5)
    │   │   └── feature/             # 6 本
    │   ├── layouts/
    │   │   └── Layout.astro         # 日本語ヘッダ・文字セット
    │   └── pages/
    │       ├── index.astro          # LP(ヒーロー・特徴・チュートリアル・特集・CTA)
    │       ├── 404.astro            # 404(接頭辞を省いた URL を正しい場所へ誘導)
    │       ├── poi-search.astro     # 公開デモ(/poi-search/、OpenPOI API 検索)
    │       ├── tutorial/
    │       │   ├── index.astro      # 一覧(order 順)
    │       │   └── [...slug].astro  # 個別 + prev/next ナビ
    │       └── feature/
    │           ├── index.astro      # 一覧(新着順)
    │           └── [...slug].astro  # 個別 + prev/next ナビ
    └── package.json                 # dev / build / preview
```

## コンテンツコレクション

### tutorial(チュートリアル、order 順)

| order | id | タイトル |
|---|---|---|
| 0 | 00-what-is-portolan | What is Portolan — 基礎 |
| 1 | 01-create-a-collection | Create a Collection — 最初のコレクション |
| 2 | 02-agents-md | AGENTS.md — AI に使い方を伝える |
| 3 | 03-deploy-github-pages | Deploy — GitHub Pages で公開 |
| 4 | 04-google-colab | Google Colaboratory — パーソナル・開発サーバー |
| 5 | 05-local-llm | Local LLM — マウントしたローカル LLM でデータ解析する |

frontmatter: `title` / `description` / `order`(number) / `pubDate`(date)

### feature(特集、新しい順)

| id | タイトル |
|---|---|
| poi-search-demo | ケーススタディ — OpenPOI API 検索デモ(認証なし・サーバーなし) |
| colab-mcp-server | Colab MCP server に期待できる機能 |
| gmaps-osm-interop | Google Maps × OpenStreetMap — データ連携 |
| common-protocols | 共通プロトコルの用例 — STAC・GeoParquet・PMTiles |
| helsinki-demo | ケーススタディ — OGC Connect Helsinki デモ |
| google-github-workflow | ケーススタディ — Google アカウント × GitHub アカウントの両立ワークフロー |

frontmatter: `title` / `description` / `pubDate`(date)

## マイルストーン

| # | 内容 | 完了条件 |
|---|------|----------|
| M1 | 構想の整理(DEV-MEMO.md に集約) | 構想・考察・啓発活動の観点を移行・文書化 |
| M2 | ASTRO プロジェクト生成 + GitHub Pages 設定 | `npm run build` が静的サイトを出力 |
| M3 | GitHub Actions デプロイワークフロー | リポジトリルートに `deploy.yml`(サブディレクトリビルド対応) |
| M4 | README 日英 2 版作成(v0.1.0) | README.md / README_en.md を生成、okf-seedling の構成に準拠 |
| M5 | チュートリアルコーナー | コレクション + 記事 5 本 + 一覧・個別ページ |
| M6 | 特集コーナー | feature コレクション + 記事 4 本 + 一覧・個別ページ |
| M7 | リモート公開 | GitHub リポジトリ作成 + GH Pages に LP 公開(公開 URL で 200 確認) |
| M8 | LICENSE 決定(MIT) | LICENSE 追加 + README ライセンス節・バッジへ反映 |
| M9 | 記事内容の拡充 | tutorial 5 本 → 全記事に具体例・コード・表を追加(+622行) |
| M10 | Colab MCP server 検証 | read/convert/validate の4ツール実装・公開デモコレクションで動作確認(HTTP 200) |
| M11 | Colab MCP 次段階 | deploy_to_github_pages / write_to_drive 追加、Pages へのMCP経由デプロイを実証 |
| M12 | ローカル LLM 用例 | Ollama を Drive にマウントして解析するツール4種 + 実機検証(ask/geo_analyze) |
| M13 | 両アカウント WF 記事 | tutorial 05-local-llm + feature google-github-workflow の新規追加 |
| M14 | 公開デモ + 事例記事 | `/poi-search/`(OpenPOI API 検索・補完・地図・書き出し)+ feature poi-search-demo + archify 12 図目 |

## 実装メモ

- `astro dev` は AGENTS.md に従いバックグラウンドモードで運用(`astro dev --background` / `astro dev stop` / `astro dev status` / `astro dev logs`)
- ページ共通スタイル(ダークグラデーションのヒーロー + #c45c3e アクセント)は okf-seedling や Portolan_要約.html の雰囲気を踏襲
- 個別記事ページは breadcrumb / prev・next ナビゲーションを備える
- 特集一覧の並びは `pubDate` 降順(新しい順)

## デプロイ状況

- GitHub Pages: **公開済み**(2026-09-11)。公開 URL: https://watanabe3tipapa.github.io/portolan-sandbox/
- リポジトリ: watanabe3tipapa/portolan-sandbox(Public)
- デプロイ経路: GitHub Actions(`.github/workflows/deploy.yml`)の build → deploy-pages。main への push で自動デプロイ
- Pages 設定: Source を **GitHub Actions**(build_type: workflow)に設定済み

## 検証記録: Colab MCP server(`demos/colab-mcp-server/`)

「Google アカウントだけで完結する認証・デプロイ」のうち、まず **Colab MCP server(パーソナル・開発サーバー)としての基盤**を検証。

- `uv init` した Python プロジェクト `portolan-mcp`(fastmcp 4.0.3 + geopandas + pyarrow)
- ツール実装(`server.py`): `read_collection` / `read_geoparquet` / `convert_geoparquet` / `validate_collection`
- **検証結果(2026-09-11)**:
  - `validate_collection(VALID)` → `valid: true`(fixtures/collection.json、7 フィールド正常)
  - `read_collection(URL)` → https://watanabe3tipapa.github.io/portolan-sandbox/demo-collection/collection.json を読み、id/ライセンス/bbox/リンクを返すことに成功
  - `read_geoparquet(URL)` → 公開中の demo-collection/data/poi.parquet(3857)を 4326 に変換して件数・CRS・サンプルを返すことに成功
  - `convert_geoparquet(ローカル)` → 3857→4326 変換後のファイル書き出しに成功(CRS を pyarrow で読み検証)
  - MCP server は HTTP トランスポート(`http://127.0.0.1:8000/mcp`)で起動確認
- **技術メモ**(検証で判明):
  - `geopandas.read_parquet()` は URL 直接読み込み不可 → `urllib` でバイト列取得 → `BytesIO` に包む
  - fastmcp 4.x では `mcp._tool_manager` 等の内部属性は非公開。検証は関数を直接 import して実行
  - `uv init` を誤って `portolan-lp/`(Astro プロジェクト)内で実行しないこと。デモは `demos/<name>/` に分離
  - Git 管理: `demos/colab-mcp-server/.gitignore` で `.venv/` `__pycache__/` を除外。`uv.lock` は管理対象
- **デモコレクション**(公開 URL): https://watanabe3tipapa.github.io/portolan-sandbox/demo-collection/collection.json
  - 実体は `portolan-lp/public/demo-collection/`(Astro の `public/` に置くと `dist/` にコピーされ Pages で配信される)
  - サンプルデータ(poi.parquet): 東京 5 地点の POI(EPSG:3857 で保存 → AGENTS.md の「3857 は変換が必要」の例題に活用)

### 検証記録(続き): 次段階(認証・Drive・GitHub Pages デプロイ) — 2026-09-11

構想のゴール「Google アカウントだけで完結」のうち、残っていた 3 要素を追加・検証した。

- **ツール追加**(`server.py`):
  - `deploy_to_github_pages(repo, file_path, content, message)` — GitHub Contents API でファイルを commit。clone 不要で push も不要(commit 自体が push を兼ねる)
  - `write_to_drive(filename, content)` — Colab でマウント済み Drive へ書き込み
  - `_github_token()` / `_github_request()` — 認証の共通処理。トークンは `GITHUB_TOKEN` env、なければ `gh auth token` を参照
- **検証結果**:
  - `deploy_to_github_pages` を実リポジトリ(watanabe3tipapa/portolan-sandbox)の `portolan-lp/public/demo-collection/README.md` 新規作成で実行 → commit `80568a8` 成功
  - 約 45 秒後に https://watanabe3tipapa.github.io/portolan-sandbox/demo-collection/README.md が **HTTP 200** で配信(GitHub Actions の自動デプロイが起動)
  - つまり「git clone 不要・端末の git 環境不要」で、Contents API → commit → Pages 反映の一連が完結
- **Colab 用ノートブック**: `demos/colab-mcp-server/colab_portolan_mcp.ipynb`
  - Drive マウント(Google アカウント OAuth)→ GitHub token 入力 → server の各ツール呼び出し → Pages 反映確認まで 7 セクション
  - Colab 上では `getpass` で token を入力し、セル表示に残さない
- **技術メモ**:
  - GitHub Contents API は既存ファイル更新時に `sha` が必要(GET で取得 → PUT に含める)。404 なら新規作成
  - 認証は `gh` CLI の credential か env。Colab には `gh` が無いためトークン必須
  - 更新ファイルは `portolan-lp/public/demo-collection/` に置く前提(Astro の `public/` は dist にコピーされて Pages に配信)

## 追録: Google アカウントと GitHub アカウントを両方持っている場合

構想の「Google アカウントだけで完結」はハードルを下げるための極論であり、**現実の典型ユーザーは両アカウントを持っている**。両方保有時のワークフローを整理する(2026-09-11 追録)。

### 役割分担の整理

| レイヤー | Google アカウント(Colab) | GitHub アカウント(リポジトリ) |
|---|---|---|
| 認証 | OAuth でログイン、追加基盤不要 | GitHub 自体が認証基盤 |
| データ生成・検証 | GeoPandas 等で前処理・CRS 変換 | / |
| コンテンツ配信 | / | GitHub Pages(GitHub Actions) |
| メタデータ・カタログ | 生成した collection.json を置く | Pages 上の公開 URL(demo-collection 等) |
| AI 連携 | Colab MCP server(パーソナル・開発サーバー) | Pages 公開データを参照(認証不要) |
| 版管理・コラボ | / | git / PR / Issue |

### 両方持っているときの主経路(本リポジトリの実例)

```text
データ準備(Colab)
  └─ GeoPandas で 3857→4326 変換などの前処理・検証
  └─ collection.json / AGENTS.md を生成
public/ に配置 → commit → push(GitHub アカウント)
  └─ GitHub Actions が自動で build → Pages デプロイ
AI エージェント(任意の MCP クライアント)
  └─ Pages 公開 URL(collection.json / *.parquet)を直接参照
  └─ Colab MCP server を経由すれば、Google アカウントの状態も操作
```

### 使い分けの指針

| 状況 | どちらを使うか |
|---|---|
| 手元にいないがデータを確かめたい | Google アカウント + Colab(ブラウザだけで完結) |
| 公開・配信・版管理したい | GitHub アカウント(Pages / Actions / git) |
| エージェントに「読ませる」 | どちらのアカウントでも可(Pages 公開 URL は認証不要) |
| 個人の開発サーバーとして使いたい | Google アカウント + Colab MCP server |

- **本リポジトリは「両方持っている」場合の実例**であり、Python をインストールできない環境でも Colab でデータを整えて GitHub Pages へ渡せる。
- 「Google アカウントだけ」の極論は、GitHub 未所有の初学者や教育現場を想定した下位互換の構想として残す。

### 検証記録(続々): ローカル LLM 環境のマウント用例 — 2026-09-11

「Colab 上にローカル LLM をマウントすれば、多様な解析(空間解析含む)が可能になる」という仮説の実装を行った。

- **ツール追加**(`server.py`、依存に `ollama` Python クライアントを追加):
  - `ollama_status(model)` — Ollama バイナリ有無・モデル保持状況の確認
  - `pull_local_llm(model)` — モデルをダウンロード(例: qwen2.5:0.5b)
  - `ask_local_llm(question, model, system)` — ローカル LLM へ直接質問(外部 API へ送らない)
  - `geo_analyze_local_llm(source, question, model)` — GeoParquet を読み、サンプルをローカル LLM で分析
- **ポイント**: `OLLAMA_MODELS` に Google Drive パスを指定してサーバー起動することで、モデルを**Drive に永続マウント**し、ランタイム再起動後も再利用できる
- **Colab ノートブック**にセクション 8〜10 追加(Ollama インストール → Drive 永続化 → 起動 → モデル pull → 空間解析)
- **状態**: ツール読み込み・構文確認済み。モデル pull の実機検証は中断(Model サイズ約 500MB のため)。TODO: 後日まとめてチュートリアル化する際に再検証する
- **実機検証(2026-09-11、追記)**: `ollama pull qwen2.5:0.5b` 成功 → ローカルで `ollama_status` が `model_present: true` → `ask_local_llm`(CRS 質問に UTM と回答)／`geo_analyze_local_llm`(公開 poi.parquet を読んで "The dataset contains information about various locations." と回答)を確認。4 ツールすべて正常動作

## 今後やること(仮)

- 上記の各マイルストーン(M9〜M13)は完了。新規の検証テーマが出た時点で随時追加する

## 仕上げ: タイポチェック実施 — 2026-09-11

- 全 md / html を対象に日本語・英語のタイポをスキャンし、次の誤記を修正:
  - `helsinki-demo.md`: 「標深 FOSS4G」→「FOSS4G コミュニティにおける地理空間データの合言葉」
  - `DEV-MEMO.md`: 「servers 起動」→「サーバー起動」、「措置」→「操作」
  - `colab-mcp-server.md` / `gmaps-osm-interop.md`: 「措置」→「操作」、「実時間性」→「リアルタイム性」
  - `tutorial/04-google-colab.md`: 「このチュートリアルはおわり / 全 5 ステップ」→ 「途中です」+ 05 への案内（チュートリアル 6 本構成に整合）
  - `tutorial/00-what-is-portolan.md`: シリーズの流れに 06(ローカル LLM) を追加
- ビルド確認済み(14 ページ生成、エラーなし)。リポジトリ内の残存タイポは確認されず

## 仕上げ(図の総点検): archify 11 図 + iframe 埋め込み — 2026-09-30

LP に archify 図(全 11: tutorial 6 + feature 5)を埋め込み、総点検を実施した。

- **図の生成と配置**: すべて `--quality showcase --json` + `meta.locale: ja` + `meta.translations` に `examples/locales/ja.json`(423 キー)を注入。各図のフォルダは `.archify/arch-{tutorialNN|feat-*}-20260930-102113/`
- **iframe 埋め込み**: 11 記事すべての冒頭イントロ直後に `<figure class="diagram">` + `../../diagrams/<slug>.html`(相対パス、base ルートを経由して `/portolan-sandbox/diagrams/` に到達)。`Layout.astro` の `:global` スタイルに `.diagram` / `iframe` / `figcaption` を追加
- **タイポ・表記修正**:
  - `common-protocols`(図 JSON の edge ラベル + カード項目): 「指引」(中国語) →「案内」×2
  - `common-protocols.md`(ASCII 図): 「エージェントへの指引」→「エージェントへの案内」
  - `tutorial-04`(図 JSON): 「必要部分」→「必要な部分」(tutorial-00 の表現に統一)
- **検証方法**: 全 body/candidate に対し Python で機械スキャン(二重スペース・全角英数字・制御文字・中国語表現・表記揺れ等)。再生成した 2 図は candidate 再注入 → finalize 再実行(全ゲート pass)→ `public/diagrams/` に再コピー → `npm run build` ≠ 成功、preview + curl で全 11 記事・全 11 図が 200
- **残作業**: ユーザー確認後にコミット・push(未実施)

## 仕上げ(公開デモ): OpenPOI 検索デモ + archify 12 図目 + タイポチェック — 2026-10-04

`/poi-search/` に公開デモを追加し、12 枚目の archify 図とケーススタディ記事(事例 6 本目)を作成した。

- **方針**: Vue などの新規依存は増やさない(純 ASTRO + クライアント `<script>`)。Leaflet 1.9.4 は unpkg から SRI 付きで読み込む
- **追加・変更したファイル**:
  - `portolan-lp/src/components/PoiSearch.astro` — 検索 UI とロジック(新規)
  - `portolan-lp/src/pages/poi-search.astro` — 公開ページ(パンくず・試し方・利用上の注意・出典)(新規)
  - `portolan-lp/src/content/feature/poi-search-demo.md` — ケーススタディ(新規)
  - `portolan-lp/public/diagrams/poi-search-demo.html` — 12 枚目の図(新規)
  - `portolan-lp/src/layouts/Layout.astro` — `title` / `description` を任意 props に変更(既定値は従来どおり)
  - `portolan-lp/src/pages/feature/index.astro` / `README.md` / `README_en.md` — 記事数・図数・デモページを追記
- **機能**: キーワード検索 / 現在地検索(Geolocation)/ 入力補完(`/v1/suggest`)/ カテゴリ絞り込み / Leaflet 地図 / `collection.json` と GeoJSON の書き出し / 出典表示
- **実測して見つけた落とし穴**( artigoにも記載):
  - `center` は `lng,lat` の順。逆だと 400(エラーメッセージが理由を示してくれる)
  - 1 文字の入力では補完が 0 件(2 文字なら全国展開で返る)
  - Overture Maps 由来のレコードは `address`・`prefecture` が空文字、`name` も空のことがある
  - `lat` / `lng` は `number | string` で、座標なしは空文字。`Number.isFinite()` で除外しないと `fitBounds` が壊れる
  - 429 は CORS ヘッダを返さないため、ブラウザでは CORS エラーとして見える
  - 検索のたびに `L.map()` を呼ぶと 2 回目以降で例外。Leaflet のインスタンスを保持してレイヤーを差し替える
- **地図の初期表示**: 札幌市 `[43.0618, 141.3545]`(zoom 12)
- **12 枚目の図**: workflow / `schema_version: 2` / `--quality showcase` / `meta.locale: ja` + `ja.json`(423 キー)。作業フォルダ `.archify/workflow-poi-search-demo-20261004-100455/`。初回 finalize は `workflow/unexpected-root` で fail したが、`dataset` も root なので `semanticChecks.allowedRoots` に追加して再実行し、validate / deliver / check / browser-check の全ゲート pass・診断 0 件。1440〜2048px × light/dark でオーバーフローなし
- **検証**: `npm run build` で 16 ページ。Playwright(ローカル Chromium)で補完 8 件・語彙 1 件、検索 20 件とマーカー 20 個、絞り込み 20→4 件、現在地検索 20 件(入力欄の検索語を保持)、`collection.json` / GeoJSON のダウンロード(GeoJSON は 20 features)、0 件・空入力・420px 幅を確認し、console error / page error / request failed はいずれも 0。1440px / 420px とも横スクロールなし
- **タイポチェック**: 新しい 3 ファイルを対象に文字化け(U+FFFD)・無関係な語句の混入を機械スキャンして修正。出典セクションは `openpoiapi.com/attribution.html` の実内容(由来別ライセンス表、Foursquare の NOTICE.txt 全文転記要件、PDL1.0 の加工主体記載)に合わせて書き直し、JSON サンプルは書き出しの実測値と一致させた

## リリース: v0.1.2(2026-10-04)

- **公開デモの追加**: `/poi-search/` — OpenPOI API をブラウザの `fetch` で直接叩く POI 検索(認証・API キー・サーバー不要)。キーワード検索 / 現在地検索 / 入力補完 / カテゴリ絞り込み / Leaflet 地図 / `collection.json` と GeoJSON の書き出し
- **事例記事 6 本目**: `feature/poi-search-demo` — 実測した落とし穴(`center` の順序、1 文字の補完、空の住所、文字列・空文字の座標、429 の CORS 挙動、地図の二重初期化)と出典・ライセンスの条件
- **archify 12 枚目**: `poi-search-demo.html`(workflow / showcase / 日本語 UI)。作業フォルダ `.archify/workflow-poi-search-demo-20261004-100455/`
- **地図の初期表示**: 札幌市 `[43.0618, 141.3545]`
- **その他**: `Layout.astro` に任意の `title` / `description` を追加、特集一覧のリード文と README 日英 2 種の記事数・図数を同期、`plan/` を削除
- **検証**: `npm run build` 16 ページ / 全 28 URL が 200 / Playwright smoke でエラー 0

## 対応: 404 ページを追加(接頭辞を省いた URL の誘導) — 2026-10-04

`https://watanabe3tipapa.github.io/poi-search/` が 404 になる件への対応。この LP は `base: '/portolan-sandbox/'` のプロジェクトサイトなので、ドメイン直下に短い URL を作ることはできない(ドメイン直下は別の Quarto サイトが user site で公開している)。利用者が接頭辞を省いた URL を無意識にクリックしても迷わないように、GitHub Pages が配信する `404.html` を用意した。

- `portolan-lp/src/pages/404.astro`(新規)— GitHub Pages が `/portolan-sandbox/404.html` を配信し、プロジェクト内の未知のパスにこのページが出る
- 表示内容: プロジェクトサイトである旨と接頭辞の説明、主要的ページへのリンク(トップ / デモ / 特集 / チュートリアル / GitHub)、リクエストされたパス
- 接頭辞を省いたアクセス(`/poi-search` など)を検出し、正しい URL への移動リンクを前面表示(リンク先とラベルは `define:vars` で渡し、DOM は `textContent` と属性で組み立てる)
- 検証: ビルド 17 ページ。Playwright で `/poi-search/`・`/poi-search`(末尾スラッシュ無し)は誘導リンク表示、`/nope/` は非表示、console / page error 0、横スクロールなし
- 制約: ドメイン直下の 404(例 `https://watanabe3tipapa.github.io/poi-search/`)は別のサイトの 404 が返るため、このページでは拾えない。正しい URL は `https://watanabe3tipapa.github.io/portolan-sandbox/poi-search/`

## 決定: 共有時の URL には必ず `/portolan-sandbox/` を付ける — 2026-10-04

プロジェクトサイト(`base: /portolan-sandbox/`)なので、ドメイン直下の短い URL は無効。共有・引用時の URL には必ず接頭辞を含める運用とする。

- 決定事項 8 に追記(決定の記録として保持)
- 運用: README 日英 2 種の「連絡先 / 公開サイト」に注意書きを追加、`/poi-search/` のページと `feature/poi-search-demo` の記事に絶対 URL を明記
- `poi-search.astro` は `new URL(BASE_URL + 'poi-search/', Astro.site)` で共有用 URL を組み立てて表示(ハードコードしない)
- 補足: `404.html` が拾えないのはドメイン直下の 404 だけ(別サイトの管理領域)。プロジェクト内の誤りは `/portolan-sandbox/404.html` が誘導する

## 総点検: タイポチェック — 2026-10-04

公開前の機械スキャン。対象は 47 のテキストファイル(README 日英・DEV-MEMO・要約 HTML・記事 12 本・Astro/TS/yml/py)と、公開図 12 枚の可視テキスト。

- 検査項目: U+FFFD / 制御文字 / 不可視文字、韓国語・キリル・ギリシャ・タイ等の非日本語スクリプト、全角英数字、簡体字(日本語と字形の異なる 44 文字)、全角スペース、句読点重複、和文中の半角カンマ・記号、連続空白、行末空白、タブ、TODO 類
- 構造検査: frontmatter 12 件(必須項目がすべて揃い日付形式 YYYY-MM-DD)、記事と図 12 枚が双方向で 1 対 1、見出しレベルのジャンプ/重複なし、インデックス一覧は `getCollection` の自動生成、README の記載数(チュートリアル 6 本 + 事例 6 本 / 図 12 枚)は実装と一致、title と description は長すぎていない
- 結果: 文字の誤りは 0 件。検出 108 件すべて誤検知と判定(ラベル直後の `図:` 等、`付与` に含まれる `与`、コードフェンス内のタブ、`lng,lat` のように意図したカンマ、PEP8 のインラインコメント前の 2 スペース)
- ビルド・配信: `rm -rf dist .astro` から 17 ページ再生成。`dist` 内の内部リンク 129 本がすべて解決、公開 URL 17 ページ + 図 12 枚がすべて 200
- 既知の残件(未修正): 追跡ファイル 34 個が末尾改行なし。これはリポジトリ作成時からの状態なので、今回は記事 1 本(ユーザー修正分)のみ末尾改行あり。揃える場合はファイル数が増えるため別途判断する
- 参考: 繁体字と簡体字は字形が近いだけで日本語の文脈とは矛盾しないため誤検知が多くなる。機械スキャンで出た 1 件ずつを文脈で確認し、確定したものを修正する運用が有効
