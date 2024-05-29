import os
from docx import Document

def create_word_document(name):
    doc = Document()
    doc.add_heading(name, level=1)
    doc.save(f'{name}.docx')

car_names = [
    'Audi',
    'Mazda',
    'Rolls Royce',
    'Dodge',
    'BMW',
    'Mercedes',
    'Mitsubishi',
    'Volvo',
    'Renault'
]

for car_name in car_names:
    create_word_document(car_name)

print("Word documents created successfully.")
