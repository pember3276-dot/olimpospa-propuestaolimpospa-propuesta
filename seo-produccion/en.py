# Traducción al inglés de la página de producción. Cada par (español, inglés) se
# aplica sobre el HTML ya armado; si un texto en español cambia en v4-2, el armado
# se detiene y avisa cuál falta actualizar aquí.
import re, json

WA_ES = 'Hola, vengo de su sitio web, deseo agendar un masaje'
WA_EN = "Hello, I’m coming from your website, I’d like to book a massage"

PAIRS = [
 # Mensajes de WhatsApp (primero los que llevan complemento)
 (WA_ES + ': Masaje Relajante (Olimpo o Spartacus)', WA_EN + ': Relaxing Massage (Olimpo or Spartacus)'),
 (WA_ES + ': Experiencia de bienestar exclusiva (Gladiador o Fuego Divino)', WA_EN + ': Exclusive wellness experience (Gladiador or Fuego Divino)'),
 (WA_ES + ': Masaje con dos o tres Diosas', WA_EN + ': Massage with two or three Goddesses'),
 (WA_ES + ': Experiencia de bienestar en pareja', WA_EN + ': Couples wellness experience'),
 ("'" + WA_ES + " con '+o.name", '"' + WA_EN + ' with "+o.name'),
 # Menú
 ('aria-label="Olimpo Spa, inicio"', 'aria-label="Olimpo Spa, home"'),
 ('>Espacios</a>', '>Spaces</a>'),
 ('>Nuestras diosas</a>', '>Our goddesses</a>'),
 ('>Masajes y valores</a>', '>Massages and prices</a>'),
 ('<a href="#masajes">Masajes</a>', '<a href="#masajes">Massages</a>'),
 ('Agenda tu masaje ↗', 'Book your massage ↗'),
 ('aria-label="Abrir menú"', 'aria-label="Open menu"'),
 ('aria-label="Menú principal"', 'aria-label="Main menu"'),
 # Portada
 ('<h1>Relájate, respira. <em>Vuelve a ti.</em></h1>', '<h1>Relax, breathe. <em>Come back to you.</em></h1>'),
 ('Spa inspirado en diosas de la mitología griega', 'A spa inspired by the goddesses of Greek mythology'),
 ('Masajes relajantes en Laureles, Medellín. Cuerpo completo, piedras volcánicas y aromaterapia con terapeutas profesionales.', 'Relaxing massages in Laureles, Medellín. Full body, hot stones and aromatherapy with professional therapists.'),
 ('>Ver Diosas ↗', '>Meet the Goddesses ↗'),
 ('>Experiencias y valores ↗', '>Experiences and prices ↗'),
 # Espacios
 ('>Espacios del spa<', '>Spa spaces<'),
 ('Hay espacios que se visitan. Otros se sienten.', 'Some spaces you visit. Others you feel.'),
 ('aria-label="Fotos anteriores"', 'aria-label="Previous photos"'),
 ('aria-label="Galería de espacios, desliza para ver más"', 'aria-label="Spaces gallery, swipe to see more"'),
 ('aria-label="Más fotos"', 'aria-label="More photos"'),
 ('Sala con bustos clásicos, fuente y velas', 'Lounge with classical busts, fountain and candles'),
 ('Habitación con camilla y espejo dorado iluminado', 'Room with massage table and lit golden mirror'),
 ('Pasillo del spa con pared verde esmeralda', 'Spa hallway with emerald green wall'),
 ('Sala de espera con cortinas, palma y luz cálida', 'Waiting lounge with curtains, palm and warm light'),
 ('Salón con sofá y luz cálida', 'Lounge with sofa and warm light'),
 ('Habitación con camilla y camino verde esmeralda', 'Room with massage table and emerald green runner'),
 ('Habitación cálida con velas y palma', 'Warm room with candles and palm'),
 ('Habitación con camilla y luz indirecta', 'Room with massage table and soft lighting'),
 ('Salón con cielo de luces de colores', 'Lounge with a ceiling of colored lights'),
 ('Galería de las habitaciones de Olimpo. Toca una foto para ampliarla.', 'Gallery of the rooms at Olimpo. Tap a photo to enlarge it.'),
 # Diosas
 ('<span class="eyebrow">Nuestras diosas</span>', '<span class="eyebrow">Our goddesses</span>'),
 ('Sofisticación, relajación y bienestar', 'Sophistication, relaxation and wellness'),
 ('En Olimpo Spa Massage, combinamos masajes de relajación profunda con un ambiente elegante y de inspiración griega.', 'At Olimpo Spa Massage we combine deep relaxation massages with an elegant, Greek-inspired setting.'),
 ('Disfruta una experiencia sensorial pensada para liberar tensiones y dedicarte un momento de bienestar.', 'Enjoy a sensory experience designed to release tension and give yourself a moment of wellness.'),
 ('Ambiente elegante<', 'Elegant setting<'),
 ('Relajación profunda<', 'Deep relaxation<'),
 ('Bienestar sensorial<', 'Sensory wellness<'),
 ('Reserva tu sesión →', 'Book your session →'),
 ('aria-label="Reproducir video"', 'aria-label="Play video"'),
 # Masajes
 ('Masajes relajantes Medellín</span>', 'Relaxing massages in Medellín</span>'),
 ('Elige tu experiencia<', 'Choose your experience<'),
 ('Todos los masajes incluyen bebida de bienvenida y ducha al inicio y al final.', 'Every massage includes a welcome drink and a shower before and after. Prices in Colombian pesos (COP).'),
 ('Terapeuta en atuendo de inspiración griega', 'Therapist in Greek-inspired attire'),
 ('<h3>Masaje Relajante</h3>', '<h3>Relaxing Massage</h3>'),
 ('Un masaje privado pensado para liberar tensión acumulada y recuperar una sensación de calma.', 'A private massage designed to release built-up tension and bring back a sense of calm.'),
 ('Contamos con 4 experiencias', 'We offer 4 experiences'),
 ('<h3>Experiencia de bienestar exclusiva</h3>', '<h3>Exclusive wellness experience</h3>'),
 ('Una experiencia inmersiva de bienestar, con movimiento suave y atención en un espacio privado.', 'An immersive wellness experience with gentle movement and personal attention in a private space.'),
 ('<h3>Masaje con dos o tres Diosas</h3>', '<h3>Massage with two or three Goddesses</h3>'),
 ('Dos o tres terapeutas trabajan en armonía para ofrecer una experiencia de masaje más envolvente.', 'Two or three therapists work in harmony for a more enveloping massage experience.'),
 ('<h3>Experiencia de bienestar en pareja</h3>', '<h3>Couples wellness experience</h3>'),
 ('Un momento para compartir, conectar y hacer una pausa juntos en un entorno tranquilo.', 'A moment to share, connect and pause together in a calm setting.'),
 ('Consultar disponibilidad →', 'Check availability →'),
 # Cierre
 ('Empieza hoy tu momento de bienestar', 'Start your moment of wellness today'),
 ('Estamos en Laureles, Medellín. Escríbenos por WhatsApp y te confirmamos la cita.', 'We are in Laureles, Medellín. Message us on WhatsApp and we will confirm your appointment.'),
 ('¿Listo para sentirte mejor?', 'Ready to feel better?'),
 ('Habla directamente con un asesor de Olimpo Spa y elige el ritual y el espacio que más te gusten. Sin llenar formularios ni esperar.', 'Talk directly with an Olimpo Spa advisor and choose the ritual and the space you like best. No forms, no waiting.'),
 ('aria-label="Ampliar foto de la fachada"', 'aria-label="Enlarge photo of the entrance"'),
 ('Fachada de Olimpo Spa, Carrera 77B #48B-41, con el timbre señalado', 'Olimpo Spa entrance, Carrera 77B #48B-41, with the doorbell marked'),
 ('Mapa de ubicación de Olimpo Spa en Laureles', 'Map showing Olimpo Spa in Laureles'),
 ('Estamos en una de las zonas más convenientes de Medellín para visitantes y residentes. Escríbenos antes de llegar; nuestro equipo te orientará con discreción.', 'We are in one of the most convenient areas of Medellín for visitors and residents. Message us before you arrive; our team will guide you discreetly.'),
 ('<h3>Enlaces</h3>', '<h3>Links</h3>'),
 ('<h3>Masajes</h3>', '<h3>Massages</h3>'),
 ('Spartacus y Gladiador', 'Spartacus and Gladiador'),
 ('4 y 6 manos', '4 and 6 hands'),
 ('<h3>Horarios y pagos</h3>', '<h3>Hours and payment</h3>'),
 ('<li>Lunes a sábado de 11 am a 7 pm</li>', '<li>Monday to Saturday, 11 am to 7 pm</li>'),
 ('Domingos bajo reserva', 'Sundays by appointment'),
 ('Efectivo: pesos colombianos y dólares', 'Cash: Colombian pesos and US dollars'),
 ('<li>Transferencia</li>', '<li>Bank transfer</li>'),
 ('<h3>Contacto</h3>', '<h3>Contact</h3>'),
 ('Cerca al C.C. Obelisco y a la estación Floresta', 'Near Obelisco mall and Floresta metro station'),
 ('Privacidad · Términos', 'Privacy · Terms'),
 # Visor y asistente
 ('aria-label="Foto ampliada"', 'aria-label="Enlarged photo"'),
 ('aria-label="Cerrar"', 'aria-label="Close"'),
 ('aria-label="Foto anterior"', 'aria-label="Previous photo"'),
 ('aria-label="Foto siguiente"', 'aria-label="Next photo"'),
 ('hidden>Reservar ↗', 'hidden>Book ↗'),
 ('aria-label="Asistente virtual de Olimpo"', 'aria-label="Olimpo virtual assistant"'),
 ('Asistente virtual<small>Respuestas al instante</small>', 'Virtual assistant<small>Instant answers</small>'),
 ('aria-label="Cerrar asistente"', 'aria-label="Close assistant"'),
 ('placeholder="Escribe tu mensaje…" aria-label="Escribe tu mensaje"', 'placeholder="Type your message…" aria-label="Type your message"'),
 ('aria-label="Enviar"', 'aria-label="Send"'),
 ('aria-label="Abrir asistente virtual"', 'aria-label="Open virtual assistant"'),
 ('aria-label="Escribir por WhatsApp"', 'aria-label="Message us on WhatsApp"'),
 ('aria-label="Acciones rápidas"', 'aria-label="Quick actions"'),
 ('>Cómo llegar</a>', '>Directions</a>'),
 ('>Terapeutas</a>', '>Therapists</a>'),
 # Script
 (", terapeuta de Olimpo\"", ", Olimpo therapist\""),
 ('Ampliar foto ›', 'Enlarge photo ›'),
 ('Foto próximamente', 'Photo coming soon'),
 ("'Reservar con '+o.name", "'Book with '+o.name"),
 ("'Ampliar foto: '", "'Enlarge photo: '"),
 ('Fachada de Olimpo Spa · Carrera 77B #48B-41, cerca al Centro Comercial Obelisco y a la estación Floresta', 'Olimpo Spa entrance · Carrera 77B #48B-41, near Obelisco mall and Floresta metro station'),
 ('Ir al chat de WhatsApp ↗', 'Go to WhatsApp chat ↗'),
 ('Hola, soy la asistente virtual de Olimpo. Nuestro horario es de 11 am a 7 pm de lunes a sábado, y domingos bajo reserva. Para una atención más humana, da clic en el siguiente botón y te llevará a nuestro chat corporativo.', 'Hi, I am the Olimpo virtual assistant. We are open Monday to Saturday from 11 am to 7 pm, and Sundays by appointment. To talk with a person, tap the button below and it will take you to our WhatsApp chat.'),
 ("['Dúo del Olimpo','$220.000']", "['Dúo del Olimpo','$220.000']"),
 ("'Masajes y precios','Estos son nuestros masajes y sus valores:'", "'Massages and prices','These are our massages and their prices in Colombian pesos:'"),
 ("['4 manos','$320.000'],['6 manos','$430.000'],['Dúo del Olimpo (parejas)'", "['4 hands','$320.000'],['6 hands','$430.000'],['Dúo del Olimpo (couples)'"),
 ("'Experiencia para parejas','Tenemos dos experiencias para parejas:'", "'Couples experience','We have two experiences for couples:'"),
 ("'Horario y ubicación','Atendemos de lunes a sábado de 11 am a 7 pm, y domingos bajo reserva. Estamos en la Carrera 77B #48B-41, Laureles, Medellín.", "'Hours and location','We are open Monday to Saturday from 11 am to 7 pm, and Sundays by appointment. We are at Carrera 77B #48B-41, Laureles, Medellín."),
 ('<iframe title="Mapa"', '<iframe title="Map"'),
 ('">Cómo llegar ↗</a>', '">Directions ↗</a>'),
 ("'Quiero reservar','Perfecto. Toca el botón y te atendemos de inmediato por WhatsApp.'", "'I want to book','Great. Tap the button and we will help you right away on WhatsApp.'"),
 ("/precio|valor|cu[aá]nto|masaje/.test(s)?0:/pareja/.test(s)?1:/reserv|agend|cita/", "/precio|valor|cu[aá]nto|masaje|price|cost|how much|massage/.test(s)?0:/pareja|couple/.test(s)?1:/reserv|agend|cita|book|appointment/"),
]

META = {
 'title': 'Olimpo Spa Medellín | Relaxing Massages in Laureles',
 'description': 'Discover a unique relaxation experience at Olimpo Spa Medellín. Professional massages in Laureles with personal attention in an exclusive setting. Book your appointment.',
 'keywords': 'Medellín spa, massage Medellín, Laureles spa, relaxing massage, wellness Medellín, Olimpo Spa',
 'og:description': 'Relaxing massages in Laureles, Medellín, in an exclusive Greek-inspired setting. Monday to Saturday, 11 am to 7 pm. Book on WhatsApp.',
 'twitter:description': 'Relaxing massages in Laureles, Medellín, in an exclusive Greek-inspired setting. Book on WhatsApp.',
 'og:image:alt': 'Olimpo Spa lounge with classical busts, fountain and candles',
}
LD = {
 'Spa de masajes relajantes en Laureles, Medellín, con ambiente de inspiración griega, habitaciones privadas y atención personalizada. Reservas por WhatsApp.': 'Relaxing massage spa in Laureles, Medellín, with a Greek-inspired setting, private rooms and personal attention. Bookings on WhatsApp.',
 'Efectivo, Transferencia bancaria': 'Cash, Bank transfer',
 'Masajes y valores': 'Massages and prices',
 'Masaje Olimpo': 'Olimpo massage', 'Masaje Spartacus': 'Spartacus massage', 'Masaje Gladiador': 'Gladiador massage',
 'Masaje Fuego divino': 'Fuego divino massage', 'Masaje a 4 manos': '4 hands massage', 'Masaje a 6 manos': '6 hands massage',
 'Dúo del Olimpo (parejas)': 'Dúo del Olimpo (couples)', 'La reina y el emperador (parejas)': 'La reina y el emperador (couples)',
 'Masaje relajante privado. Incluye bebida de bienvenida y ducha al inicio y al final.': 'Private relaxing massage. Includes a welcome drink and a shower before and after.',
 'Experiencia de bienestar exclusiva. Incluye bebida de bienvenida y ducha al inicio y al final.': 'Exclusive wellness experience. Includes a welcome drink and a shower before and after.',
 'Masaje con dos terapeutas. Incluye bebida de bienvenida y ducha al inicio y al final.': 'Massage with two therapists. Includes a welcome drink and a shower before and after.',
 'Masaje con tres terapeutas. Incluye bebida de bienvenida y ducha al inicio y al final.': 'Massage with three therapists. Includes a welcome drink and a shower before and after.',
 'Experiencia de bienestar en pareja. Incluye bebida de bienvenida y ducha al inicio y al final.': 'Couples wellness experience. Includes a welcome drink and a shower before and after.',
 'es-CO': 'en',
}

def traducir(s):
    falt = [a for a, b in PAIRS if a not in s]
    assert not falt, 'Textos que ya no están en la página; actualizar seo-produccion/en.py: %r' % falt
    for a, b in PAIRS: s = s.replace(a, b)
    s = s.replace(WA_ES, WA_EN)
    s = s.replace('<html lang="es">', '<html lang="en">', 1)
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % META['title'], s, count=1)
    for k in ('og:title', 'twitter:title'): META[k] = META['title']
    for k, v in META.items():
        if k == 'title': continue
        s, n = re.subn(r'(<meta (?:name|property)="%s" content=")[^"]*"' % re.escape(k), lambda m: m.group(1) + v + '"', s); assert n == 1, k
    s = s.replace('<meta property="og:locale" content="es_CO">', '<meta property="og:locale" content="en_US">')
    s = s.replace('<link rel="canonical" href="https://olimpospa.com.co/">', '<link rel="canonical" href="https://olimpospa.com.co/en/">')
    s = s.replace('<meta property="og:url" content="https://olimpospa.com.co/">', '<meta property="og:url" content="https://olimpospa.com.co/en/">')
    # Datos estructurados
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    def tr(o):
        if isinstance(o, dict): return {k: tr(v) for k, v in o.items()}
        if isinstance(o, list): return [tr(v) for v in o]
        if isinstance(o, str) and o in LD: return LD[o]
        return o
    j = tr(json.loads(m.group(2)))
    for g in j['@graph']:
        if g.get('@type') == 'WebSite': g['url'] = 'https://olimpospa.com.co/en/'; g['@id'] = 'https://olimpospa.com.co/en/#sitio'
    s = s[:m.start(2)] + '\n' + json.dumps(j, ensure_ascii=False, indent=1) + '\n' + s[m.end(2):]
    # La página vive en /en/: los recursos están un nivel arriba
    s = re.sub(r'''(?<=["'( ])(img/|fuentes/|logo-olimpo\.webp|favicon\.png)''', r'../\1', s)
    return s
