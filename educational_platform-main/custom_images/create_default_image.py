from PIL import Image, ImageDraw, ImageFont
import os

def create_default_image():
    # Создаем изображение размером 400x300 пикселей
    width, height = 400, 300
    image = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(image)
    
    # Добавляем рамку
    draw.rectangle([(10, 10), (width-10, height-10)], outline='#dee2e6', width=2)
    
    # Добавляем текст
    try:
        # Пробуем использовать системный шрифт
        font = ImageFont.truetype("Arial", 24)
    except:
        # Если системный шрифт недоступен, используем стандартный
        font = ImageFont.load_default()
    
    text = "Изображение\nне загружено"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='#6c757d', font=font)
    
    # Сохраняем изображение
    image.save(os.path.join(os.path.dirname(__file__), 'default-task-image.png'))

if __name__ == '__main__':
    create_default_image() 