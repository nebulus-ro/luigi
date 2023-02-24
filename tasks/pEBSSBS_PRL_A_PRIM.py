import sqlite3
import time
import pandas as pd

def process_set(conn, df):
    c = conn.cursor()
    c.execute('BEGIN TRANSACTION')
    for _, row in df.iterrows():
        df, freq, time_period, ref_area, indicator, activity, number_empl, product, turnover, client_residence, unit_measure, unit_mult, decimals, obs_status, obs_status_1, conf_status, conf_status_1, obs_value, dominance, share_second, comment_obs = row.values
        c.execute('SELECT id FROM flow1keys WHERE freq=? AND time_period=? AND ref_area=? AND indicator=? AND activity=? AND number_empl=? AND product=? AND turnover=? AND client_residence=? AND unit_measure=?', \
                  (freq, time_period, ref_area, indicator, activity, number_empl, product, turnover, client_residence, unit_measure))
        result = c.fetchone()
        if result:
            keyID = result[0]
        else:
            c.execute('INSERT INTO flow1keys (freq, time_period, ref_area, indicator, activity, number_empl, product, turnover, client_residence, unit_measure) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                      (freq, time_period, ref_area, indicator, activity, number_empl, product, turnover, client_residence, unit_measure))
            keyID = c.lastrowid

        c.execute('SELECT obs_status, obs_status_1, conf_status, conf_status_1, obs_value, unit_mult, decimals, dominance, share_second, comment_obs FROM flow1values WHERE keyID=? ORDER BY timestamp DESC LIMIT 1', (keyID,))
        result = c.fetchone()
        if not result or \
            (result[0] != obs_status or result[1] != obs_status_1 or result[2] != conf_status or result[3] != conf_status_1 or result[4] != obs_value or result[5] != unit_mult):
            timestamp = int(time.time())
            c.execute('INSERT INTO flow1values (timestamp, keyID, obs_status, obs_status_1, conf_status, conf_status_1, obs_value, unit_mult, decimals, dominance, share_second, comment_obs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                       (timestamp, keyID, obs_status, obs_status_1, conf_status, conf_status_1, obs_value, unit_mult, decimals, dominance, share_second, comment_obs))
    conn.commit()
