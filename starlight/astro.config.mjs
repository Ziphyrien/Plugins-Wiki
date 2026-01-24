// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';
import icon from 'astro-icon';
import starlightSidebarTopics from 'starlight-sidebar-topics';
import { sidebar, topics } from './sidebar.mjs';

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      plugins: [
        starlightSidebarTopics(topics),
      ],
      title: 'Plugins Wiki',
      defaultLocale: 'root',
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-CN',
        },
        en: {
          label: 'English',
          lang: 'en',
        },
      },
      components: {
        PageTitle: './src/components/PageTitle.astro',
        PageFrame: './src/components/PageFrame.astro',
        Sidebar: '@astrojs/starlight/components/Sidebar.astro',
      },
      customCss: ['./src/styles/global.css'],
      social: [
        {
          label: 'GitHub',
          href: 'https://github.com/Ziphyrien/Plugins-Wiki',
          icon: 'github',
        },
      ],
    }),
    icon(),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
