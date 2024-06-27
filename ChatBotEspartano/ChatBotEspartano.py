from flask import Flask, request, jsonify, render_template
import re
from collections import defaultdict
import openai

openai.api_key = "sk-proj-QNOUOLds2uSOx8VWAxBoT3BlbkFJXYL3XYO7iWMi0CyX1QPW"

app = Flask(__name__)

modelo = "gpt-3.5-turbo"

def obtener_respuesta_gpt3(entrada_usuario):
    try:
        respuesta = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {"role": "user", "content": entrada_usuario}
            ],
            max_tokens=150
        )
        respuesta_texto = respuesta['choices'][0]['message']['content']
        return respuesta_texto.strip()
    except Exception as e:
        return str(e)

def obtener_respuesta(entrada_usuario):
    mensaje_dividido = re.split(r'\s|[,:;.?!-_]\s*', entrada_usuario.lower())
    respuesta = verificar_todos_los_mensajes(mensaje_dividido)
    return respuesta

def calcular_probabilidad(mensaje_usuario, palabras_reconocidas, respuesta_unica=False, palabras_requeridas=[]):
    certeza_mensaje = 0
    tiene_palabras_requeridas = True

    for palabra in mensaje_usuario:
        if palabra in palabras_reconocidas:
            certeza_mensaje += 1

    porcentaje = float(certeza_mensaje) / float(len(palabras_reconocidas))

    for palabra in palabras_requeridas:
        if palabra not in mensaje_usuario:
            tiene_palabras_requeridas = False
            break

    if tiene_palabras_requeridas or respuesta_unica:
        return int(porcentaje * 100)
    else:
        return 0

def verificar_todos_los_mensajes(mensaje):
    mayor_probabilidad = defaultdict(int)

    def agregar_respuesta(respuesta_bot, lista_de_palabras, respuesta_unica=False, palabras_requeridas=[]):
        nonlocal mayor_probabilidad
        probabilidad = calcular_probabilidad(mensaje, lista_de_palabras, respuesta_unica, palabras_requeridas)
        if probabilidad > mayor_probabilidad[respuesta_bot]:
            mayor_probabilidad[respuesta_bot] = probabilidad

    # Definir respuestas posibles y palabras clave asociadas
    agregar_respuesta('Hola', ['hola', 'saludo', 'saludos', 'buenas'], respuesta_unica=True)
    agregar_respuesta('Estoy bien y tú?', ['como', 'estas', 'vas', 'sientes'], respuesta_unica=True)
    agregar_respuesta('Que bueno que te encuentres bien', ['bien', 'todo', 'encuentro', 'super', 'genial'], palabras_requeridas=['bien'])
    agregar_respuesta('¡Claro! Estoy aquí para ayudarte. ¿Qué deseas saber?', ['ayuda','necesito', 'quisisera', 'ayudes', 'ayuda','ayudar'], respuesta_unica=True)
    agregar_respuesta('Me llamo Espartano, en que puedo ayudarte?', ['nombre','como','cual','llamas'], respuesta_unica=True)
    agregar_respuesta('No te preocupes, estare aqui para ayudar!', ['perdon', 'siento'], respuesta_unica=True)
    agregar_respuesta('Lamento oir eso. Procura repasar a tiempo y consulta tus dudas al docente', ['estoy', 'mal','curso','que','pesimo','grave'], respuesta_unica=True)


    # ACERCA DE LA UNIVERSIDAD CONTINENTAL
    # Definir las respuestas posibles y sus palabras clave asociadas
    agregar_respuesta('La Organización Educativa Continental nace en Huancayo como Centro de Cómputo en 1983.'+ 
                      'Sin embargo, gracias al crecimiento e innovación, en 1998 se fundó la Universidad Continental'+ 
                      ' de Ciencias e Ingeniería (Hace 23 años iniciábamos con 3 carreras y con solo 180 estudiantes.'+ 
                      ' Hoy somos más de 44 mil estudiantes en nuestros diferentes campus Huancayo, Arequipa, Cusco y Lima.)', 
                      ['contar', 'reseña', 'historia', 'universidad', 'continental'], respuesta_unica=True)
    agregar_respuesta('La Universidad Continental cuenta con 29 carreras profesionales', ['carrera', 'carreras','cuantas','que'], respuesta_unica=True)
    agregar_respuesta('La Universidad Continental cuenta con las modalidades presencial, semipresencial y a distancia.', ['que', 'cuenta', 'tiene', 'son', 'cuales', 'modalidad', 'modalidad','modalidades','que'], respuesta_unica=True)
    agregar_respuesta('Estamos ubicados en Sector Angostura km. 10 - San Jerónimo', ['ubicados', 'ubicación','ubicacion', 'dirección', 'direccion', 'donde', 'cusco','Cusco','cual','universidad','continental'], respuesta_unica=True)
    agregar_respuesta('Estamos ubicados en Av. Alfredo Mendiola 5210 Los Olivos - Lima', ['ubicados', 'ubicación','ubicacion', 'dirección', 'donde', 'direccion', 'lima','Lima','cual','universidad','continental'], respuesta_unica=True)
    agregar_respuesta('Estamos ubicados en La Canseco II / Sector: Valle Chili José Luis Bustamante y Rivero - Arequipa', ['ubicados', 'ubicación','ubicacion', 'dirección', 'direccion', 'donde', 'arequipa','Arequipa','cual','universidad','continental'], respuesta_unica=True)
    agregar_respuesta('Estamos ubicados en Av. San Carlos 1980 Urb. San Antonio - Huancayo', ['ubicados', 'ubicación','ubicacion', 'dirección', 'donde', 'direccion', 'huancayo','Huancayo','cual','universidad','continental'], respuesta_unica=True)
    agregar_respuesta('¡De nada! Estoy aquí para ayudar', ['gracias', 'te lo agradezco', 'informacion','información'], respuesta_unica=True)
    #A cerca de los cursos
    agregar_respuesta('Este semestre estás inscrito en los siguientes cursos: \n'
                      'Arquitectura Empresarial,\n'+
                      'Redes de Computadores \n'
                      'Construccion de Software\n'
                      'Ingenieria economica\n'
                      'Gestion profesional\n'
                      'innovacion social',   ['Que', 'cursos', 'que', 'llevando','llevo'], respuesta_unica=True)
    agregar_respuesta('El curso de Arquitectura empresarial lo dicta el docente: Erick Alcca Zela.', ['arquitectura', 'empresarial','quien'], respuesta_unica=True)
    agregar_respuesta('El curso de Construccion de software lo dicta el docente: Hugo Espetia Huamanga.', ['construccion', 'software','quien'], respuesta_unica=True)
    agregar_respuesta('El curso de Gestion Profesional lo dicta el docente: Jesus Castro Mardiaga.', ['gestion', 'profesional','quien'], respuesta_unica=True)
    agregar_respuesta('El curso de Ingenieria economica lo dicta la docente: Veronica Garcia Tovar.', ['ingenieria', 'economica','quien'], respuesta_unica=True)
    agregar_respuesta('El curso de Innovacion social lo dicta la docente: yesenia Florez Mujica.', ['innovacion', 'social','quien'], respuesta_unica=True)
    agregar_respuesta('El curso de Redes de Computadores lo dicta el docente: Erick Alcca Zela.', ['redes', 'computadores','quien'], respuesta_unica=True)
        #Horario y dias
    agregar_respuesta('El curso de Arquitectura empresarial lo llevas los dias lunes de 5:20 pm a 6:49 pm '+
                      'y los dias miercoles de 3:40 pm a 6:49 pm', ['arquitectura', 'empresarial','dia','dias'], respuesta_unica=True)
    agregar_respuesta('El curso de Construccion de Software lo llevas los dias miercoles de 2:00 pm a 3:29 pm '+
                      'y los dias jueves de 2:00 pm a 5:09 pm', ['construccion', 'software','dia','dias'], respuesta_unica=True)
    agregar_respuesta('El curso de Gestion Profesional lo llevas el dia jueves de manera remota a las 7:00 pm a 8:29 pm ', ['gestion', 'profesional','dia','dias'], respuesta_unica=True)
    agregar_respuesta('El curso de Ingenieria Economica lo llevas los dias lunes a las 7:00 am a 8:29 am '+
                      'y los dias jueves de 8:40 am a 10:09 am', ['ingenieria', 'economica','dia','dias'], respuesta_unica=True)
    agregar_respuesta('El curso de Innovacion Social lo llevas el dia viernes de 2:00 pm a 5:09 pm ', ['innovacion', 'social','dia','dias'], respuesta_unica=True)
    agregar_respuesta('El curso de Redes de Computadores lo llevas el dia lunes de 3:40pm a 5:09pm '+
                      'y los dias martes de 3:40 pm a 6:49 pm ', ['redes', 'computadores','dia','dias'], respuesta_unica=True)
    agregar_respuesta('El curso de construccion de software lo llevas en el aula A304 los dias miercoles y los'
                      +' jueves en el aula A801', ['construccion', 'aula','salon','clase','en','que'], respuesta_unica=True)
    agregar_respuesta('El NRC del curso de construccion de software es: 12861. ', ['nrc', 'NRC','que','construccion','software'], respuesta_unica=True)
    agregar_respuesta(' Las pruebas unitarias son como revisiones detalladas de cada parte del código,'
                      +'como inspeccionar piezas de un rompecabezas para asegurarse de que encajen perfectamente.'
                      +' Ayudan a encontrar errores desde el principio y mantienen el software confiable al verificar'
                      +'funciones y métodos individualmente. Es fundamental para asegurar que todo funcione como se '
                      +'espera y para evitar problemas costosos en etapas avanzadas del desarrollo.', ['pruebas', 'unitarias','construccion','que','tdd'], respuesta_unica=True)
    agregar_respuesta('Tu horario asignado para este semestre es: \n'
                      +'Lunes: Redes de computadores(3.40 pm a 5:09 pm)-Arquitectura empresarial (5:20 pm a 6:49 pm).\n'
                      'Martes: Ingenieria Economica(7:00 am a 8:29 am)-Redes de computadores(3:40 pm a 6:49 pm)\n'
                      'Miercoles: Construccion de software(2:00 pm a 3:29 pm)-Arquitectura empresarial(3:40 pm a 6:49 pm)\n'
                      'Jueves: Construccion de Software(2:00 pm a 5:09 pm)-Gestion profesional(7:00 pm a 8:30 pm)\n'
                      'Viernes: Innovacion social(2:00 pm a 5:09 pm)', ['horario', 'cual','es','mi','son','clases'], respuesta_unica=True)

    agregar_respuesta('Fui creado en junio del 2024 en Cusco-Perú. Mi dueño legal es el Ingeniero Hugo Espetia Huamanga pero '
                      +'suelen usarme de manera gratuita sin restricciones.', ['dueño', 'quien','te','creo','es','naciste','cuando'], respuesta_unica=True)
    
    agregar_respuesta('El primer sprint del proyecto debe presentarse el dia 13 de junio del 2024. ', ['sprint', 'construccion','dia','dias','primer','cs'], respuesta_unica=True)
    agregar_respuesta('El primer sprint del proyecto fue presentado el dia 13 de junio del 2024. ', ['sprint', 'cuando', 'se', 'construccion','dia','dias','primer','cs'], respuesta_unica=True)
    agregar_respuesta('El segundo sprint del proyecto debe presentarse el dia 27 de junio del 2024. ', ['segundo', 'cuando', 'segundo', 'construccion','dia','dias','sprint','cs'], respuesta_unica=True)
    agregar_respuesta('El actual semestre academico(2024-1) culmina el dia viernes 5 de julio. Puede extenderse en caso lleves '
                      'un examen sustiturio.', ['cuando', 'acaba','termina','culmina','semestre'], respuesta_unica=True)

    if mayor_probabilidad:
        mejor_respuesta = max(mayor_probabilidad, key=mayor_probabilidad.get)
        if mayor_probabilidad[mejor_respuesta] > 0:
            return mejor_respuesta

    return "Lo siento, no entiendo tu mensaje. ¿Podrías reformularlo?"

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    datos = request.get_json()
    mensaje_usuario = datos.get('message')
    if 'chat' in mensaje_usuario.lower():
        respuesta = obtener_respuesta_gpt3(mensaje_usuario)
    else:
        respuesta = obtener_respuesta(mensaje_usuario)
    return jsonify({'message': respuesta})

if __name__ == '__main__':
    app.run(debug=True)
