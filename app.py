import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="CSPM Vulnerability Delta")

st.title("🛡️ CSPM Vulnerability Comparison Dashboard")
st.write("Upload two scans (CSV) to identify Open vs. Closed vulnerabilities.")

# 1. File Uploaders
col1, col2 = st.columns(2)
with col1:
    old_file = st.file_uploader("Upload PREVIOUS Scan (File 1)", type="csv")
with col2:
    new_file = st.file_uploader("Upload LATEST Scan (File 2)", type="csv")

if old_file and new_file:
    df1 = pd.read_csv(old_file)
    df2 = pd.read_csv(new_file)

    # 2. Create a Unique Key (Asset + CVE)
    # This ensures we track the CVE specifically on that machine/resource
    for df in [df1, df2]:
        df['Unique_ID'] = df['Inventory.Name'].astype(str) + "_" + df['CveId'].astype(str)

    # 3. Logic: Compare Sets
    set_old = set(df1['Unique_ID'])
    set_new = set(df2['Unique_ID'])

    # Closed: In Old but NOT in New
    closed_ids = set_old - set_new
    # Still Open: In BOTH Old and New
    still_open_ids = set_old.intersection(set_new)
    # New Findings: In New but NOT in Old
    new_findings_ids = set_new - set_old

    # 4. Filter Dataframes
    df_closed = df1[df1['Unique_ID'].isin(closed_ids)]
    df_open = df2[df2['Unique_ID'].isin(still_open_ids)]
    df_new = df2[df2['Unique_ID'].isin(new_findings_ids)]

    # 5. Visualizations
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Closed (Fixed)", len(df_closed), delta_color="normal")
    m2.metric("Still Open", len(df_open), delta=f"+{len(df_new)} new", delta_color="inverse")
    m3.metric("Total Current", len(df2))

    # 6. Data Tables
    st.subheader("✅ Closed Vulnerabilities (Fixed)")
    st.dataframe(df_closed[['CveId', 'Inventory.Name', 'CvssSeverity', 'CloudAccount.Name']])

    st.subheader("⚠️ Still Open Vulnerabilities")
    st.dataframe(df_open[['CveId', 'Inventory.Name', 'CvssSeverity', 'CloudAccount.Name']])

    # Download Button for Report
    csv = df_open.to_csv(index=False).encode('utf-8')
    st.download_button("Download Open Vulns CSV", data=csv, file_name="open_vulns.csv")