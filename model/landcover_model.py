import torch
import torchvision.transforms as T
from torchvision import models
from PIL import Image
import numpy as np

CLASS_NAMES = [
    'Background', 'Wall', 'Building', 'Sky', 'Floor', 'Tree', 'Ceiling', 'Road',
    'Bed', 'Windowpane', 'Grass', 'Cabinet', 'Sidewalk', 'Person', 'Earth',
    'Door', 'Table', 'Mountain', 'Plant', 'Sheep', 'Water', 'Mirror', 'Car',
    'Fence', 'Desk', 'Wild', 'Soil', 'Field', 'BarrenLand'
]

# Mapping from ADE20K/COCO to your categories
MAP_TO_CUSTOM = {
    'Grass': 'Agriculture',
    'Field': 'Agriculture',
    'Tree': 'Forest',
    'Plant': 'Forest',
    'Water': 'Water',
    'Building': 'Urban',
    'Road': 'Urban',
    'Sky': None,
    'Earth': 'BarrenLand',
    'Soil': 'BarrenLand',
    'BarrenLand': 'BarrenLand'
}
CUSTOM_CLASSES = ['Agriculture', 'Forest', 'Water', 'Urban', 'BarrenLand']

def get_model():
    model = models.segmentation.deeplabv3_resnet50(pretrained=True).eval()
    return model

def process_image(image_path):
    model = get_model()
    img = Image.open(image_path).convert('RGB')
    transform = T.Compose([T.Resize((256, 256)), T.ToTensor()])
    inp = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(inp)['out'][0]
    pred = out.argmax(0).numpy()

    # Map ADE20K classes to your custom classes
    counts = {k:0 for k in CUSTOM_CLASSES}
    for c in np.unique(pred):
        name = CLASS_NAMES[c] if c < len(CLASS_NAMES) else None
        if name and name in MAP_TO_CUSTOM and MAP_TO_CUSTOM[name]:
            custom = MAP_TO_CUSTOM[name]
            n_pixels = (pred == c).sum()
            counts[custom] += n_pixels

    total = sum(counts.values())
    dominant = max(counts, key=counts.get)
    return {
        'dominant_class': dominant,
        'class_counts': counts,
        'matrix': pred  # For visualization if needed
    }
