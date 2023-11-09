from PIL import Image
from pathlib import Path
import img2pdf
import argparse
import zipfile as zf
import tempfile as tf
from multiprocessing import Pool


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ereader-pipeline", description="downscale and convert .cbz to .pdf"
    )
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("-f", "--factor", type=float, default=0.7, metavar="f")

    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)
    factor = args.factor

    with tf.TemporaryDirectory() as dir_scans:
        # extract
        with zf.ZipFile(input_file) as zfile:
            zfile.extractall(dir_scans)
        # downscale
        with tf.TemporaryDirectory() as dir_downscaled:
            dir_downscaled_p = Path(dir_downscaled)

            def downscale_image(page):
                downscaled_path = dir_downscaled_p / page.name
                print(f"processing: {page.name}")
                img = Image.open(page)
                img.thumbnail(
                    (int(img.width * factor), int(img.height * factor)),
                    Image.Resampling.LANCZOS,
                )
                img.save(downscaled_path, img.format)

            pool = Pool()
            pool.map(downscale_image, filter(Path.is_file, Path(dir_scans).iterdir()))

            print("downscaling complete")
            # combine images into pdf
            with open(output_file, "wb") as f:
                f.write(img2pdf.convert(sorted([str(x) for x in dir_downscaled_p.iterdir() if x.is_file()])))  # type: ignore
            print(f"output pdf file: {output_file}")
