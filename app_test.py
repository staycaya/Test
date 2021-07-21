import streamlit as st
import numpy as np 
import psycopg2
import warnings
import datetime
import pandas as pd
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# @st.cache

sale_date_og = st.date_input('Pick the sale date')
sale_date = sale_date_og.strftime("%Y-%m-%d")

conn = psycopg2.connect(host='ec2-52-30-249-200.eu-west-1.compute.amazonaws.com',
                      dbname='d262kqjmj5i477',
                      user='aya',
                      password='p679d56110f3291d3a9a4b707a93a539e31d3deb7f191a50a5aa121f6175874f7')
cursor = conn.cursor()
cursor.execute(""" SELECT b.date, b.customer_first_name, b.customer_last_name, b.customer_phone, b.customer_email, b.code, h.name, cf.global_score, cf.comment FROM customer_feedbacks cf
                    JOIN bookings_by_sale_dates b on b.id = cf.booking_id
                    JOIN hotels h on h.id = b.hotel_id
                    WHERE b.status = 'accepted'
                    AND cf.global_score <8
                    AND b.sale_date BETWEEN %s AND %s
                    ORDER BY h.name; """,
                    (sale_date, sale_date))
result = cursor.fetchall()
reviews = pd.DataFrame(result, columns=['Date', 'Prénom', 'Nom de famille', 'N° de téléphone', 'e-mail', 'N° de réservation',
                                       'Hôtel', 'Note', 'Commentaire'])
conn.close()

st.write("### Bad reviews of the week", reviews)