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
- 日英 2 言語の README でプロジェクトの入口を整える(現行 v0.1.0)

## 決定事項

1. **ポートフォリオ構成**: ルートに `Portolan_要約.html`(GeoAI 第16回 要約)・LP 用 ASTRO プロジェクト(`portolan-lp/`)を共存。構想は本ファイル(DEV-MEMO.md)の「構想」節に集約
2. **LP は ASTRO(basics テンプレート)で構築** → 静的出力で GitHub Pages にデプロイ
3. **デプロイは GitHub Actions**(`deploy.yml`)に一本化。main への push で自動ビルド・公開
4. **チュートリアルはコンテンツコレクション(`tutorial`)で管理**。番号(order)付きで学習順を明示
5. **特集コーナーはコンテンツコレクション(`feature`)で管理**。Google Maps×OSM 連携・共通プロトコル・実証デモ・Colab MCP server を収録
6. README は okf-seedling に倣って **日英 2 版**(メインは日本語)
7. **ライセンスは MIT**。LICENSE ファイルをリポジトリ配布(okf-seedling と同形式)

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
    │   ├── content/
    │   │   ├── tutorial/            # 5 本(order 0〜4)
    │   │   └── feature/             # 4 本
    │   ├── layouts/
    │   │   └── Layout.astro         # 日本語ヘッダ・文字セット
    │   └── pages/
    │       ├── index.astro          # LP(ヒーロー・特徴・チュートリアル・特集・CTA)
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