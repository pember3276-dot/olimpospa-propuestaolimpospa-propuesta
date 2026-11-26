#!/bin/sh
# Arma el sitio de producción (olimpospa.com.co) a partir de v4-2. Uso: sh seo-produccion/construir.sh CARPETA_DESTINO
set -e
D="$1"; rm -rf "$D"; mkdir -p "$D/img"
cp v4-2/img/* "$D/img/"; cp v4/img/hero.webp "$D/img/"; cp logo-olimpo.png "$D/"
cp seo-produccion/robots.txt seo-produccion/sitemap.xml seo-produccion/llms.txt "$D/"
python3 - "$D" <<'PY'
import re,sys
s=open('v4-2/index.html',encoding='utf-8').read()
s=s.replace('../v4/img/hero.webp','img/hero.webp').replace('../logo-olimpo.png','logo-olimpo.png')
s,n=re.subn(r'<div class="draft">.*?</div>\n*','',s,count=1,flags=re.S); assert n==1
s,n=re.subn(r'<!-- SEO: esta maqueta.*?-->\n<meta name="robots" content="noindex, nofollow">','<meta name="robots" content="index, follow, max-image-preview:large">',s,flags=re.S); assert n==1
assert '../' not in s
open(sys.argv[1]+'/index.html','w',encoding='utf-8').write(s)
PY
