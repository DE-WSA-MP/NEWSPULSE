# 📰 NewsPulse

## Multi-Source News Intelligence & Trend Analysis Platform

NewsPulse is a multi-source news intelligence and trend analysis platform developed as a Web Scraping and APIs mini-project.

The system collects news and current-event information from multiple online sources, processes and integrates the acquired data, identifies topics and trends, and presents the results through an interactive Streamlit dashboard.

---

## 📌 Project Overview

News and current-event information is available across different websites and APIs. However, information obtained from different sources can have different structures, formats, and fields.

NewsPulse provides a common pipeline for acquiring and processing information from multiple sources.

The system currently collects data from:

- **NASA Recently Published**
- **Wikipedia Current Events**
- **Hacker News API**

The acquired records are converted into a common structure and processed through cleaning, validation, topic classification, deduplication, integration, and trend analysis before being displayed on the dashboard.

---

## 🎯 Objectives

The main objectives of NewsPulse are:

1. Acquire news and current-event data from multiple online sources.
2. Demonstrate web scraping using Python.
3. Demonstrate REST API-based data acquisition.
4. Clean and normalize data obtained from different sources.
5. Validate acquired records before further processing.
6. Classify or extract topics associated with news records.
7. Remove duplicate records using hash-based data structures.
8. Integrate data from multiple sources into a common dataset.
9. Analyze basic trends and frequently occurring keywords.
10. Present the processed information through an interactive dashboard.
11. Allow users to refresh the dashboard with newly acquired data.

---

## 🔄 System Workflow

```text
                    User
                      │
                      ▼
              NewsPulse Dashboard
                      │
                      ▼
              Data Acquisition
             ┌────────┼─────────┐
             │        │         │
             ▼        ▼         ▼
           NASA   Wikipedia   Hacker News
          Scraper   Scraper      API
             │        │         │
             └────────┼─────────┘
                      ▼
                Data Integration
                      │
                      ▼
                   Cleaning
                      │
                      ▼
              Topic Classification
                      │
                      ▼
                  Validation
                      │
                      ▼
                Deduplication
                      │
                      ▼
              Final Integration
                      │
                      ▼
                Trend Analysis
                      │
                      ▼
             Interactive Dashboard
