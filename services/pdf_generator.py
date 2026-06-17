import os
from datetime import datetime
from fpdf import FPDF
from models.product import Product

def generate_products_pdf(products: list[Product], filename: str = "products_report.pdf") -> str:
    pdf = FPDF()
    pdf.add_page()
    
    # Set document metadata
    pdf.set_title("Products Catalog Report")
    pdf.set_author("FastAPI Product Service")
    
    # Title Banner
    pdf.set_fill_color(33, 47, 61)  # Dark Navy/Slate
    pdf.rect(0, 0, 210, 40, "F")
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 20, "PRODUCTS CATALOG REPORT", ln=True, align="C")
    
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 5, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    
    pdf.ln(15)
    
    # Summary info
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Total Products in Catalog: {len(products)}", ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_fill_color(46, 134, 193)  # Premium Blue
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 11)
    
    # Columns: ID (15), Name (75), Price (30), Stock (30), Category (40)
    pdf.cell(15, 10, "ID", border=1, align="C", fill=True)
    pdf.cell(75, 10, "Name", border=1, align="L", fill=True)
    pdf.cell(30, 10, "Price ($)", border=1, align="R", fill=True)
    pdf.cell(30, 10, "Stock", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Category ID", border=1, align="C", fill=True)
    pdf.ln()
    
    # Table Rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    
    fill = False
    for p in products:
        # Alternating background colors
        if fill:
            pdf.set_fill_color(240, 244, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        pdf.cell(15, 8, str(p.id), border=1, align="C", fill=True)
        pdf.cell(75, 8, str(p.name), border=1, align="L", fill=True)
        pdf.cell(30, 8, f"{float(p.price):.2f}", border=1, align="R", fill=True)
        pdf.cell(30, 8, str(p.stock), border=1, align="C", fill=True)
        cat_id = str(p.category_id) if p.category_id is not None else "-"
        pdf.cell(40, 8, cat_id, border=1, align="C", fill=True)
        pdf.ln()
        fill = not fill
        
    # Save file
    os.makedirs("reports", exist_ok=True)
    filepath = os.path.join("reports", filename)
    pdf.output(filepath)
    return filepath
