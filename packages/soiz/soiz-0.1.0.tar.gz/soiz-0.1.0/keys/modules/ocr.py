from pathlib import Path
from typing import List
from PIL import Image

# Import modules for specific tasks
import pypdfium2
from surya.detection import batch_text_detection
from surya.input.pdflines import get_page_text_lines, get_table_blocks
from surya.layout import batch_layout_detection
from surya.ocr import run_ocr
from surya.input.langs import replace_lang_with_code
from surya.settings import settings
from surya.tables import batch_table_recognition
from surya.postprocessing.util import rescale_bbox
from surya.postprocessing.heatmap import draw_polys_on_image, draw_bboxes_on_image
from surya.postprocessing.text import draw_text_on_image


def load_models():
    """Load all required models."""
    from surya.model.detection.model import load_model, load_processor
    from surya.model.layout.model import load_model as load_layout_model
    from surya.model.layout.processor import load_processor as load_layout_processor
    from surya.model.recognition.model import load_model as load_rec_model
    from surya.model.recognition.processor import load_processor as load_rec_processor
    from surya.model.table_rec.model import load_model as load_table_model
    from surya.model.table_rec.processor import load_processor as load_table_processor

    det_model, det_processor = load_model(), load_processor()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()
    layout_model, layout_processor = load_layout_model(), load_layout_processor()
    table_model, table_processor = load_table_model(), load_table_processor()

    return (
        det_model,
        det_processor,
        rec_model,
        rec_processor,
        layout_model,
        layout_processor,
        table_model,
        table_processor,
    )


def text_detection(img, det_model, det_processor):
    """Run text detection on an image."""
    pred = batch_text_detection([img], det_model, det_processor)[0]
    polygons = [p.polygon for p in pred.bboxes]
    det_img = draw_polys_on_image(polygons, img.copy())
    return det_img, pred, polygons


def layout_detection(img, layout_model, layout_processor):
    """Run layout detection on an image."""
    pred = batch_layout_detection([img], layout_model, layout_processor)[0]
    polygons = [p.polygon for p in pred.bboxes]
    bboxes = [p.bbox for p in pred.bboxes]
    labels = [f"{p.label}-{p.position}" for p in pred.bboxes]
    layout_img = draw_polys_on_image(
        polygons, img.copy(), labels=labels, label_font_size=12
    )
    return polygons, labels, layout_img, pred, bboxes


def table_recognition(
    img,
    highres_img,
    filepath,
    page_idx,
    use_pdf_boxes,
    skip_table_detection,
    det_model,
    det_processor,
    layout_model,
    layout_processor,
    table_model,
    table_processor,
):
    """Run table recognition on an image."""
    if skip_table_detection:
        layout_tables = [(0, 0, highres_img.size[0], highres_img.size[1])]
        table_imgs = [highres_img]
    else:
        _, layout_pred = layout_detection(img, layout_model, layout_processor)
        layout_tables_lowres = [
            l.bbox for l in layout_pred.bboxes if l.label == "Table"
        ]
        table_imgs = []
        layout_tables = []
        for tb in layout_tables_lowres:
            highres_bbox = rescale_bbox(tb, img.size, highres_img.size)
            table_imgs.append(highres_img.crop(highres_bbox))
            layout_tables.append(highres_bbox)

    try:
        page_text = get_page_text_lines(filepath, [page_idx], [highres_img.size])[0]
        table_bboxes = get_table_blocks(layout_tables, page_text, highres_img.size)
    except Exception:
        table_bboxes = [[] for _ in layout_tables]

    if not use_pdf_boxes or any(len(tb) == 0 for tb in table_bboxes):
        det_results = batch_text_detection(table_imgs, det_model, det_processor)
        table_bboxes = [
            [{"bbox": tb.bbox, "text": None} for tb in det_result.bboxes]
            for det_result in det_results
        ]

    table_preds = batch_table_recognition(
        table_imgs, table_bboxes, table_model, table_processor
    )
    table_img = img.copy()

    for results, table_bbox in zip(table_preds, layout_tables):
        adjusted_bboxes = []
        labels = []
        colors = []

        for item in results.rows + results.cols:
            adjusted_bboxes.append(
                [
                    (item.bbox[0] + table_bbox[0]),
                    (item.bbox[1] + table_bbox[1]),
                    (item.bbox[2] + table_bbox[0]),
                    (item.bbox[3] + table_bbox[1]),
                ]
            )
            labels.append(item.label)
            colors.append("blue" if hasattr(item, "row_id") else "red")

        table_img = draw_bboxes_on_image(
            adjusted_bboxes,
            highres_img,
            labels=labels,
            label_font_size=18,
            color=colors,
        )
    return table_img, table_preds


def ocr(
    img,
    highres_img,
    langs: List[str],
    det_model,
    det_processor,
    rec_model,
    rec_processor,
):
    """Run OCR on an image."""
    replace_lang_with_code(langs)
    img_pred = run_ocr(
        [img],
        [langs],
        det_model,
        det_processor,
        rec_model,
        rec_processor,
        highres_images=[highres_img],
    )[0]

    bboxes = [l.bbox for l in img_pred.text_lines]
    text = [l.text for l in img_pred.text_lines]
    rec_img = draw_text_on_image(
        bboxes, text, img.size, langs, has_math="_math" in langs
    )
    return rec_img, img_pred, text


def process_file(
    filepath: str,
    page_number: int = None,
    languages: List[str] = None,
    operation: str = "ocr",
    use_pdf_boxes: bool = True,
    skip_table_detection: bool = False,
    output_dir: str = "output",
):
    """Process a single file with the specified operation."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    (
        det_model,
        det_processor,
        rec_model,
        rec_processor,
        layout_model,
        layout_processor,
        table_model,
        table_processor,
    ) = load_models()

    if filepath.lower().endswith(".pdf"):
        pdf = pypdfium2.PdfDocument(filepath)
        if page_number is None:
            page_number = 1
        renderer = pdf.render(
            pypdfium2.PdfBitmap.to_pil,
            page_indices=[page_number - 1],
            scale=settings.IMAGE_DPI / 72,
        )
        pil_image = list(renderer)[0].convert("RGB")

        renderer_highres = pdf.render(
            pypdfium2.PdfBitmap.to_pil,
            page_indices=[page_number - 1],
            scale=settings.IMAGE_DPI_HIGHRES / 72,
        )
        pil_image_highres = list(renderer_highres)[0].convert("RGB")
    else:
        pil_image = Image.open(filepath).convert("RGB")
        pil_image_highres = pil_image
        page_number = None

    if operation == "text_detection":
        result_img, pred, polygons = text_detection(pil_image, det_model, det_processor)
        return result_img, pred, polygons
    elif operation == "layout":
        return layout_detection(pil_image, layout_model, layout_processor)
    elif operation == "ocr":
        return ocr(
            pil_image,
            pil_image_highres,
            languages or [],
            det_model,
            det_processor,
            rec_model,
            rec_processor,
        )
    elif operation == "table":
        result_img, pred = table_recognition(
            pil_image,
            pil_image_highres,
            filepath,
            page_number - 1 if page_number else None,
            use_pdf_boxes,
            skip_table_detection,
            det_model,
            det_processor,
            layout_model,
            layout_processor,
            table_model,
            table_processor,
        )
        # result_img.save(output_dir / f"{input_filename}_table.png")
        # with open(output_dir / f"{input_filename}_table.json", "w") as f:
        #     json.dump([p.model_dump() for p in pred], f, indent=2)
