import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const tutorial = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/tutorial' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number(),
    pubDate: z.date(),
  }),
});

const feature = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/feature' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
  }),
});

export const collections = { tutorial, feature };