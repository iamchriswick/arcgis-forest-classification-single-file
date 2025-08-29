---
title: Import Fields
description: Documents field definitions and data structure mappings
author: iamchriswick
version: 1.0.1
created: 2025-08-25
updated: 2025-08-27 18:45:17
revision_notes: Updated header format and documentation structure
---

# Forest Classification Field Definitions

## **Age Data**

| Field Name      | Description           | Path                                            |
| --------------- | --------------------- | ----------------------------------------------- |
| `srrhogstaar`   | Harvest year          | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrhogstaar   |
| `srrtrealder`   | Stand age             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtrealder   |
| `srrtrealder_l` | Stand age lower bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtrealder_l |
| `srrtrealder_u` | Stand age upper bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtrealder_u |

## **Species Type**

| Field Name   | Description      | Path                                         |
| ------------ | ---------------- | -------------------------------------------- |
| `srrtreslag` | Dominant species | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreslag |

## **Biomass**

| Field Name | Description                             | Path                                       |
| ---------- | --------------------------------------- | ------------------------------------------ |
| `srrbmo`   | Above-ground biomass (t/ha)             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbmo   |
| `srrbmo_l` | Above-ground biomass lower bound (t/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbmo_l |
| `srrbmo_u` | Above-ground biomass upper bound (t/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbmo_u |
| `srrbmu`   | Below-ground biomass (t/ha)             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbmu   |
| `srrbmu_l` | Below-ground biomass lower bound (t/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbmu_l |
| `srrbmu_u` | Below-ground biomass upper bound (t/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbmu_u |

## **Volume**

| Field Name   | Description                           | Path                                         |
| ------------ | ------------------------------------- | -------------------------------------------- |
| `srrvolmb`   | Volume over bark (m³/ha)              | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrvolmb   |
| `srrvolmb_l` | Volume over bark lower bound (m³/ha)  | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrvolmb_l |
| `srrvolmb_u` | Volume over bark upper bound (m³/ha)  | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrvolmb_u |
| `srrvolub`   | Volume under bark (m³/ha)             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrvolub   |
| `srrvolub_l` | Volume under bark lower bound (m³/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrvolub_l |
| `srrvolub_u` | Volume under bark upper bound (m³/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrvolub_u |

## **Height**

| Field Name    | Description                 | Path                                          |
| ------------- | --------------------------- | --------------------------------------------- |
| `srrmhoyde`   | Mean height (m)             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrmhoyde   |
| `srrmhoyde_l` | Mean height lower bound (m) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrmhoyde_l |
| `srrmhoyde_u` | Mean height upper bound (m) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrmhoyde_u |
| `srrohoyde`   | Top height (m)              | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrohoyde   |
| `srrohoyde_l` | Top height lower bound (m)  | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrohoyde_l |
| `srrohoyde_u` | Top height upper bound (m)  | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrohoyde_u |

## **Site Index**

| Field Name   | Description          | Path                                         |
| ------------ | -------------------- | -------------------------------------------- |
| `srrbonitet` | Site index (bonitet) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrbonitet |

## **Diameter**

| Field Name            | Description                      | Path                                                  |
| --------------------- | -------------------------------- | ----------------------------------------------------- |
| `srrdiammiddel`       | Mean DBH (cm)                    | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrdiammiddel       |
| `srrdiammiddel_l`     | Mean DBH lower bound (cm)        | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrdiammiddel_l     |
| `srrdiammiddel_u`     | Mean DBH upper bound (cm)        | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrdiammiddel_u     |
| `srrdiammiddel_ge8`   | Mean DBH ≥ 8 cm (cm)             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrdiammiddel_ge8   |
| `srrdiammiddel_ge8_l` | Mean DBH ≥ 8 cm lower bound (cm) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrdiammiddel_ge8_l |
| `srrdiammiddel_ge8_u` | Mean DBH ≥ 8 cm upper bound (cm) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrdiammiddel_ge8_u |

## **Basal Area**

| Field Name     | Description                    | Path                                           |
| -------------- | ------------------------------ | ---------------------------------------------- |
| `srrgrflate`   | Basal area (m²/ha)             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrgrflate   |
| `srrgrflate_l` | Basal area lower bound (m²/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrgrflate_l |
| `srrgrflate_u` | Basal area upper bound (m²/ha) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrgrflate_u |

## **Tree Density**

| Field Name            | Description                           | Path                                                  |
| --------------------- | ------------------------------------- | ----------------------------------------------------- |
| `srrtreantall`        | Trees per hectare (all)               | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall        |
| `srrtreantall_l`      | Trees per hectare lower bound (all)   | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_l      |
| `srrtreantall_u`      | Trees per hectare upper bound (all)   | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_u      |
| `srrtreantall_ge8`    | Trees per hectare ≥ 8 cm DBH          | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge8    |
| `srrtreantall_ge8_l`  | Trees per hectare ≥ 8 cm lower bound  | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge8_l  |
| `srrtreantall_ge8_u`  | Trees per hectare ≥ 8 cm upper bound  | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge8_u  |
| `srrtreantall_ge10`   | Trees per hectare ≥ 10 cm DBH         | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge10   |
| `srrtreantall_ge10_l` | Trees per hectare ≥ 10 cm lower bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge10_l |
| `srrtreantall_ge10_u` | Trees per hectare ≥ 10 cm upper bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge10_u |
| `srrtreantall_ge16`   | Trees per hectare ≥ 16 cm DBH         | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge16   |
| `srrtreantall_ge16_l` | Trees per hectare ≥ 16 cm lower bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge16_l |
| `srrtreantall_ge16_u` | Trees per hectare ≥ 16 cm upper bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreantall_ge16_u |

## **Leaf Area Index**

| Field Name | Description                 | Path                                       |
| ---------- | --------------------------- | ------------------------------------------ |
| `srrlai`   | Leaf Area Index             | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrlai   |
| `srrlai_l` | Leaf Area Index lower bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrlai_l |
| `srrlai_u` | Leaf Area Index upper bound | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrlai_u |

## **Crown Coverage**

| Field Name    | Description        | Path                                          |
| ------------- | ------------------ | --------------------------------------------- |
| `srrkronedek` | Crown coverage (%) | Grid_8m_SR16_Dataset/Grid_8m_SR16_srrkronedek |

## **Elevation**

| Field Name  | Description           | Path                    |
| ----------- | --------------------- | ----------------------- |
| `elev_min`  | Minimum elevation (m) | Table_Grid_8m_ElevStats |
| `elev_mean` | Mean elevation (m)    | Table_Grid_8m_ElevStats |
| `elev_max`  | Maximum elevation (m) | Table_Grid_8m_ElevStats |

## **Soil Properties**

| Field Name | Description                  | Path                                     |
| ---------- | ---------------------------- | ---------------------------------------- |
| `markfukt` | Soil moisture classification | Grid_8m_AR5_Dataset/Grid_8m_AR5_markfukt |
| `artype`   | Soil type classification     | Grid_8m_AR5_Dataset/Grid_8m_AR5_artype   |
| `argrunnf` | Soil depth / foundation      | Grid_8m_AR5_Dataset/Grid_8m_AR5_argrunnf |

## **Location**

| Field Name | Description | Path             |
| ---------- | ----------- | ---------------- |
| `loc_long` | Longitude   | Grid_8m_Location |
| `loc_lat`  | Latitude    | Grid_8m_Location |
