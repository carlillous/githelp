import streamlit as st
import pandas as pd
from mongodb.mongo_client import MongoDBClient
from neo4j_integration.neo4j_connection import Neo4JConnection
import json

# Función para ejecutar consultas
def execute_queries(mongo_query, neo4j_query, selected_collection):
    results = {}

    # Ejecutar consulta en MongoDB
    if mongo_query.strip():
        try:
            mongo_query_dict = json.loads(mongo_query.strip())
            collection = mongo_client.database[selected_collection]
            results_mongo = list(collection.find(mongo_query_dict))

            results["mongo"] = results_mongo
        except Exception as e:
            results["mongo_error"] = str(e)

    # Ejecutar consulta en Neo4j
    if neo4j_query.strip():
        try:
            with neo4j_driver.session() as session:
                results_neo4j = session.run(neo4j_query.strip())
                results_neo4j = [dict(record) for record in results_neo4j]

            results["neo4j"] = results_neo4j
        except Exception as e:
            results["neo4j_error"] = str(e)

    return results

st.title('GitHelp')

mongo_client = MongoDBClient("github_data", username="carlosmenegg", password="agcnc7SuS7f9BPou")
neo4j_driver = Neo4JConnection("neo4j+ssc://b47768d5.databases.neo4j.io:", "neo4j", "4I9XJHCkbj3zth9vf3POnpU6byO9cIjboda_aUwLC3k")

# MongoDB Query Section
st.sidebar.header("Consulta MongoDB")
collections = ['repositories', 'users', 'network']  # List of collections
selected_collection = st.sidebar.selectbox("Selecciona la colección", collections)
mongo_query = st.sidebar.text_area("Consulta (JSON)")

# Neo4j Query Section
st.sidebar.header("Consulta Neo4j")
neo4j_query = st.sidebar.text_area("Consulta (Cypher)")

# Execute Queries
execute_button = st.sidebar.button("Ejecutar consultas")

if execute_button:
    if not mongo_query.strip() and not neo4j_query.strip():
        st.warning("Por favor ingresa al menos una consulta.")
    else:
        results = execute_queries(mongo_query, neo4j_query, selected_collection)

        # Guardar en el historial
        st.session_state.query_history.append({
            "collection": selected_collection,
            "mongo_query": mongo_query,
            "neo4j_query": neo4j_query,
            "results": results
        })

        # Mostrar resultados de MongoDB
        if "mongo" in results:
            st.subheader(f"Resultados de MongoDB ({selected_collection}):")
            if results["mongo"]:
                df_mongo = pd.DataFrame(results["mongo"])
                st.dataframe(df_mongo)
                csv_mongo = df_mongo.to_csv(index=False)
                st.download_button("Descargar resultados de MongoDB", csv_mongo, "resultados_mongo.csv", "text/csv")
            else:
                st.write("No se encontraron resultados en MongoDB.")
        elif "mongo_error" in results:
            st.error(f"Error en la consulta de MongoDB: {results['mongo_error']}")

        # Mostrar resultados de Neo4j
        if "neo4j" in results:
            st.subheader("Resultados de Neo4j:")
            if results["neo4j"]:
                df_neo4j = pd.DataFrame(results["neo4j"])
                st.dataframe(df_neo4j)
                csv_neo4j = df_neo4j.to_csv(index=False)
                st.download_button("Descargar resultados de Neo4j", csv_neo4j, "resultados_neo4j.csv", "text/csv")
            else:
                st.write("No se encontraron resultados en Neo4j.")
        elif "neo4j_error" in results:
            st.error(f"Error en la consulta de Neo4j: {results['neo4j_error']}")


# Historial de Consultas
st.sidebar.header("Historial de Consultas")
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

with st.sidebar.expander("Mostrar Historial de Consultas"):
    for i, entry in enumerate(st.session_state.query_history):
        st.write(f"Consulta {i + 1}:")
        st.write("MongoDB (Colección):", entry["collection"])
        st.write("Consulta MongoDB:", entry["mongo_query"])
        st.write("Consulta Neo4j:", entry["neo4j_query"])
        if st.button(f"Mostrar Resultados {i + 1}"):
            if "mongo" in entry["results"]:
                st.subheader(f"Resultados de MongoDB ({entry['collection']}):")
                if entry["results"]["mongo"]:
                    df_mongo = pd.DataFrame(entry["results"]["mongo"])
                    st.dataframe(df_mongo)
                else:
                    st.write("No se encontraron resultados en MongoDB.")
            elif "mongo_error" in entry["results"]:
                st.error(f"Error en la consulta de MongoDB: {entry['results']['mongo_error']}")

            if "neo4j" in entry["results"]:
                st.subheader("Resultados de Neo4j:")
                if entry["results"]["neo4j"]:
                    df_neo4j = pd.DataFrame(entry["results"]["neo4j"])
                    st.dataframe(df_neo4j)
                else:
                    st.write("No se encontraron resultados en Neo4j.")
            elif "neo4j_error" in entry["results"]:
                st.error(f"Error en la consulta de Neo4j: {entry['results']['neo4j_error']}")