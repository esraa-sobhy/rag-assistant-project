from groq import Groq


class Generator:
    def __init__(self, api_key: str, model_name: str):
        self.model_name = model_name
        self.client = Groq(api_key=api_key)

    def generate(self, question: str, documents):

        context_parts = []
        sources = []

        for i, doc in enumerate(documents, start=1):

            source = doc.metadata.get(
                "source",
                "Unknown"
            )

            context_parts.append(
                f"[Chunk {i} | Source: {source}]\n"
                f"{doc.page_content}"
            )

            sources.append(
                f"Chunk {i} — {source}"
            )

        context = "\n\n---\n\n".join(context_parts)

        prompt = f"""
You are a helpful assistant.

Answer the user's question using ONLY the provided context.

If the answer is not available in the context, say:
"I could not find the answer in the provided document."

Do not use outside knowledge.
Do not make up information.

At the end of your answer, mention the relevant source.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        return answer, sources