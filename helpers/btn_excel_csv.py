from io import BytesIO
import streamlit as st
import pandas as pd


def btn_excel_csv(base, nombre_archivo):
    # convertir a excel en memoria
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
            base.to_excel(writer, index=False, sheet_name="Datos")

    excel_data = output.getvalue()

        # botón descarga
        # st.download_button(
        #     label="📥 Descargar Excel",
        #     data=excel_data,
        #     file_name="datos_filtrados.xlsx",
        #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # )



        #######################
    csv = base.to_csv(index=False).encode("utf-8")

        # st.download_button(
        #     label="📥 Descargar CSV",
        #     data=csv,
        #     file_name="datos_filtrados.csv",
        #     mime="text/csv"
        # )


    col1, col2 = st.columns(2)

    with col1:
            # botón 
            # botón descarga
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=f"{nombre_archivo}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn-excel"
            )

    with col2:
            # botón csv
                st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"{nombre_archivo}.csv",
                mime="text/csv",
                key="btn-csv"
            )

        

    
    