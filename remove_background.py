import argparse
import os
import io
from rembg import remove, new_session
from PIL import Image


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def process_single_image(input_path, output_dir):


    filename = os.path.basename(input_path)
    filename_no_ext = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"{filename_no_ext}.png")
    try:

        session = new_session("u2net_human_seg")

        with open(input_path, 'rb') as i:
            input_data = i.read()

        output_data = remove(input_data, session=session)

        img = Image.open(io.BytesIO(output_data))
        img.save(output_path)

    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert portrait image to transparent png")

    parser.add_argument("input_image", type=str, help="path to the source image file")
    parser.add_argument("output_dir", type=str, help="folder to save the result")

    args = parser.parse_args()

    process_single_image(args.input_image, args.output_dir)