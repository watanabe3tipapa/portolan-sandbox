# DEV-MEMO.md

portolan-sandbox 開発メモ。「AI が直接読める空間インフラ Portolan」を多くの人に身近に使ってもらうための手法を開拓する実験リポジトリ。ASTRO で構築した LP とチュートリアル・特集ページを GitHub Pages で公開する。

## 構想(PLAN.md から移行)

- できるだけ多くの人々が Portolan を身近に使えるようにするための手法の開拓
- Google アカウントだけで全ての措置(認証・デプロイなど)に対応したい
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

frontmatter: `title` / `description` / `order`(number) / `pubDate`(date)

### feature(特集、新しい順)

| id | タイトル |
|---|---|
| colab-mcp-server | Colab MCP server に期待できる機能 |
| gmaps-osm-interop | Google Maps × OpenStreetMap — データ連携 |
| common-protocols | 共通プロトコルの用例 — STAC・GeoParquet・PMTiles |
| helsinki-demo | ケーススタディ — OGC Connect Helsinki デモ |

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

## 今後やること(仮)

- LICENSE の決定(MIT 検討中)→ README / バッジの反映
- 「Google アカウントだけで完結する認証・デプロイ」検証(Colab / Colab MCP server、本ファイル「構想」節と連動)
- tutorial 記事の内容充実と、特集記事の更新