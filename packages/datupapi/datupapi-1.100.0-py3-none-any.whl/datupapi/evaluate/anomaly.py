import boto3
import numpy as np
import os
import pandas as pd


# from datupapi.configure.config import Config


class Anomaly:

    def __init__(self):
        print('Anomalia')

        
    def detectar_anomalias_prep(self, df, location=False,
                                prob_lim_general=0.85,
                                prob_lim_item=0.95,
                                limite_cambio_demanda=10):
        """
        Función para detectar anomalías y generar alertas en la preparación de nuevos clientes

        Parámetros obligatorios:
        - df: Dataframe a analizar. Debe incluir mínimo las columnas 'timestamp', 'item_id' y 'demand'.

        Parámetros opcionales:
        - location: Indica si existe la columna de location.
        - prob_lim_general: Límite de probabilidad para LOF general(default = 0.85).
        - prob_lim_item: Límite de probabilidad para LOF por item (default = 0.95).
        - limite_cambio_demanda: Límite para la alerta de cambio en la demanda (default = 10%).
        """

        # Preparar dataframe por total y por item
        df['demand'] = df['demand'].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        demand_total = df[['timestamp','demand']]
        demand_total = demand_total.groupby('timestamp').sum()

        demand_item = df[['timestamp','item_id','demand']]
        demand_item = demand_item.groupby(['timestamp','item_id']).sum()
        demand_item = demand_item.reset_index()
        unique_items = demand_item['item_id'].unique()
        print('Unique items:',demand_item['item_id'].nunique())

        if location:
            print("Sección de análsis por item-loc en desarrollo")

        #1. LOF general ------
        demand_reshaped  = demand_total['demand'].values.reshape(-1, 1)
        lof = LOF(n_neighbors = 20, metric ="manhattan", novelty=True)
        lof.fit(demand_reshaped)
        #me quedo sólo con los datos anómalos
        probs = lof.predict_proba(demand_reshaped)
        is_out = probs[:,1] > prob_lim_general
        out = demand_total[is_out]

        #alerta
        alert_anomalies_total = True if not out.empty else False
        alert_anomalies_total_txt = f"Anomalias en el total de la demanda: {out.shape[0]}. Detalles: {out}" if alert_anomalies_total else ""

        #2. LOF por item ------
        out_if_item2 = pd.DataFrame()
        lof2 = LOF(n_neighbors = 20, metric ="manhattan", novelty=True)

        alerta_max = 0
        alerta_media = 0
        items_alerta_max = []
        items_alerta_media = []

        for item_id in unique_items:
            # Filtrar el DataFrame para el ítem actual
            item_tmp = demand_item[demand_item['item_id'] == item_id]

            # Verificar si hay suficientes datos para el modelo LOF
            if 24 < len(item_tmp) <= 48:
                alerta_media = alerta_media +1
                items_alerta_media.append(item_id)

            if len(item_tmp) > 24:  # Asegurar que haya suficientes puntos para aplicar LOF
                # Aplicar LOF
                lof2.fit(item_tmp[['demand']])
                probs = lof2.predict_proba(item_tmp[['demand']])
                is_out = probs[:, 1] > prob_lim_item
                out2 = item_tmp[is_out]

                # Concatenar los outliers del ítem actual al DataFrame de resultados
                out_if_item2 = pd.concat([out_if_item2, out2[['item_id', 'timestamp', 'demand']]], ignore_index=True)

            else:
                alerta_max = alerta_max + 1
                items_alerta_max.append(item_id)

        out_if_item2 = out_if_item2.drop_duplicates()
        #alerta por anomalias
        alert_anomalies_item = True if not out_if_item2.empty else False
        alert_anomalies_item_txt = f"Items con probabilidad de anomalía: {out_if_item2['item_id'].nunique()}. Detalles: {out_if_item2}" if alert_anomalies_item else ""

        #3. Alerta por items con poco histórico -------------------
        alert_insufficient_history = True if alerta_max > 0 or alerta_media > 0 else False
        alert_insufficient_history_txt = f"Items con alerta máxima en el histórico: {alerta_max}. ({', '.join(map(str, items_alerta_max))}). " if alerta_max > 0 else ""
        alert_insufficient_history_txt += f"Items con alerta media en el histórico: {alerta_media}. ({', '.join(map(str, items_alerta_media))})." if alerta_media > 0 else ""

        #4. Cambio drástico en la demanda total en comparación con el mes anterior --OJO ESTO DEBE IR DESPUÉS DEL RESAMPLE
        demand_actual = demand_total['demand'].iloc[-1]
        demand_ant = demand_total['demand'].iloc[-2]
        percentage_change = ((demand_actual - demand_ant) / demand_ant) * 100

        alert_demand_var = True if abs(percentage_change) > 10 else False
        alert_demand_var_txt = f"Variación en la demanda total: {cambio_num_items:.2f}%." if alert_demand_var else ""
        print(f"Demanda tuvo un cambio del {percentage_change:.2f}% respecto al mes anterior.")

        ## --------------------- MATRIZ DE ALERTAS ------------------------------
        execution_date = pd.to_datetime(datetime.now()).strftime('%Y-%m-%d')
        print(execution_date)

        alert_messages = [alert_anomalies_total_txt,
                        alert_anomalies_item_txt,
                        alert_insufficient_history_txt,
                        alert_demand_var_txt
                        ]

        alert_summary = '\n'.join(filter(None, alert_messages)) if any(alert_messages) else "Sin alertas"
        print(alert_summary)

        alert_matrix = pd.DataFrame({
            'Anomalias_Total_Demand': [alert_anomalies_total],
            'Anomalias_Item': [alert_anomalies_item],
            'Historico': [alert_insufficient_history],
            'Var_Demanda_Total': [alert_demand_var],
            'Alertas': [alert_summary]
        })

        return alert_matrix

anomalia = Anomaly()    