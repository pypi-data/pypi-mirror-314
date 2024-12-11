from PIL import Image
import dataframe_image as dfi


def create_image_from_bbox(image_path, bbox, output_path=None):
    try:
        with Image.open(image_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            cropped_img = img.crop(bbox)
            if output_path is None:
                filename = image_path.rsplit(".", 1)[0]
                output_path = f"{filename}_cropped.png"
            cropped_img.save(output_path, "PNG")
            return output_path
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None


def create_photo_from_df(df):
    df_styled = (
        df.style.background_gradient()
        .hide(axis="index")
        .set_properties(subset=["Dự án"], **{"text-align": "left"})
        .set_table_styles(
            [
                {
                    "selector": "td, th",
                    "props": [("border", "1px solid grey !important")],
                },
                {
                    "selector": "th",
                    "props": [("text-align", "center !important")],
                },
            ]
        )
    )
    dfi.export(df_styled, "result.png", table_conversion="html2image")
