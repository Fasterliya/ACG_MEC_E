# EU4 Mod 开发工具参考

## 1. 任务树 required_missions 编写规范

设 slot = x，position = y（均为正整数）。

对于位置 `(x, y)` 的任务，`required_missions` 中**仅允许**以下两种引用：

### 规则 1：同行前列
```
(x, y-n)   其中 n 为任意正整数，且 y-n > 0
```
即同一 slot 内、position 更小的任意任务。

### 规则 2：跨行上一级
```
(s, y-1)   其中 s ∈ {1, 2, 3, 4, 5}
```
即**任意 slot** 中、position 恰好为 `y-1` 的任务（不允许跳 position）。

### 合法示例
```
(3,8) requires (3,7) + (1,7)    ✅ (3,7)规则1, (1,7)规则2
(5,6) requires (5,5) + (4,5)    ✅ (5,5)规则1, (4,5)规则2
(4,3) requires (4,2) + (1,2)    ✅ (4,2)规则1, (1,2)规则2
(1,5) requires (1,3) + (1,4)    ✅ 同slot允许引多个前列
```

### 违规示例
```
(3,5) requires (3,4) + (1,3)    ❌ (1,3)的position=3 ≠ y-1=4
(2,6) requires (2,5) + (1,4)    ❌ (1,4)的position=4 ≠ y-1=5
(4,7) requires (4,6) + (1,5)    ❌ (1,5)的position=5 ≠ y-1=6
(1,5) requires (1,3) + (4,2)    ❌ (4,2)的position=2 ≠ y-1=4
```

---

## 2. 地理键值校验

### 游戏源路径

```
基础游戏地图:  F:\SteamLibrary\steamapps\common\Europa Universalis IV\map
Area 定义:     F:\SteamLibrary\steamapps\common\Europa Universalis IV\map\area.txt
Region 定义:   F:\SteamLibrary\steamapps\common\Europa Universalis IV\map\region.txt
```

### 快速验证命令 (PowerShell)

```powershell
# 验证 region 键值是否存在
Select-String -Path "F:\SteamLibrary\steamapps\common\Europa Universalis IV\map\region.txt" `
    -Pattern "carpathia_region|balkan_region|crimea_region"

# 验证 area 键值是否存在
Select-String -Path "F:\SteamLibrary\steamapps\common\Europa Universalis IV\map\area.txt" `
    -Pattern "alfold_area|slovakia_area|thrace_area"

# 列出所有 region 名称
Select-String -Path "F:\SteamLibrary\steamapps\common\Europa Universalis IV\map\region.txt" `
    -Pattern "_region =" | ForEach-Object { $_.Line.Trim() -replace ' \{.*', '' }

# 列出所有 area 名称
Select-String -Path "F:\SteamLibrary\steamapps\common\Europa Universalis IV\map\area.txt" `
    -Pattern "_area =" | ForEach-Object { $_.Line.Trim() -replace ' \{.*', '' }

# 批量校验 missions 文件中的所有 geokey
Select-String -Path ".\missions\*_missions.txt" -Pattern "_region|_area" |
    ForEach-Object { $_.Line.Trim() }
```

### 已知陷阱

| 常被误写的名称 | 正确的游戏键值 |
|---------------|---------------|
| `carpathian_region` | `carpathia_region` |
| `south_germany_region` | `south_german_region` |
| `pontic_steppe_region` | **不存在**，用 `crimea_region` |
| `austria_region` | **不存在**，奥地利诸省在 `south_german_region` |
| `pest_area` | **不存在**，用 `alfold_area` |
| `pozsony_area` | **不存在**，用 `slovakia_area` |
| `spis_area` | **不存在**，用 `transylvania_area` |
| `wien_area` | **不存在**，用 `austria_proper_area` |
| `constantinople_area` | **不存在**，用 `thrace_area` |

### 工作流

1. 设计任务树 → 确定目标地理区域
2. 在 `region.txt` / `area.txt` 中 grep 确认键值存在
3. 使用**游戏原生键值**写入 `_missions.txt`
4. 运行上方批量校验命令确认无误
