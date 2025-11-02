from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def preprocess_image(image_path):
    """Resmi modele uygun hale getirir."""
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    return data

def get_all_predictions(model_path, labels_path, image_path):
    """Tüm sınıflar için tahmin oranlarını döndürür."""
    model = load_model(model_path, compile=False)
    with open(labels_path, "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f.readlines()]
    
    input_data = preprocess_image(image_path)
    predictions = model.predict(input_data)[0]  # shape: (n_classes,)

    # Her sınıf için (isim, yüzde) şeklinde liste oluştur
    results = []
    for i, score in enumerate(predictions):
        label = class_names[i].strip()
        if label.startswith(" "):  # Teachable Machine bazen boşluk ekler
            label = label[2:] if len(label) > 2 else label[1:]
        percentage = round(float(score) * 100, 2)
        results.append((label, percentage))
    
    # en yüksekten düşüğe sırala
    results.sort(key=lambda x: x[1], reverse=True)
    return results