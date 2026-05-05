from zipfile import ZipFile
import xml.etree.ElementTree as ET

z = ZipFile('43110402_PPT_MPG.pptx')
slides = sorted([f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')])

for slide_num, slide_file in enumerate(slides, 1):
    content = z.read(slide_file).decode('utf-8')
    root = ET.fromstring(content)
    
    # Define namespaces
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }
    
    # Extract all text elements
    text_elements = root.findall('.//a:t', ns)
    texts = [elem.text for elem in text_elements if elem.text]
    
    print(f"\n{'='*70}")
    print(f"SLIDE {slide_num}")
    print(f"{'='*70}")
    for text in texts:
        print(f"  {text}")
