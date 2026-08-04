import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base=r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
# gather reform icon refs
icons=[]
for f in glob.glob(base+r'\common\government_reforms\*.txt'):
    c=open(f,encoding='utf-8',errors='ignore').read()
    for m in re.finditer(r'icon\s*=\s*"([^"]+)"', c):
        icons.append((os.path.basename(f), m.group(1)))
# gather sprite definitions
sprites=set()
for g in glob.glob(base+r'\interface\*.gfx'):
    c=open(g,encoding='utf-8',errors='ignore').read()
    for m in re.finditer(r'name\s*=\s*"government_reform_([^"]+)"', c):
        sprites.add(m.group(1))
print('reform icon refs:')
for f,ic in icons:
    need='government_reform_'+ic
    ok = ic in sprites
    print(f'  {f}: icon={ic} -> sprite {"OK" if ok else "MISSING"}')
print()
# verify texture files exist for each sprite
for g in glob.glob(base+r'\interface\*.gfx'):
    c=open(g,encoding='utf-8',errors='ignore').read()
    for m in re.finditer(r'texturefile\s*=\s*"([^"]+)"', c):
        tex=os.path.join(base, m.group(1).replace('/','\\'))
        print(os.path.basename(g), '->', os.path.exists(tex) and 'OK' or 'MISSING', m.group(1).split('/')[-1])
