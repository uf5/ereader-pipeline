from PIL import Image
from pathlib import Path
from sys import argv
import img2pdf


def downscale(input_dir, output_dir, factor):
    for f in (x for x in input_dir.iterdir() if x.is_file()):
        new_file = output_dir / f.name
        print(f"Processing: {f.name}")
        img = Image.open(f)
        img.thumbnail((int(img.width * factor), int(img.height * factor)), Image.Resampling.LANCZOS)
        img.save(new_file, img.format)


def generate_pdf(input_dir, output_file):
    with open(output_file, "wb") as f:
        f.write(img2pdf.convert(sorted([str(x) for x in input_dir.iterdir() if x.is_file()])))


if __name__ == "__main__":
    input_dir = Path(argv[1])

    downscale_dir = input_dir / "downscaled"
    downscale_dir.mkdir(parents=True, exist_ok=True)

    factor = float(argv[2])

    pdf_file = Path(argv[3])

    downscale(input_dir, downscale_dir, factor)
    print("Downscaling complete.")
    generate_pdf(downscale_dir, pdf_file)
    print(f"Output pdf file: {pdf_file}")

