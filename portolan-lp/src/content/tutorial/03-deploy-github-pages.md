---
title: "3. Deploy — GitHub Pages で公開する"
description: "コレクションと LP を GitHub Pages に配置し、世界に向けて公開する方法を学びます。"
order: 3
pubDate: 2026-09-11
---

## GitHub Pages で静的サイトを公開

Portolan は静的ファイル（GeoParquet・PMTiles・collection.json・Markdown）として公開できるため、GitHub Pages との相性が抜群です。GitHub アカウントさえあれば追加費用なしで公開できます。

## 公開の流れ（GitHub Actions 利用）

1. リポジトリを作成（例: `watanabe3tipapa/portolan-sandbox`）
2. `main` ブランチへ push
3. リポジトリ設定 → Pages → Source を **GitHub Actions** に設定
4. push のたびに自動ビルド・デプロイ

### Pages 設定の手順

```text
GitHub リポジトリ → Settings → Pages
  → Source: "GitHub Actions" を選択
```

ここで「GitHub Actions」を選ぶと、リポジトリ内のワークフローが `actions/deploy-pages` でデプロイできるようになります。

## 本プロジェクトのワークフロー

本リポジトリでは `.github/workflows/deploy.yml` により ASTRO の `dist/` を GitHub Pages へ自動デプロイしています。構成は次のとおりです。

```text
push を main に検知
  └─ build ジョブ: npm install → npm run build → dist/ を artifact 化
  └─ deploy ジョブ: actions/deploy-pages で公開
```

要点:

- `permissions: pages: write, id-token: write` が必要
- `actions/upload-pages-artifact` でビルド成果物をアップロード
- `actions/deploy-pages` が本番公開を実行
- GitHub Pages は Actions ソースの場合、`environment: github-pages` が自動的に作られる

## ASTRO プロジェクトでの設定（この LP の実装例）

`astro.config.mjs` で GitHub Pages の URL を指定します。サブディレクトリ公開の場合は `base` にリポジトリ名を入れます。

```js
export default defineConfig({
  site: 'https://watanabe3tipapa.github.io',
  base: '/portolan-sandbox',
  output: 'static',
});
```

この設定があると、ビルド時にリンクが `/portolan-sandbox/...` として生成されます。リポジトリ名で公開する場合、**base を忘れると画像やリンクが崩れる**ので注意してください。

## 公開 URL の確認

デプロイ後、次の URL で確認できます。

- サイト: `https://<username>.github.io/<repo>/`
- 例: https://watanabe3tipapa.github.io/portolan-sandbox/

## コレクションも GitHub に置く

Portolan のコレクション（`collection.json` + データ）も GitHub リポジトリに置けます。`raw.githubusercontent.com` や Pages で静的配信すれば、サーバー運用なしで公開できます。

```text
https://<username>.github.io/my-collection/collection.json   ← 公開 URL
```

## トラブルシューティング

| 症状 | 原因と対処 |
|---|---|
| リンク・画像が 404 | `base` 未設定 → `astro.config.mjs` で `base: '/<repo>'` を設定 |
| ワークフローが実行されない | GitHub Actions が有効か確認、`permissions` に `pages: write` を追加 |
| Pages が 403 | Pages 設定の Source が「GitHub Actions」になっているか確認 |
| 初回デプロイが遅い | ビルドとデプロイで数分かかる。Actions タブのログを確認 |

## 次のステップ

次のステップ: [Google Colaboratory と連携する](../04-google-colab/)