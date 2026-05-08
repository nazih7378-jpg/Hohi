import streamlit as st
import pandas as pd

def process_files(file1, file2):
    # قراءة الملفات
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # دمج الملفين في جدول واحد
    df_merged = pd.concat([df1, df2], ignore_index=True)
    
    # تحويل عمود الوقت إلى صيغة DateTime لضمان الترتيب الصحيح
    # ملاحظة: سيتم التعرف تلقائياً على الصيغ المختلفة (مع وقت أو بدونه)
    df_merged['Horaire_Sorted'] = pd.to_datetime(df_merged['Horaire'], errors='coerce')
    
    # ترتيب البيانات حسب الوقت (الأقدم أولاً) بدون حذف أي شيء
    df_merged = df_merged.sort_values(by='Horaire_Sorted').drop(columns=['Horaire_Sorted'])
    
    return df_merged

st.title("Outil de Fusion des Évènements")
st.write("ارفع ملفات Excel لدمجها وترتيبها زمنياً")

uploaded_f1 = st.file_uploader("Upload F1 (Excel)", type=["xlsx"])
uploaded_f2 = st.file_uploader("Upload F2 (Excel)", type=["xlsx"])

if uploaded_f1 and uploaded_f2:
    if st.button("دمج وترتيب الأحداث"):
        result_df = process_files(uploaded_f1, uploaded_f2)
        
        st.success("تم الترتيب بنجاح!")
        st.dataframe(result_df) # عرض معاينة للنتيجة
        
        # تحويل النتيجة لملف Excel للتحميل
        output_path = "Merged_Events_Final.xlsx"
        result_df.to_excel(output_path, index=False)
        
        with open(output_path, "rb") as f:
            st.download_button(
                label="تحميل الملف النهائي",
                data=f,
                file_name="Merged_Events_Final.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
