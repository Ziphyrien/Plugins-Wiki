---
title: Requirements
sidebar:
  order: 2
---

## Java Version

* Basic Requirement: **Java9+**
* **Java 17+** is <mark style="color:red;">recommended</mark>. Java17 and above versions are recommended, but plugins are compiled using **Java9**, so theoretically, you only need Java8 or higher versions.

## Server Software

* **Paper** and its downstream forks are <mark style="color:red;">recommended</mark>. When the plugin detects that your server software is Paper, it will enable some features that are only available in Paper, some of which can provide subtle performance improvements.
* **Folia** server also supported. Please note: Folia's support is in the <mark style="color:red;">early testing stage</mark> and may be released in official versions or removed in the future. This support is not a guarantee.

## Server Version

* The plugin theoretically supports any version between **1.14** and **1.21.7**.
* Obviously, supporting so many versions is not an easy task. It is impossible for the author to test all versions between 1.14 and 1.21.7 every time the plugin is updated. If you encounter errors while using a certain version, <mark style="color:red;">please join our Discord feedback</mark>.

## A chat/tab/scoreboard and PlaceholderAPI plugin if you want to display prefix (tag)

* MythicPrefixes is just a **tag manager** plugin, <mark style="color:red;">we do not auto add prefix at chat/tab/scoreboard</mark>, you have to use other plugins like **TAB**, and use our [Placeholders](https://mythicprefixes.superiormc.cn/info/compatibility) in them to display the tag.
