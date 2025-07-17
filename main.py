from odoo import http
from odoo.http import request

import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.chat_models import ChatOpenAI


class LibraryAgentController(http.Controller):

    @http.route('/library/agent_ui', type='http', auth='public', website=True)
    def library_agent_ui(self, **kwargs):
        return request.render("library_agent.library_agent_page", {})

    @http.route('/library/agent_query', type='json', auth='public', csrf=False)
    def agent_query(self, **kwargs):
        question = kwargs.get("question", "")
        print("Received question:", question)

        try:
            os.environ["OPENAI_API_KEY"] = "key"

            db_uri = "postgresql://aarti:odoo17@localhost:5432/odoo17"
            db = SQLDatabase.from_uri(db_uri, include_tables=["library_book"])

            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)

            agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )

            response = agent.run(question)
            return {"result": {"response": response}}

        except Exception as e:
            print("Error:", e)
            return {"result": {"response": f"Error: {str(e)}"}}