import os
import pandas as pd
from langchain_experimental.agents import create_csv_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage

def ejecutar_consulta(pregunta):
    sheet_id = "1K8f_mfByLNZY48UoQ9T_CzTpRyxCWwee3jmNrxU7kGQ"
    gid = "3208895"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    df = pd.read_csv(url)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df.to_csv("temp.csv", index=False)

    llm = ChatOpenAI(temperature=0.3, model_name="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    agent = create_csv_agent(llm=llm, path="temp.csv", verbose=False, handle_parsing_errors=True)

    system_message = SystemMessage(content="""- You are a senior analyst at Kavak.
- Always generate a clear, actionable summary based strictly on the information provided.
- Only respond with insights if the user asks a business question.
- Compare countries when relevant.
- Refer to countries by name: AR = Argentina, CL = Chile, MX = Mexico, BR = Brazil, GCC = GCC.""")

    try:
        resultado = agent.invoke(pregunta)["output"]
        final = llm.invoke([system_message, {"role": "user", "content": f"Pregunta: {pregunta}\n\nResumen: {resultado}"}])
        return final.content
    except Exception as e:
        return f"Error: {str(e)}"
