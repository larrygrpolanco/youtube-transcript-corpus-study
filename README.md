# YouTube Academic Spoken English Corpus (YASEC)

## Overview
This repository contains the scripts and tools used to create and analyze the YouTube Academic Spoken English Corpus (YASEC), a 58-million-word corpus of academic spoken discourse sourced from YouTube. The corpus was constructed from 9,430 video transcripts categorized into four main academic disciplines: engineering, humanities and arts, science and math, and social sciences.

## Research Abstract
Vocabulary plays a key role in understanding academic spoken English, and YouTube grants students access to numerous academic events. However, research into the lexical demands of academic English on YouTube remains sparse. This study analyzes the lexical profile of a 58-million-word corpus of academic spoken discourse on YouTube. The YouTube Academic Spoken English Corpus, created for this study, was constructed from 9,430 video transcripts categorized into four main academic disciplines (engineering, humanities and arts, science and math, and social sciences). Examined were (a) the lexical demand of the corpus, (b) variations in the lexical demand across each discipline, and (c) the coverage of the Academic Spoken Word List (ASWL) in this corpus and its sub corpora. The results revealed that to achieve 90% comprehension of this corpus, learners must have knowledge of the 2,000 most frequent word families. Knowledge of 4,000 and 8,000 word families are required to attain more than 95% and 98% coverage, respectively. Discussed are the implications of these findings for EAP pedagogy and viability of streaming media and language education.

**Keywords**: Academic spoken English; corpus; lexical coverage; OpenCourseWare; vocabulary; word list

## Repository Structure

### Data Collection Tools
- **Transcript Scrapper.py**: Extracts transcripts from YouTube videos using video IDs
- **Comment Scrapper.py**: Collects comments from YouTube videos for analysis
- **Large/Small YouTube Table.py**: Scripts for organizing and processing large datasets of YouTube videos
- **Transcript_Checker.py**: Verifies availability and quality of transcripts
- **check_transcript_availability.py**: Checks if transcripts are available for given video IDs
- **check_transcript_type.py**: Determines if transcripts are auto-generated or manual

### Data Processing Tools
- **Text Combiner.py**: Combines multiple transcript files into a single corpus file
- **Transcript Transfer.py**: Transfers and organizes transcript files
- **List Formatter.py**: Formats word lists for analysis
- **Word List Converter**: Tools for converting between different word list formats
  - Used for processing the Academic Spoken Word List (ASWL)

### Sample Data
- **Analysis Sample Documentary**: Contains sample transcripts and comments from documentary videos
- **Analysis Sample vlog shorts**: Contains sample transcripts from vlog and short-form videos

## Key Findings
- Knowledge of the 2,000 most frequent word families is required for 90% comprehension
- 4,000 word families are needed for 95% coverage
- 8,000 word families are required for 98% coverage
- Lexical demands vary across academic disciplines

## Usage
The scripts in this repository can be used to:
1. Collect transcripts from YouTube videos using video IDs
2. Process and organize transcript files for corpus analysis
3. Analyze the lexical profile of YouTube academic content
4. Compare coverage of word lists across different academic disciplines

## Requirements
Most scripts require:
- Python 3.6+
- youtube-transcript-api
- google-api-python-client
