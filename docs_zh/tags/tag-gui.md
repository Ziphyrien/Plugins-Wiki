# 📋称号 GUI (Tag GUI)

你可以使用 `/prefix opengui` 打开称号 GUI，玩家需要 `mythicprefixes.opengui` 权限才能使用它。

你可以在 `config.yml` 文件的 `prefix-item-slots` 选项中设置称号显示物品的槽位。

## 标题更新 - <mark style="color:red;">付费版，需要 Packetevents</mark>

你可以在选择称号 GUI 的标题中使用 {now} 和 {max} 占位符。

```yaml
choose-prefix-gui:
  # 你可以使用 {max} 显示最大页数，{now} 显示当前页数。需要启用标题更新才能在打开 GUI 后更新这些占位符。
  title: 'Choose your prefix {now}/{max}' # 在这里使用占位符。
  # 仅限付费版，如果启用，可以更新 GUI 标题中使用的动态值。
  title-update:
    # 需要 Packetevents。
    enabled: true # <--- 将其设置为 true
    resend-items-pack: false
```

## 过滤器 <mark style="color:red;">- 付费版</mark>

你可以通过以下格式添加过滤器物品：

```yaml
  filter-item:
    # 设置为 -1 以隐藏。
    slot: 47
    material: ANVIL
    name: '&bFilter'
    lore:
      - '&7Filter: {filter}'
    placeholder:
      all: '&aALL'
      using: '&cUSING'
      can-use: '&dCan Use'
```

## 自定义物品

你可以通过以下格式添加自定义物品：

```yaml
  custom-item:
    49: # 代表槽位
      material: SPAWNER
      name: '&4Unequip All tags'
      lore:
        - '&cClick to unequip.'
      actions:
        1:
          type: removeall
      bedrock:
        extra-line: '&fThis can not rollback!'
    53: # 代表槽位
      material: BARRIER
      name: '&cClose'
      lore:
        - '&cClick to close this menu.'
      actions:
        1:
          type: close
```

## 基岩版 <mark style="color:red;">- 付费版</mark>

这允许基岩版玩家显示表单 UI 而不是 Java 菜单。像这样：

<figure><img src="https://2999812483-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F3m8mzEiFIjMyc4GHSsws%2Fuploads%2FuLDjTb06Cy9JY6VAUmfZ%2F%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-02-02%20223508.png?alt=media&#x26;token=f0ab1d50-050c-49bd-8eb2-333a32d85313" alt=""><figcaption></figcaption></figure>

```yaml
  # 仅限付费版
  bedrock:
    enabled: true
    # 支持的值: FLOODGATE, UUID
    check-method: FLOODGATE
```

### 要求 <a href="#requirements" id="requirements"></a>

* 你的 Spigot 服务器中**必须安装** Geyser 和 Floodgate。如果你使用的是 BungeeCord 代理，你需要在后端服务器和代理服务器中都安装它们。
* 你必须将 Geyser 的 `auth-type` 设置为 **`floodgate`**。
* 如果你使用的是 BungeeCord，你需要仔细按照 [这些步骤](https://wiki.geysermc.org/floodgate/setup/) 在后端服务器中设置 floodgate。

> [!NOTE]
> 如果你的服务器正确安装并配置了 floodgate，当 UltimateShop（注：此处原文可能是复制粘贴错误，应为 MythicPrefixes）开始运行时，控制台会提示 `Hooking into floorgate`。如果没有出现此提示，但你坚持认为你的服务器有 floodgate，那么很可能是你意外下载了插件的免费版本。


* 所有基岩版玩家都将使用新 UI。如果没有，你可以尝试在 `config.yml` 中将 `choose-prefix-gui.bedrock.check-method` 选项值从 **FLOODGATE** 设置为 **UUID**。
* 基岩版 UI 是自动生成的，不需要任何手动修改。

目前，我们支持基岩版按钮或前缀配置的这些选项：

* icon: 此按钮的图标，格式为 `path;;<image path>` 或 `url;;<image url>`。图片路径是基岩版纹理路径，而不是你的插件路径，例如：`path;;textures/blocks/stone_granite.png`。如果你不知道这是什么，请忽略它，不要问我。
* hide: 对基岩版玩家隐藏按钮。
* extra-line: 在基岩版按钮上显示第二行，支持产品的 `{buy-price}` 和 `{sell-price}` 占位符。
