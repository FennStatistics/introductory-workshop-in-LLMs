# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import random


def retrieveGenerate(query_text, prompt_template, openAI_key, chroma_path, docsReturn=5, thresholdSimilarity=0.7):
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(api_key=openAI_key)
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=150) # !!!

    filtered_results = []
    for res in results:
        if res[1] > thresholdSimilarity:
            filtered_results.append(res)

    print(f"Number of possible relevant text chunks found with a threshold similarity of {thresholdSimilarity}:", len(filtered_results))

    # print("results:", results, "\n")
    if len(filtered_results) == 0:
        print("Unable to find matching results.")
        response_text, source_page_pairs, results = None, None, None, results
    else:
        
        # Randomly sample up to 5 documents from filtered results.
        sample_size = min(len(filtered_results), docsReturn)
        sampled_results = random.sample(filtered_results, sample_size)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in sampled_results])
        
        prompt_template_instance = ChatPromptTemplate.from_template(prompt_template)
        prompt = prompt_template_instance.format(context=context_text, question=query_text)
        # print("Query:", prompt, "\n\n")

        model = ChatOpenAI(api_key=openAI_key, temperature=0.3)
        response_text = model.predict(prompt)

        # get sources within results
        sources = [doc.metadata.get("source", None) for doc, _score in sampled_results]

        # get page number within results
        pages = [doc.metadata.get("page", None) for doc, _score in sampled_results]

        # combine sources and pages
        source_page_pairs = list(zip(sources, pages))

    #formatted_response = f"{response_text} \n\n (sources, pages): {source_page_pairs}"
    #print(formatted_response)
    return response_text, source_page_pairs, sampled_results, filtered_results