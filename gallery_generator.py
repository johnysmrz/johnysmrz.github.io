import yaml
from PIL import Image
from pathlib import Path

DATASOURCE = "data/leather/leather.yml"
DESTINATION = "content/leather/"

def load_data():
    with open(DATASOURCE, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def generate_gallery():
    for product in load_data():
        if Path.exists(Path(DESTINATION + product['slug'] + ".md")):
            print("\033[93mSKIPPING\033[0m existing file: " + product['slug'] + ".md")
            continue
        else:
            print("\033[92mCREATING\033[0m file: " + product['slug'] + ".md")

        # resize images and copy them from originals folder
        ORIGINALS = f"static/leather/{product['slug']}/original"
        IMG_FOLDER = f"static/leather/{product['slug']}/"

        images = []

        if Path(ORIGINALS).exists():
            i = 0
            for f in Path(ORIGINALS).iterdir():
                if f.is_file() and f.name.endswith(".jpg"):
                    out_name = f"{product['slug']}-{i}.jpg"
                    resize_image(f, f"{IMG_FOLDER}{out_name}", 1280)
                    images.append(out_name)
                    i += 1

        # generate preview image
        PREVIEW_IMAGE_SOURCE = f"static/leather/{product['slug']}/original/{product['preview_image']}"
        PREVIEW_IMAGE_DEST = f"static/leather/{product['slug']}/{product['slug']}_preview.jpg"

        print("PREVIEW_IMAGE_SOURCE: " + PREVIEW_IMAGE_SOURCE)

        if Path(PREVIEW_IMAGE_SOURCE).exists():
            print("Generating preview image")
            resize_image(PREVIEW_IMAGE_SOURCE, PREVIEW_IMAGE_DEST, 500)


        # write markdown file
        with open(DESTINATION + product['slug'] + ".md", "w") as file:
            file.write("---\n")
            file.write("title: " + product['title'] + "\n")
            file.write("slug: " + product['slug'] + "\n")
            file.write("price: " + str(product['price']) + "\n")
            file.write(f"image: {product['slug']}_preview.jpg \n")

            file.write("images: ['" + "', '".join(images) + "']\n")

            file.write("tags: " + str(product['tags']) + "\n")
            file.write("---\n\n")
            file.write(product['description'] + "\n")
        

def resize_image(image_path, output_path, max_size=1080):
    with Image.open(image_path) as img:
        width, height = img.size

        if width > height:
            scale = max_size / width
        else:
            scale = max_size / height

        print(f"Resizing {image_path} to {int(width * scale)}x{int(height * scale)}")

        resized_img = img.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)
        resized_img.save(output_path)


if __name__ == "__main__":
    generate_gallery()