# Archivos SEO para producción (olimpospa.com.co)

Estos tres archivos van en la raíz del dominio cuando la versión 4.0, edición 2, se publique en olimpospa.com.co:

- `robots.txt` reemplaza el robots.txt de la maqueta, que bloquea todo a propósito.
- `sitemap.xml` se envía en Google Search Console y Bing Webmaster Tools.
- `llms.txt` resume el negocio para asistentes de IA.

Además, en `index.html` hay que cambiar `noindex, nofollow` por `index, follow, max-image-preview:large` y quitar la franja "Maqueta de propuesta".
Las rutas `../logo-olimpo.png` y `../v4/img/hero.webp` deben quedar dentro del sitio final.
