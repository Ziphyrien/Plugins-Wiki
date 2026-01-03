# 🎬动作格式 (Action Format)

## 可用占位符

* {world}
* {amount}
* {player\_x}
* {player\_y}
* {player\_z}
* {player\_pitch}
* {player\_yaw}
* {player}

## 添加称号 (Add Prefix)

```yaml
   actions:
     1:
       type: add_prefix
       prefix: example
```

## 移除称号 (Remove Prefix)

```yaml
   actions:
     1:
       type: remove_prefix
       prefix: example
```

## 移除所有 (Remove All)

移除所有已装备的称号。

```yaml
   actions:
     1:
       type: removeall
```

## 关闭 (Close)

关闭已打开的 GUI。

```yaml
   actions:
     1:
       type: close
```

## 声音 (Sound)

向玩家发送声音。

```yaml
    actions:
      1:
        type: sound
        sound: 'ui.button.click'
        volume: 1
        pitch: 1
```

## 消息 (Message)

向玩家发送消息，支持颜色代码。

```yaml
    actions:
      1:
        type: message
        message: 'Hello!'
```

## 公告 (Announcement)

向所有在线玩家发送消息，支持颜色代码。

```yaml
    actions:
      1:
        type: announcement
        message: 'Hello!'
```

## 效果 (Effect)

给予玩家药水效果。

```yaml
    actions:
      1:
        type: effect
        potion: BLINDNESS
        duration: 60
        level: 1
        ambient: true # 可选
        particles: true # 可选
        icon: true # 可选
```

## 传送 (Teleport)

将玩家传送到指定位置。

```yaml
    actions:
      1:
        type: teleport
        world: LobbyWorld
        x: 100
        y: 30
        z: 300
        pitch: 90 # 可选
        yaw: 0 # 可选
```

## 玩家命令 (Player Command)

让玩家执行命令。

```yaml
    actions:
      1:
        type: player_command
        command: 'tell Hello!'
```

## OP 命令 (Op Command)

让玩家以 OP 身份执行命令。

```yaml
    actions:
      1:
        type: op_command
        command: 'tell Hello!'
```

## 控制台命令 (Console Command)

让控制台执行命令。

```yaml
    actions:
      1:
        type: console_command
        command: 'op {player}'
```

## 生成原版生物 (Spawn vanilla mobs)

生成原版生物。

```yaml
    actions:
      1:
        type: entity_spawn
        entity: ZOMBIE
        world: LOBBY # 可选
        x: 100.0 # 可选
        y: 2.0 # 可选
        z: -100.0 # 可选
```

## 延迟 (Delay) <mark style="color:red;">- 付费版</mark>

让动作在 X tick 后运行。

```yaml
    actions:
      1:
        type: delay
        time: 50
        wait-for-player: true
        actions:
          1:
            type: entity_spawn
            entity: ZOMBIE
```

## 概率 (Chance) <mark style="color:red;">- 付费版</mark>

设置动作执行的概率，最高 100。50 意味着此动作有 50% 的概率执行。

```yaml
    actions:
      1:
        type: chance
        rate: 50
        actions:
          1:
            type: entity_spawn
            entity: ZOMBIE
```

## 随机 (Any) <mark style="color:red;">- 付费版</mark>

随机选择一个动作执行。

```yaml
    actions:
      1:
        type: any
        amount: 2
        actions:
          1:
            type: entity_spawn
            entity: ZOMBIE
          2:
            type: entity_spawn
            entity: SKELETON
          3:
            type: entity_spawn
            entity: WITHER
```
