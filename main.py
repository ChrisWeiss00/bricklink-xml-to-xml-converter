import pandas as pd
import math
#einlesen
df6 = pd.read_xml('xml_daten/4339.xml',encoding='utf-8', xpath='//*')
df = pd.read_xml('xml_daten/4348.xml')
df2 = pd.read_xml('xml_daten/4347.xml')
df7 = pd.read_xml('xml_daten/4349.xml')
df8 = pd.read_xml('xml_daten/4439.xml')
df9 = pd.read_xml('xml_daten/7690.xml')
df10 = pd.read_xml('xml_daten/7971.xml')
df11 = pd.read_xml('xml_daten/8773.xml')
df12 = pd.read_xml('xml_daten/9677.xml')
df3 = pd.read_xml('xml_daten/8832.xml' )
df4 = pd.read_xml('xml_daten/75321.xml')
df13 = pd.read_xml('xml_daten/76092.xml')
df5 = pd.read_xml('xml_daten/Ski.xml')
#concat
df= pd.concat([df,df2,df3,df4,df5,df7,df8,df9,df10,df11,df12,df13])

#sortieren
df=df.sort_values(by=['ITEMID','COLOR'])
for ind in df.index:
    df.at[ind,'CONDITION']="U"
df=df.reset_index(drop=True)

#falls eins existiert wo qtfilled ist, wird die minqty runtergesetzt
#evtl entfernen, falls qtfilled nicht vorhanden
qty=False
rem=False
for col in df.columns:
    if col=="QTYFILLED":
        qty=True

        for ind in df.index:
            if math.isnan(df.at[ind,'QTYFILLED']):
                color=1
            elif df.at[ind,'QTYFILLED']>=df.at[ind,'MINQTY']:
                df=df.drop(ind)
            else:
                df.at[ind,'MINQTY']=df.at[ind,'MINQTY']-int(df.at[ind,'QTYFILLED'])
    elif  col=="REMARKS":
        rem=True
if qty==True:
    df=df.drop(columns=['QTYFILLED'])
if rem==True:
    df=df.drop(columns=['REMARKS'])



#bearbeiten der Felder das nurnoch eins pro Farbe/Id übrig bleibt
#1. der letzten Reihe pro Color/id alle andere zusammenrechnen
#2. nurnoch den letzten wert behalten
#1. werte addieren
color =0
id =0
value= 0
for ind in df.index:
    if id== df.at[ind,'ITEMID']:
        if color== df.at[ind,'COLOR']:
            df.at[ind,'MINQTY']=df.at[ind,'MINQTY']+value
        if df.at[ind,'COLOR']==math.nan:
            print(ind)
    id=df.at[ind,'ITEMID']
    color=df.at[ind,'COLOR']
    value=df.at[ind,'MINQTY']
#duplicates löschen
#df.duplicated(keep=False,subset=['ITEMID','COLOR'])
df=df.drop_duplicates(keep='last',subset=['ITEMID','COLOR'])
print(df)
#print(df.sort_values(by=['COLOR']))
#ausgabe formatieren
df=df.drop(columns=['MAXPRICE','NOTIFY'])
df=df.rename(columns={"MINQTY":"QTY"})
df.to_xml("zwischen.xml",index=False,row_name='ITEM',root_name='INVENTORY',xml_declaration=False)
print(df.dtypes)
df['COLOR']=df['COLOR'].astype('Int64')
df=df.to_xml("output.xml",index=False,row_name='ITEM',root_name='INVENTORY',xml_declaration=False)

print(df)
