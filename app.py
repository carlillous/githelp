import streamlit as st
from mongodb.mongo_client import MongoDBClient
from neo4j_integration.neo4j_connection import Neo4JConnection

# Aquí puedes escribir el código para tu aplicación
st.title('GitHelp')

mongo_client = MongoDBClient("github_data", "repositories", username="carlosmenegg", password="agcnc7SuS7f9BPou")
neo4j_driver = Neo4JConnection("neo4j+ssc://761fb7e4.databases.neo4j.io:", "neo4j", "bUamNfpq4UTlaV1A15xaDf0Tv0oebuQYOKhtX5O068Q")

mongo_query = st.text_area("Consulta para MongoDB")
neo4j_query = st.text_area("Consulta para Neo4j")

if st.button("Ejecutar consultas"):
    if mongo_query.strip() == "" and neo4j_query.strip() == "":
        st.warning("Por favor ingresa al menos una consulta.")
    else:
        if mongo_query.strip() != "":
            with mongo_client.client.start_session() as session:
                db = mongo_client.base_de_datos
                collection = db.mi_coleccion
                results_mongo = collection.find(mongo_query.strip())

            st.header("Resultados de MongoDB:")
            for result in results_mongo:
                st.write(result)

        if neo4j_query.strip() != "":
            with neo4j_driver.session() as session:
                results_neo4j = session.run(neo4j_query.strip())

            st.header("Resultados de Neo4j:")
            for record in results_neo4j:
                st.write(record)

