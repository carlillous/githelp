import streamlit as st
from pymongo import MongoClient
from neo4j import GraphDatabase

# Aquí puedes escribir el código para tu aplicación
st.title('GitHelp')

mongo_client = MongoClient("mongodb://usuario:contraseña@localhost:27017/base_de_datos")
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("usuario", "contraseña"))

mongo_query = st.text_area("Consulta para MongoDB")
neo4j_query = st.text_area("Consulta para Neo4j")

if st.button("Ejecutar consultas"):
    if mongo_query.strip() == "" and neo4j_query.strip() == "":
        st.warning("Por favor ingresa al menos una consulta.")
    else:
        if mongo_query.strip() != "":
            with mongo_client.start_session() as session:
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

