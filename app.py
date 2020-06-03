import pandas as pd 
import streamlit as st
import json
from PIL import Image
from firebase import firebase
from streamlit import caching

image = Image.open('banner.jpg')
st.image(image, caption='',use_column_width=True)

image = Image.open('logo.jpg')
st.sidebar.image(image, caption='',use_column_width=True)

documento=st.sidebar.selectbox("¿Qué tipo de documento tienes?",("DNI", "CARNET EXTRANJERIA"))
st.sidebar.text_input(label='DNI',value='',key=None, type='default')

firebase=firebase.FirebaseApplication('https://diccionario-analitika.firebaseio.com/', None)


@st.cache(persist=False,allow_output_mutation=True)
def obtener_datos():
	####---conectarme a firebase:
	GRUPOPALABRAS= firebase.get('/0', None)
	GRUPOPALABRAS=json.dumps(GRUPOPALABRAS)
	dfpalabras=json.loads(GRUPOPALABRAS)
	dfpalabras = pd.DataFrame(dfpalabras)

	#muestreo de la tabla
	x=dfpalabras.sample(n=1)

	#obtener la palabra
	palabra=x['grupo'].values
	palabra=palabra[0]

	#obtener el indice
	indice=x['Id'].values
	indice=indice[0]

	return(indice,palabra)


result1=obtener_datos()
indice = result1[0]
palabra= result1[1]
st.title("Califica la siguiente palabra")

html_temp = """
				<div style="background-color:#26c5de;opacity: 0.80;padding:0.2 px">
				<h1 style="color:white;text-align:center;">"""+palabra+""" </h2>
				</div>"""
st.markdown(html_temp,unsafe_allow_html=True)

polaridad1= st.selectbox(label="polaridad",options=['seleccionar','positiva','neutra','negativa'],index=0,)

if polaridad1 == 'positiva':
	sccore=st.number_input(label='nivel positiva',min_value=2, max_value=5)
if polaridad1 == 'neutra':
	sccore=st.number_input(label='nivel neutra',min_value=-1, max_value=1)
if polaridad1 == 'negativa':
	sccore=st.number_input(label='nivel negativa',min_value=-5, max_value=-2)

if polaridad1 == 'positiva':
	emocion2= st.selectbox(label="tipo emocion positiva",options=['seleccionar','enfado','disgusto','miedo','alegria','tristeza','sorpresa','confianza'],index=0,)
if polaridad1 == 'neutra':
	emocion2= st.selectbox(label="tipo de emocion neutra",options=['seleccionar','enfado','disgusto','miedo','alegria','tristeza','sorpresa','confianza'],index=0,)
if polaridad1 == 'negativa':
	emocion2= st.selectbox(label="tipo de emocion negativa",options=['seleccionar','enfado','disgusto','miedo','alegria','tristeza','sorpresa','confianza'],index=0,)

if polaridad1 == 'positiva':
	sccore2=st.number_input(label='Califica la emocion',min_value=1, max_value=5)
if polaridad1 == 'neutra':
	sccore2=st.number_input(label='Califica la emocion ',min_value=1, max_value=5)
if polaridad1 == 'negativa':
	sccore2=st.number_input(label='Califica la emocion   ',min_value=1, max_value=5)

def main():
	if st.button("**GUARDAR CALIFICACION**"):
		dni=documento
		ids=indice
		polaridad=polaridad1
		score=sccore
		emocion=emocion2
		score_emotion=sccore2
		result=firebase.post('/respuesta',{'id': int(ids),'polaridad': polaridad,'score':int(score),'emocion': emocion,'score_emotion':int(score_emotion),'dni':dni})
		caching.clear_cache()

if __name__ == '__main__':
	main()

st.button('Rerun')
