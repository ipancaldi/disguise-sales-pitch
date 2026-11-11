"""Compile the protected templates, editable copy and media to one offline HTML file."""
from argparse import ArgumentParser
from functools import lru_cache
from html import escape
from io import BytesIO
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
import base64
import hashlib
import json
import re

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
ASSETS = ROOT / 'assets'
MEDIA = REPO / 'media'
VERTICAL_ICONS = {'Picto_Live', 'Picto_LBX', 'Picto_Broadcast', 'Picto_VP'}
IMAGE_FIELDS = json.loads((ROOT / 'cms-image-fields.json').read_text(encoding='utf-8'))
HARDWARE_DEFAULTS = json.loads((ROOT / 'hardware-media-defaults.json').read_text(encoding='utf-8'))
CONTENT = {
    p.stem: json.loads(p.read_text(encoding='utf-8'))
    for p in (REPO / 'content').glob('*.json')
}
ASSET_TOKEN = re.compile(r'@@([\w-]+)@@')
COPY_TOKEN = re.compile(r'@@(HTML|JHTML|JS|JDATA|QHTML|THTML|URL):([a-z0-9_]+\.[a-z0-9_]+)@@')


def value(key):
    filename, field = key.split('.')
    try:
        v = CONTENT[filename][field]
    except KeyError as exc:
        raise ValueError(f'Missing editable field: {key}') from exc
    if not isinstance(v, str) or len(v) > 6000 or not v.strip():
        raise ValueError(f'Expected non-empty text of at most 6,000 characters: {key}')
    return v


def js_literal(v):
    return json.dumps(v, ensure_ascii=True).replace('<', r'\u003c').replace('>', r'\u003e')


def embed_copy(m):
    mode, key = m.groups()
    v = value(key)
    if mode == 'URL':
        u = urlsplit(v)
        if u.scheme != 'https' or not u.hostname or u.username or u.password or any(c.isspace() for c in v):
            raise ValueError(f'Enter a valid HTTPS link for {key}')
        return escape(v)
    if mode == 'HTML':
        return escape(v)
    if mode == 'JHTML':
        return js_literal(escape(v))
    if mode == 'JS':
        return js_literal(v)
    if mode == 'QHTML':
        return js_literal(escape(v))[1:-1]
    if mode == 'JDATA':
        return js_literal(v)[1:-1]
    return escape(v).replace('\\', '\\\\').replace('`', '\\`').replace('$', r'\$')


def data_uri(kind, raw):
    return f'data:{kind};base64,' + base64.b64encode(raw).decode('ascii')


def editable_image(slot):
    v = value(IMAGE_FIELDS[slot])
    raw = PurePosixPath(v.lstrip('/'))
    if not raw.parts or raw.parts[0] != 'media' or '..' in raw.parts or '\\' in v:
        raise ValueError(f'Choose an uploaded image for {IMAGE_FIELDS[slot]}')
    file = (REPO / raw).resolve()
    if not file.is_relative_to(MEDIA.resolve()) or file.suffix.lower() not in {'.jpg','.jpeg','.png','.webp'}:
        raise ValueError(f'Choose a JPG, PNG or WebP image for {IMAGE_FIELDS[slot]}')
    if not file.is_file():
        raise ValueError(f'Uploaded image not found: {v}')
    if file.stat().st_size > 25 * 1024 * 1024:
        raise ValueError(f'Image exceeds 25 MB: {v}')
    return file


@lru_cache(maxsize=None)
def photo(file, wide=False):
    with Image.open(file) as src:
        im = ImageOps.exif_transpose(src).convert('RGB')
    im.thumbnail((1800 if wide else 1350, 1200))
    b = BytesIO()
    im.save(b, 'JPEG', quality=86, optimize=True)
    return data_uri('image/jpeg', b.getvalue())


def hardware_assets():
    geometry = json.loads((ROOT / 'hardware-geometry.json').read_text(encoding='utf-8'))
    for key, asset in geometry.items():
        slot = 'hardware-' + key
        if slot in IMAGE_FIELDS:
            file = editable_image(slot)
            raw = file.read_bytes()
            if hashlib.sha256(raw).hexdigest() != HARDWARE_DEFAULTS[key]:
                with Image.open(file) as source:
                    im = ImageOps.exif_transpose(source).convert('RGBA')
                im.thumbnail((2200,2200))
                b = BytesIO()
                im.save(b, 'WEBP', quality=90, method=4)
                raw = b.getvalue()
                asset['replacement'] = True
            asset['src'] = data_uri('image/webp', raw)
        else:
            file = ROOT / asset['file']
            if file.suffix == '.svg':
                asset['src'] = data_uri('image/svg+xml', file.read_bytes())
            else:
                asset['src'] = data_uri('image/webp', file.with_suffix('.webp').read_bytes())
    return json.dumps(geometry)


@lru_cache(maxsize=None)
def asset(name):
    if name in VERTICAL_ICONS:
        return data_uri('image/svg+xml', (ASSETS / 'vertical-icons' / (name+'.svg')).read_bytes())
    binary = {
        'XKEY': ('image/png', 'x-series-dongle.png'),
        'CALIBRATIONVIDEO': ('video/mp4', 'calibration-loop.mp4'),
        'REEL': ('video/mp4', 'project-reel.mp4'),
        'D3MAN': ('image/svg+xml', 'd3man.svg'),
        'logo': ('image/svg+xml', 'logo.svg'),
    }
    if name in binary:
        kind, file = binary[name]
        return data_uri(kind, (ASSETS / file).read_bytes())
    templates = {
        'NEEDCSS':'needs.css','NEEDJS':'needs.js','STORYCSS':'story.css','STORYJS':'story.js',
        'STAGEJS':'stage.js','CITIES':'global-cities.json','STORYSECTIONS':'story.sections.html',
        'VERTICALSECTION':'verticals.sections.html',
    }
    if name in templates:
        return expand((ROOT / templates[name]).read_text(encoding='utf-8'))
    if name == 'THREE':
        return (ASSETS / 'three.min.js').read_text(encoding='utf-8')
    if name == 'HARDWAREASSETS':
        return hardware_assets()
    if name == 'SOFTWAREICONS':
        files = {'designer':'Designer Pro.svg','renderstream':'RenderStream.svg','mapping':'Mapping Matter.svg',
                 'porta':'App_Ico_Porta.svg','plugin':'Plugin Icon.svg','api':'API.svg','aid3n':'Ask_Aid3n.svg',
                 'omnical':'OmniCal.svg','x1':'X1-1.svg','x2':'X2.svg','x3':'X3.svg'}
        return json.dumps({k: data_uri('image/svg+xml',(ASSETS/'software-icons'/f).read_bytes()) for k,f in files.items()})
    file = editable_image(name) if name in IMAGE_FIELDS else ASSETS / (name+'.jpg')
    return photo(file, name in {'hero','sphere-photo','story-platform'})


def expand(text):
    return ASSET_TOKEN.sub(lambda m: asset(m[1]), text)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=REPO / 'index.html')
    args = parser.parse_args()
    template = expand((ROOT / 'experience.source.html').read_text(encoding='utf-8'))
    out = COPY_TOKEN.sub(embed_copy, template)
    if len(out.encode('utf-8')) > 90 * 1024 * 1024:
        raise ValueError('The standalone page exceeds 90 MB. Use smaller images.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(out, encoding='utf-8')
    print(f'Built {args.output}: {len(out.encode("utf-8")) / 1024 / 1024:.2f} MB')
