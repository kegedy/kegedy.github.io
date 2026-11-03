// @ts-check
// Site configuration. See https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Kevin Egedy',
  tagline: 'Circuit design projects: schematics, layouts, and analysis',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // User site: served from https://kegedy.github.io/
  url: 'https://kegedy.github.io',
  baseUrl: '/',
  organizationName: 'kegedy',
  projectName: 'kegedy.github.io',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  customFields: {
    // Public URL of the kweb server (Hugging Face Space). Used by <LayoutViewer>.
    // Format: https://<hf-username>-<space-name>.hf.space
    // Override for local preview: KWEB_URL=http://localhost:8765 npm start
    kwebUrl: process.env.KWEB_URL ?? 'https://kegedy-gds-viewer.hf.space',
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: 'projects',
          sidebarPath: './sidebars.js',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.47/dist/katex.min.css',
      type: 'text/css',
      crossorigin: 'anonymous',
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Kevin Egedy',
        logo: {
          alt: 'Logo',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'projectsSidebar',
            position: 'left',
            label: 'Projects',
          },
          {
            href: 'https://github.com/kegedy',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `Copyright © ${new Date().getFullYear()} Kevin Egedy. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'tcl'],
      },
    }),
};

export default config;
