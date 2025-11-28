"""
Simple script to create a sample PDF for testing
"""
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    c = canvas.Canvas('sample.pdf', pagesize=letter)
    c.drawString(100, 750, 'Sample PDF Document')
    c.drawString(100, 730, 'This is a test PDF for the QA system.')
    c.drawString(100, 710, 'You can ask questions about this document.')
    c.save()
    print('sample.pdf created successfully')
except ImportError:
    print('reportlab not installed. Using alternative method...')
    # Create a minimal PDF manually
    import os
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length 117 >>
stream
BT
/F1 12 Tf
100 750 Td
(Sample PDF Document) Tj
0 -20 Td
(This is a test PDF for the QA system.) Tj
0 -20 Td
(You can ask questions about this document.) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000244 00000 n 
0000000333 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
500
%%EOF
"""
    with open('sample.pdf', 'wb') as f:
        f.write(pdf_content)
    print('sample.pdf created successfully (minimal PDF)')
