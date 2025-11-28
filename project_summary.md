# 📊 Portfolio Agenti AI "Boring B2B"

Ecco una sintesi degli agenti sviluppati (e in sviluppo), con tecnologie chiave e ipotesi di pricing per un modello Micro-SaaS o Lifetime Deal (LTD).

## 🟢 Fase 1: Le 5 Idee Originali (Già su GitHub)

Questi agenti sono stati sviluppati come MVP completi con interfaccia Streamlit.

| Agente | Descrizione | Tech Stack | Target | Pricing Ipotesi |
| :--- | :--- | :--- | :--- | :--- |
| **1. Customer Support SaaS** | Chatbot RAG che risponde da knowledge base. | **RAG**, LangChain, FAISS, OpenAI/Ollama | SaaS B2B | **€49/mese** (fino a 1000 chat) |
| **2. Lead Enrichment** | Arricchisce liste aziende con dati dal web. | **Scraping** (Google), LLM Extraction | Marketing Agencies | **€99/mese** o €0.50/lead |
| **3. Legal Translation** | Traduzione contratti con glossario forzato. | **Prompt Engineering**, Glossary Injection | Studi Legali | **€29/mese** + consumo token |
| **4. Financial Reconciliation** | Confronta CSV (Banca vs Stripe) e trova discrepanze. | **Pandas** (Deterministico), Streamlit | Commercialisti | **€149 LTD** (Licenza singola) |
| **5. Real Estate Review** | Analizza contratti affitto (PDF) per rischi e date. | **PDF Parsing**, LLM Analysis | Agenti Immobiliari | **€19/report** o €49/mese |

---

## 🟡 Fase 2: Le Nuove Idee "Boring B2B" (Mike Hill Framework)

Questi agenti sono focalizzati su problemi "noiosi" ma ad alto valore economico.

| Agente | Descrizione | Tech Stack | Target | Pricing Ipotesi |
| :--- | :--- | :--- | :--- | :--- |
| **6. RFP Responder** | Scrive risposte a bandi usando vecchie proposte. | **RAG Avanzato**, Vector DB (Chroma), Docx | Consulenti / Grandi Aziende | **€299/mese** (Risparmia settimane di lavoro) |
| **7. Label Compliance** | Controlla etichette alimentari (Allergeni, Font). | **Vision AI** (GPT-4o), Image Processing | Produttori Alimentari | **€99/mese** o €10/check |
| **8. Logistics Dispatcher** | Risponde a email "Dov'è il mio pacco?". | **NLP Extraction**, Mock ERP Lookup | E-commerce / Logistica | **€0.20/ticket** risolto |
| **9. Invoice GL Coder** | Assegna codici contabili a fatture PDF. | **Hybrid** (Lookup + AI Fallback), PDF | Studi Commercialisti | **€29/mese** per utente |
| **10. Construction BOM** *(In Sviluppo)* | Estrae lista materiali da capitolati edili. | **Entity Extraction**, Table Parsing | Imprese Edili | **€199 LTD** o €49/mese |

## 💡 Analisi Tecnologica Globale
*   **Frontend**: Tutti usano **Streamlit** per rapidità e pulizia.
*   **Backend**: Python puro + **LangChain** come orchestratore.
*   **AI Models**:
    *   *Testo*: GPT-3.5-Turbo (veloce/economico) o GPT-4 (complesso).
    *   *Vision*: GPT-4o (necessario per Agente 7).
    *   *Locale*: Predisposizione per **Ollama** (Llama 3) per privacy (Agente 1, 3, 6).
*   **Dati**:
    *   *Vettoriali*: FAISS / ChromaDB (locali, zero costi cloud).
    *   *Tabellari*: Pandas (per precisione matematica in Agente 4 e 8).

## 🚀 Valore Totale Stimato
Se lanciati come suite o singolarmente, questo portfolio copre nicchie diverse riducendo il "Platform Risk".
Il potenziale di fatturato combinato (MRR) per questi 10 micro-SaaS, con marketing adeguato, supera ampiamente l'obiettivo di **$100k/anno**.
