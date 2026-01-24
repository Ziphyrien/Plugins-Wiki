---
title: Cross-Server
sidebar:
  order: 9
---

This guide describes how to use CoinsEngine on multiple servers connected to the same MySQL database.

Balance sharing and synchronization depends on the `Column_Name` and `Synchronized` currency settings.

:::danger
`Sync_Interval` value in the **engine.yml** must be **enabled** (≥ 1) on **all** servers with balance synchronization!
:::

## Scenario #1

Currency: **money.yml**

Same balance on all servers.

* Server A: `Column_Name: money`, `Synchronized: true`
* Server B: `Column_Name: money`, `Synchronized: true`
* Server C: `Column_Name: money`, `Synchronized: true`

## Scenario #2

Currency: **money.yml**

Different balance on all servers.

* Server A: `Column_Name: money_a`, `Synchronized: false`
* Server B: `Column_Name: money_b`, `Synchronized: false`
* Server C: `Column_Name: money_c`, `Synchronized: false`

## Scenario #3

Currency: **gems.yml**

Different balance on server A, shared balance on servers B and C.

* Server A: `Column_Name: gems_a`, `Synchronized: false`
* Server B: `Column_Name: gems_shared`, `Synchronized: true`
* Server C: `Column_Name: gems_shared`, `Synchronized: true`
