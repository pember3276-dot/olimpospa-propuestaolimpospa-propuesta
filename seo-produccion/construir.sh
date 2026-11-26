#!/bin/sh
# Arma el sitio de producción (olimpospa.com.co) a partir de v4-2, con las
# optimizaciones de velocidad. Uso: sh seo-produccion/construir.sh CARPETA_DESTINO
set -e
D="$1"; rm -rf "$D"; mkdir -p "$D/img"
cp seo-produccion/robots.txt seo-produccion/sitemap.xml seo-produccion/llms.txt seo-produccion/google*.html "$D/"
cp seo-produccion/htaccess.txt "$D/.htaccess"
cp v4-2/img/video.mp4 v4-2/img/og.jpg "$D/img/"
python3 - "$D" <<'PY'
import re,sys,glob,os,hashlib
from PIL import Image
D=sys.argv[1]
# Imágenes: ancho máximo según su uso, recomprimidas en WebP
def lim(n):
    if n.startswith('masajista') or n.startswith('diosa'): return 720
    if n.startswith('fachada'): return 1000
    if n.startswith('hero'): return 1500
    if n.startswith('video-poster'): return 720
    return 820
dims={}
for f in sorted(glob.glob('v4-2/img/*.webp'))+['v4/img/hero.webp']:
    n=os.path.basename(f); im=Image.open(f).convert('RGB'); w=lim(n)
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    out=D+'/img/'+n; im.save(out,'WEBP',quality=74,method=6)
    if os.path.getsize(out)>os.path.getsize(f) and im.size==Image.open(f).size:
        open(out,'wb').write(open(f,'rb').read())
    dims['img/'+n]=im.size
lg=Image.open('logo-olimpo.png').convert('RGBA')
lg.save(D+'/logo-olimpo.webp','WEBP',quality=88,method=6); dims['logo-olimpo.webp']=lg.size
ic=lg.copy(); ic.thumbnail((96,96)); cv=Image.new('RGBA',(96,96),(0,30,25,255)); cv.paste(ic,((96-ic.width)//2,(96-ic.height)//2),ic); cv.save(D+'/favicon.png',optimize=True)

s=open('v4-2/index.html',encoding='utf-8').read()
s=s.replace('../v4/img/hero.webp','img/hero.webp')
s=s.replace('<link rel="icon" href="../logo-olimpo.png">','<link rel="icon" type="image/png" href="favicon.png">')
s=s.replace('../logo-olimpo.png','logo-olimpo.webp')
s,n=re.subn(r'<div class="draft">.*?</div>\n*','',s,count=1,flags=re.S); assert n==1
s,n=re.subn(r'<!-- SEO: esta maqueta.*?-->\n<meta name="robots" content="noindex, nofollow">','<meta name="robots" content="index, follow, max-image-preview:large">',s,flags=re.S); assert n==1
assert '../' not in s
# Fuentes sin bloquear el primer pintado
m=re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2[^"]*)">',s); assert m
u=m.group(1)
s=s.replace(m.group(0),'<link rel="preload" as="style" href="%s" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="%s"></noscript>\n<link rel="preload" as="image" href="img/hero.webp" fetchpriority="high">'%(u,u))
# Dimensiones en las imágenes, prioridad para la portada
def tag(mm):
    t=mm.group(0); src=mm.group(1)
    if src in dims and ' width=' not in t:
        w,h=dims[src]; t=t[:-1]+' width="%d" height="%d">'%(w,h)
    if src=='img/hero.webp': t=t.replace('<img ','<img fetchpriority="high" decoding="async" ')
    return t
s=re.sub(r'<img [^>]*?src="([^"\']+)"[^>]*>',tag,s)
# Accesibilidad: contraste de rótulos, proporción del logo, nombre accesible
s=s.replace('</style>','.eyebrow{color:#7E5E0D}.who img,.bot header img{object-fit:contain}\n</style>',1)
a='''aria-label="Ampliar foto de '+t[0]+'"'''; assert a in s
s=s.replace(a,'''aria-label="'+t[0]+'. Ampliar foto"''')
# Versión en los recursos para poder guardarlos un año en caché
h=hashlib.md5()
for f in sorted(glob.glob(D+'/img/*')+[D+'/logo-olimpo.webp']): h.update(open(f,'rb').read())
v=h.hexdigest()[:8]
s=re.sub(r'((?:img/[\w.-]+|logo-olimpo)\.(?:webp|mp4))(?=["\')])',lambda m:m.group(1)+'?v='+v,s)
x="""'.webp" alt="'"""; assert x in s
s=s.replace(x,"""'.webp?v=%s" alt="'"""%v)
s=s.replace('https://olimpospa.com.co/logo-olimpo.png','https://olimpospa.com.co/logo-olimpo.webp')
open(D+'/index.html','w',encoding='utf-8').write(s)
print('version',v)
PY
