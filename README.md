# ESRS E1 Climate Disclosure Assistant (RAG Pipeline)

## Overview
This project is a Retrieval-Augmented Generation (RAG) architecture designed to automate the alignment of corporate data with the European Sustainability Reporting Standards (ESRS) E1 standard. It functions as a Knowledge Assistant to help sustainability teams navigate complex regulatory requirements without relying on expensive or privacy invasive cloud APIs.

By utilizing localized, lightweight AI models, this project aligns with sustainable AI principles - reducing computational overhead and the associated carbon footprint while delivering audit-grade traceability for CSRD compliance.

## Key Features

* **Deterministic Document Parsing:** Utilizes `PyMuPDF` and regular expressions to ingest 320+ pages of complex legal PDFs. It employs a coordinate-based filtering system (y-axis thresholds) to strip structural noise (headers/footers) and logically partitions text by Disclosure Requirements (DRs) and Application Requirements (ARs).
* **Structured Metadata Indexing:** Parses regulatory text into a structured JSON schema, preserving vital document provenance (Source, Page, Section, Type) to ensure 100% traceability.
* **Semantic Retrieval Engine:** Uses a persistent `ChromaDB` instance and the `all-MiniLM-L6-v2` embedding model to perform cosine similarity searches, finding conceptual matches rather than relying on brittle keyword searches.
* **Grounded Local Generation:** Employs a local `Phi-3 Mini` model (3.8B parameters) constrained by strict system prompting to prevent hallucination. The model generates concise summaries based *only* on the retrieved context.

## Architecture Pipeline
1.  **Ingestion:** Raw PDF -> PyMuPDF Coordinate Filter -> Regex State Machine -> JSON Array.
2.  **Storage:** JSON -> `all-MiniLM-L6-v2` Embeddings -> ChromaDB Vector Index.
3.  **Retrieval:** User Query -> Embedding -> Cosine Similarity Search (Top-$k$) -> Relevant Context.
4.  **Generation:** Context + Query -> Grounded Prompt -> Local Phi-3 Mini -> Traceable Output.

## Installation

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) (installed and running locally to serve the LLM)

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/ykande1/esrs-climate-assistant.git](https://github.com/ykande1/esrs-climate-assistant.git)
   cd esrs-climate-assistant

   
## Feature Calendar

| **Issue** | **Due date** | |
| --------- | ------------ | -- |
| [Implement Data Preparation Pipeline](https://github.com/ykande1/JuniorIndependentStudy/issues/1) | Feb 26, 2026 | |
| [Develop Document Chunking Logic](https://github.com/ykande1/JuniorIndependentStudy/issues/2) | Feb 26, 2026 | |
| [Setup Vector Database](https://github.com/ykande1/JuniorIndependentStudy/issues/3) | Feb 26, 2022 | |
| [Build Semantic Retrieval Mechanism (Search Tool)](https://github.com/ykande1/JuniorIndependentStudy/issues/4) | March 6, 2026 | |
| [Design Grounded System Prompt](https://github.com/ykande1/JuniorIndependentStudy/issues/5) | March 6, 2026 | |
| [Integrate the RAG Pipeline](https://github.com/ykande1/JuniorIndependentStudy/issues/7) | March 13, 2026 | |
| [Build Streamlit Chat Interface](https://github.com/ykande1/JuniorIndependentStudy/issues/8) | March 26, 2026 | |
| [Implement Response & Citation Display](https://github.com/ykande1/JuniorIndependentStudy/issues/9) | March 26, 2026 | |
| [Develop Session Management](https://github.com/ykande1/JuniorIndependentStudy/issues/10) | April 2, 2026 | |
| [Automated PDF Parsing (Stretch Goal)](https://github.com/ykande1/JuniorIndependentStudy/issues/11) | if time permits | |
| [PDF Viewer (Stretch Goal)](https://github.com/ykande1/JuniorIndependentStudy/issues/12) | if time permits | |
| [Loading Bar (Stretch Goal)](https://github.com/ykande1/JuniorIndependentStudy/issues/13) | if time permits | |
| [Extend to other ESRS Standards (Stretch Goal)](https://github.com/ykande1/JuniorIndependentStudy/issues/13) | if time permits | |
