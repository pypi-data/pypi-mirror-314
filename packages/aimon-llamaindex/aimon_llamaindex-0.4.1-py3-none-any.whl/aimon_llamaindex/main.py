import logging
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine

llm:OpenAI
retriever: VectorIndexRetriever
embedding_model: OpenAIEmbedding

## Returns nodes with embeddings and metadata
def generate_embeddings_for_docs(documents, embedding_model):

    # Using the LlamaIndex SentenceSplitter, parse the documents into text chunks.

    from llama_index.core.node_parser import SentenceSplitter

    text_parser = SentenceSplitter()

    text_chunks = []
    doc_idxs = []
    for doc_idx, doc in enumerate(documents):
        cur_text_chunks = text_parser.split_text(doc.text)
        text_chunks.extend(cur_text_chunks)
        doc_idxs.extend([doc_idx] * len(cur_text_chunks))

    ## Construct nodes from the text chunks.

    from llama_index.core.schema import TextNode

    nodes = []
    for idx, text_chunk in enumerate(text_chunks):
        node = TextNode(text=text_chunk)
        src_doc = documents[doc_idxs[idx]]
        node.metadata = src_doc.metadata
        nodes.append(node)

    ## Generate embeddings for each TextNode.

    for node in nodes:
        node_embedding = embedding_model.get_text_embedding(
            node.get_content(metadata_mode="all"))
        node.embedding = node_embedding

    return nodes


def build_index(nodes, vector_store="Milvus"):
    ## Can add logic/support for more vector stores in the future
    from llama_index.core import VectorStoreIndex, StorageContext
    if vector_store=="Milvus":
        from llama_index.vector_stores.milvus import MilvusVectorStore
        vector_store = MilvusVectorStore(uri= "./aimon_docs.db", collection_name = "aimondocs", dim=1536, overwrite=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)
    return index


def build_retriever(index, similarity_top_k=5):
    from llama_index.core.retrievers import VectorIndexRetriever
    retriever = VectorIndexRetriever(index=index, similarity_top_k=similarity_top_k)
    return retriever


def ask_and_validate(user_query, user_instructions, retriever, llm):

    from llama_index.core.query_engine import RetrieverQueryEngine
    query_engine = RetrieverQueryEngine.from_args(retriever, llm)
    response = query_engine.query(user_query)

    ## Nested function to retrieve context and relevance scores from the LLM response.
    def get_source_docs(chat_response):
      contexts = []
      relevance_scores = []
      if hasattr(chat_response, 'source_nodes'):
          for node in chat_response.source_nodes:
              if hasattr(node, 'node') and hasattr(node.node, 'text') and hasattr(node,
                                                                          'score') and node.score is not None:
                  contexts.append(node.node.text)
                  relevance_scores.append(node.score)
              elif hasattr(node, 'text') and hasattr(node, 'score') and node.score is not None:
                  contexts.append(node.text)
                  relevance_scores.append(node.score)
              else:
                  logging.info("Node does not have required attributes.")
      else:
          logging.info("No source_nodes attribute found in the chat response.")
      return contexts, relevance_scores

    context, relevance_scores = get_source_docs(response)
    return context, user_query, user_instructions, response.response