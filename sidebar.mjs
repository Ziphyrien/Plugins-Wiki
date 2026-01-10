export const sidebar = [
  {
    label: '导航说明',
    translations: { 'en': 'Navigation' },
    link: '/plugins',
  },
  {
    label: 'MythicPrefixes',
    translations: { 'en': 'MythicPrefixes' },
    items: [
      {
        label: '开始',
        translations: { 'en': 'Start Here' },
        items: [
          { label: '🎉欢迎', translations: { 'en': '🎉Welcome' }, link: '/mythicprefixes/welcome' },
        ],
      },
      {
        label: '信息',
        translations: { 'en': 'Info' },
        autogenerate: { directory: 'mythicprefixes/info' },
      },            
      {
        label: '格式',
        translations: { 'en': 'Format' },
        autogenerate: { directory: 'mythicprefixes/format' },
      },   
      {
        label: '称号',
        translations: { 'en': 'Tags' },
        autogenerate: { directory: 'mythicprefixes/tags' },
      },                     
      {
        label: '特性',
        translations: { 'en': 'Features' },
        autogenerate: { directory: 'mythicprefixes/features' },
      }
    ],
  },
  {
    label: 'CoinsEngine',
    translations: { 'en': 'CoinsEngine' },
    items: [
      {
        label: '开始',
        translations: { 'en': 'Start Here' },
        items: [
          { label: '🎉欢迎', translations: { 'en': '🎉Welcome' }, link: '/coinsengine/welcome' },
        ],
      },
      {
        label: '特性',
        translations: { 'en': 'Features' },
        autogenerate: { directory: 'coinsengine/features' },
      },
      {
        label: '钩子',
        translations: { 'en': 'Hooks' },
        autogenerate: { directory: 'coinsengine/hooks' },
      },
      {
        label: '占位符',
        translations: { 'en': 'Placeholders' },
        autogenerate: { directory: 'coinsengine/placeholders' },
      },
      {
        label: '指令',
        translations: { 'en': 'Commands' },
        link: '/coinsengine/commands',
      },
      {
        label: '权限',
        translations: { 'en': 'Permissions' },
        link: '/coinsengine/permissions',
      },
      {
        label: '开发者API',
        translations: { 'en': 'Developer API' },
        link: '/coinsengine/developer-api',
      },
    ],
  },
];

export const topics = [
  {
    label: '开始',
    link: '/plugins',
    icon: 'rocket',
    items: [sidebar[0]],
  },
  {
    label: 'MythicPrefixes',
    link: '/mythicprefixes/welcome',
    icon: 'ri:price-tag-3-line',
    items: sidebar[1].items,
  },
  {
    label: 'CoinsEngine',
    link: '/coinsengine/welcome',
    icon: 'ri:coins-line',
    items: sidebar[2].items,
  },
];
