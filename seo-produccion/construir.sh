#!/bin/sh
# Arma el sitio de producción (olimpospa.com.co) a partir de v4-2, con las
# optimizaciones de velocidad. Uso: sh seo-produccion/construir.sh CARPETA_DESTINO
set -e
D="$1"; rm -rf "$D"; mkdir -p "$D/img" "$D/fuentes"
cp seo-produccion/fuentes/*.woff2 "$D/fuentes/"
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
    if n.startswith('video-poster'): return 600
    return 820
def small(n):
    if n.startswith('masajista'): return [('-s',420)]
    if n.startswith('fachada'): return [('-xs',300),('-s',680)]
    if n.startswith('hero'): return [('-s',900)]
    if n.startswith('video-poster'): return []
    return [('-s',460)]
SIZES={'h':'100vw','m':'(max-width:1000px) 45vw, 210px','f':'(max-width:640px) 92vw, (max-width:1100px) 46vw, 280px','g':'(max-width:640px) 62vw, (max-width:1100px) 33vw, 20vw'}
dims={}
for f in sorted(glob.glob('v4-2/img/*.webp'))+['v4/img/hero.webp']:
    n=os.path.basename(f); im=Image.open(f).convert('RGB'); w=lim(n)
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    out=D+'/img/'+n; im.save(out,'WEBP',quality=74,method=6)
    if os.path.getsize(out)>os.path.getsize(f) and im.size==Image.open(f).size:
        open(out,'wb').write(open(f,'rb').read())
    dims['img/'+n]=im.size
    # Versiones pequeñas para srcset (móvil y miniaturas)
    for suf,sw in small(n):
        if im.width>sw: im.resize((sw,round(im.height*sw/im.width)),Image.LANCZOS).save(D+'/img/'+n.replace('.webp',suf+'.webp'),'WEBP',quality=72,method=6)
lg=Image.open('logo-olimpo.png').convert('RGBA')
lg.thumbnail((200,200),Image.LANCZOS); lg.save(D+'/logo-olimpo.webp','WEBP',quality=70,method=6); dims['logo-olimpo.webp']=lg.size
lg=Image.open('logo-olimpo.png').convert('RGBA')
ic=lg.copy(); ic.thumbnail((96,96)); cv=Image.new('RGBA',(96,96),(0,30,25,255)); cv.paste(ic,((96-ic.width)//2,(96-ic.height)//2),ic); cv.save(D+'/favicon.png',optimize=True)

# Versión en los recursos para poder guardarlos un año en caché
h=hashlib.md5()
for f in sorted(glob.glob(D+'/img/*')+glob.glob(D+'/fuentes/*')+[D+'/logo-olimpo.webp']): h.update(open(f,'rb').read())
v=h.hexdigest()[:8]
s=open('v4-2/index.html',encoding='utf-8').read()
s=s.replace('../v4/img/hero.webp','img/hero.webp')
s=s.replace('<link rel="icon" href="../logo-olimpo.png">','<link rel="icon" type="image/png" href="favicon.png">')
s=s.replace('../logo-olimpo.png','logo-olimpo.webp')
s,n=re.subn(r'<div class="draft">.*?</div>\n*','',s,count=1,flags=re.S); assert n==1
s,n=re.subn(r'<!-- SEO: esta maqueta.*?-->\n<meta name="robots" content="noindex, nofollow">','<meta name="robots" content="index, follow, max-image-preview:large">',s,flags=re.S); assert n==1
assert '../' not in s
# Fuentes propias (sin conexiones a Google), solo con los caracteres que usa el sitio
m=re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2[^"]*)">',s); assert m
s=s.replace(m.group(0),'<link rel="preload" as="image" href="img/hero.webp" imagesrcset="img/hero-s.webp?v=%s 900w, img/hero.webp?v=%s 1500w" imagesizes="100vw" fetchpriority="high">'%(v,v))
s,n=re.subn(r'<link rel="preconnect" href="https://fonts\.g[^>]*>\n?','',s); assert n==2
ff=''.join('@font-face{font-family:"%s";font-style:normal;font-weight:%s;font-display:swap;src:url(fuentes/%s.woff2?v=%s) format("woff2")}'%(a,b,c,v) for a,b,c in [('Geist','500 700','geist'),('Lora','500 700','lora'),('Open Sans','400 600','opensans')])
s=s.replace('<style>','<style>\n'+ff,1); assert 'fonts.g' not in s
# Dimensiones en las imágenes, prioridad para la portada
def tag(mm):
    t=mm.group(0); src=mm.group(1)
    if src in dims and ' width=' not in t:
        w,h=dims[src]; t=t[:-1]+' width="%d" height="%d">'%(w,h)
    if src=='img/hero.webp': t=t.replace('<img ','<img fetchpriority="high" decoding="async" ')
    n=os.path.basename(src)
    if src.startswith('img/') and small(n) and 'srcset' not in t:
        k='f' if n.startswith('fachada') else 'h' if n.startswith('hero') else 'g'
        ss=', '.join(['%s?v=%s %dw'%(src.replace('.webp',suf+'.webp'),v,sw) for suf,sw in small(n)]+['%s?v=%s %dw'%(src,v,dims[src][0])])
        t=t.replace(' src=',' srcset="%s" sizes="%s" src='%(ss,SIZES[k]),1)
    return t
s=re.sub(r'<img [^>]*?src="([^"\']+)"[^>]*>',tag,s)
# Accesibilidad: contraste de rótulos, proporción del logo, nombre accesible
s=s.replace('</style>','.eyebrow{color:#7E5E0D}.who img,.bot header img{object-fit:contain}\n</style>',1)
a='''aria-label="Ampliar foto de '+t[0]+'"'''; assert a in s
s=s.replace(' '+a,'')
# Orden de títulos en el pie y contraste del botón de WhatsApp
assert s.count('<h4>')==4 and '.foot h4{' in s
s=s.replace('<h4>','<h3>').replace('</h4>','</h3>').replace('.foot h4{','.foot h3{')
assert s.count('background:#1FA855')==1; s=s.replace('background:#1FA855','background:#0E7C3A')
s=re.sub(r'((?:img/[\w.-]+|logo-olimpo)\.(?:webp|mp4))(?=["\')])',lambda m:m.group(1)+'?v='+v,s)
x="""'.webp" alt="'"""; assert x in s
s=s.replace(x,"""'.webp?v=%s" srcset="img/'+t[1]+'-s.webp?v=%s 420w, img/'+t[1]+'.webp?v=%s 720w" sizes="%s" alt="'"""%(v,v,v,SIZES['m']))
s=s.replace('https://olimpospa.com.co/logo-olimpo.png','https://olimpospa.com.co/logo-olimpo.webp')
open(D+'/index.html','w',encoding='utf-8').write(s)
print('version',v)
PY
