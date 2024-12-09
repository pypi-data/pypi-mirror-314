# langchain-chroma

This package contains the LangChain integration with HanaDB.

## Installation

```bash
pip install -U langchain-hana-prototype
```

## Usage

The `HanaDB` class exposes the connection to the HanaDB vector store. The integration enables seamless utilization of SAP HANA's advanced vector processing capabilities for efficient storage and retrieval

```python
from langchain_hana_prototype import HanaDB

embeddings = ... # use a LangChain Embeddings class

connection = ...

vectorstore = HanaDB(embeddings=embeddings, connection=connection)
```