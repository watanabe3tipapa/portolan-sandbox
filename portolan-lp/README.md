# Portolan LP

AIが直接読める空間インフラ「Portolan」のランディングページ

## 概要

地理空間データを「AIが直接読める形で」公開するための新しいオープン仕様「Portolan」を紹介するランディングページです。

## 開発環境

```sh
npm install
npm run dev
```

## ビルド

```sh
npm run build
```

## デプロイ

GitHub Pagesに自動デプロイされます。手動でデプロイする場合：

```sh
npm run deploy
```

## プロジェクト構造

```text
/
├── public/
│   └── favicon.svg
├── src
│   ├── layouts
│   │   └── Layout.astro
│   └── pages
│       └── index.astro
├── .github/workflows/
│   └── deploy.yml
└── package.json
```

## 参考

- [Portolan 仕様](https://portolan.org)
- [Astro ドキュメント](https://docs.astro.build)
