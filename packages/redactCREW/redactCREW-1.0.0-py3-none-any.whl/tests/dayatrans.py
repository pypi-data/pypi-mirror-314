import re
import sys
import os
import numpy as np
import logging
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import easyocr
from pdf2image import convert_from_path

def setup_logging(output_dir='output', log_file='results.log'):
    """
    Sets up logging to output to both console and a file.

    Args:
        output_dir (str): Directory where the log file will be saved.
        log_file (str): Name of the log file.

    Returns:
        logger (logging.Logger): Configured logger object.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    logger = logging.getLogger('TextExtractionNER')
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler
    file_handler = logging.FileHandler(os.path.join(output_dir, log_file), mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def extract_text_with_bboxes(input_image, languages=['hi', 'en']):
    """
    Extract text and bounding boxes from an image using EasyOCR.

    Args:
        input_image (PIL.Image.Image): PIL Image object.
        languages (list): List of languages to be used by EasyOCR.

    Returns:
        list of tuples: Each tuple contains (bounding_box, text, confidence).
    """
    reader = easyocr.Reader(languages, gpu=False)  # Set gpu=True if GPU is available
    results = reader.readtext(np.array(input_image), detail=1, paragraph=False)
    return results

def filter_ocr_results(ocr_results, image_width, image_height):
    """
    Filter OCR results to include only Hindi text, excluding numbers, English letters, and unwanted special characters.

    Args:
        ocr_results (list of tuples): Each tuple contains (bounding_box, text, confidence).
        image_width (int): Width of the image in pixels.
        image_height (int): Height of the image in pixels.

    Returns:
        list of dicts: Each dict contains 'text' and 'bbox' for filtered OCR results.
    """
    filtered = []
    pattern = re.compile(r'^[\u0900-\u097F।\s]+$')  # Only Hindi characters and '।'

    for result in ocr_results:
        bbox, text, conf = result
        # Remove leading/trailing spaces
        text = text.strip()
        if not text:
            continue
        # Check if text contains only Hindi characters and '।'
        if pattern.match(text):
            # Compute a single bounding box (min_x, min_y, max_x, max_y)
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            min_x, min_y = min(x_coords), min(y_coords)
            max_x, max_y = max(x_coords), max(y_coords)
            # Normalize coordinates to [0,1]
            normalized_bbox = (
                (np.float64(min_x / image_width), np.float64(min_y / image_height)),
                (np.float64(max_x / image_width), np.float64(max_y / image_height))
            )
            filtered.append({
                'text': text,
                'bbox': normalized_bbox
            })
    return filtered

def preprocess_text(filtered_ocr):
    """
    Preprocess the filtered OCR text by removing Hindi digits, special characters (except '।'), normalizing whitespace, and adding newlines.

    Args:
        filtered_ocr (list of dicts): Each dict contains 'text' and 'bbox'.

    Returns:
        tuple: (cleaned_text, word_info_list)
            - cleaned_text (str): The concatenated cleaned text.
            - word_info_list (list of dicts): Each dict contains 'text', 'bbox', 'start', 'end'.
    """
    cleaned_text = ""
    word_info_list = []
    current_pos = 0

    for entry in filtered_ocr:
        text = entry['text']
        bbox = entry['bbox']

        # Remove Hindi digits (०-९)
        text = re.sub(r'[०-९]', '', text)

        # Remove special characters except '।'
        text = re.sub(r'[^\u0900-\u097F।\s]', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        if not text:
            continue

        # Add space if not the first word
        if cleaned_text:
            cleaned_text += ' '
            current_pos += 1  # For the space

        # Record start and end positions
        start = current_pos
        end = start + len(text)
        cleaned_text += text
        word_info_list.append({
            'text': text,
            'bbox': bbox,
            'start': start,
            'end': end
        })
        current_pos = end

    # Add newlines after '।' to separate sentences
    cleaned_text = cleaned_text.replace('।', '।\n')

    return cleaned_text, word_info_list

def perform_ner(cleaned_text, model_name="ai4bharat/IndicNER", logger=None):
    """
    Perform Named Entity Recognition on the cleaned text to detect person names.

    Args:
        cleaned_text (str): The preprocessed Hindi text.
        model_name (str): Hugging Face model name for NER.
        logger (logging.Logger): Logger object for logging messages.

    Returns:
        list of dicts: Each dict contains 'name', 'confidence', 'start', 'end'.
    """
    try:
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)
    except OSError as e:
        if logger:
            logger.error(f"Error loading the model '{model_name}': {e}")
            logger.error("Please ensure the model name is correct and you have internet connectivity.")
        else:
            print(f"Error loading the model '{model_name}': {e}")
            print("Please ensure the model name is correct and you have internet connectivity.")
        sys.exit(1)

    # Initialize NER pipeline
    ner_pipeline = pipeline(
        "token-classification",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple",
        device=-1  # Use CPU. Set to 0 if using GPU.
    )

    # Perform NER
    ner_results = ner_pipeline(cleaned_text)

    # Extract person entities
    person_entities = []
    for entity in ner_results:
        if entity["entity_group"] == "PER":
            person_name = entity["word"].replace("##", "")
            confidence = entity["score"]
            start = entity["start"]
            end = entity["end"]
            person_entities.append({
                "name": person_name,
                "confidence": confidence,
                "start": start,
                "end": end
            })

    return person_entities

def map_entities_to_bboxes(person_entities, word_info_list):
    """
    Map detected person entities to their corresponding bounding boxes.

    Args:
        person_entities (list of dicts): Each dict contains 'name', 'confidence', 'start', 'end'.
        word_info_list (list of dicts): Each dict contains 'text', 'bbox', 'start', 'end'.

    Returns:
        list of dicts: Each dict contains 'name', 'confidence', and 'bounding_boxes'.
    """
    mapped_entities = []

    for entity in person_entities:
        name = entity['name']
        confidence = entity['confidence']
        start = entity['start']
        end = entity['end']

        # Find words that fall within the entity span
        bboxes = []
        for word in word_info_list:
            word_start = word['start']
            word_end = word['end']
            # Check if word overlaps with entity span
            if not (word_end <= start or word_start >= end):
                bboxes.append(word['bbox'])

        mapped_entities.append({
            "name": name,
            "confidence": confidence,
            "bounding_boxes": bboxes
        })

    return mapped_entities

def draw_bounding_boxes(input_image, mapped_entities, image_width, image_height, output_dir='output', annotated_image_name='annotated_image.jpg'):
    """
    Draw bounding boxes around detected person names on the original image and save it.

    Args:
        input_image (PIL.Image.Image): PIL Image object.
        mapped_entities (list of dicts): Each dict contains 'name', 'confidence', and 'bounding_boxes'.
        image_width (int): Width of the image in pixels.
        image_height (int): Height of the image in pixels.
        output_dir (str): Directory where the annotated image will be saved.
        annotated_image_name (str): Name of the annotated image file.
    """
    img = input_image.copy()
    draw = ImageDraw.Draw(img)

    # Optional: Choose a font and size
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except IOError:
        # If the specified font is not found, use the default font
        font = ImageFont.load_default()

    for entity in mapped_entities:
        name = entity["name"]
        confidence = entity["confidence"]
        bboxes = entity["bounding_boxes"]

        for bbox in bboxes:
            # Convert normalized coordinates back to pixel values
            (min_x_norm, min_y_norm), (max_x_norm, max_y_norm) = bbox
            min_x = int(min_x_norm * image_width)
            min_y = int(min_y_norm * image_height)
            max_x = int(max_x_norm * image_width)
            max_y = int(max_y_norm * image_height)

            # Define the rectangle's top-left and bottom-right points
            top_left = (min_x, min_y)
            bottom_right = (max_x, max_y)

            # Draw the rectangle
            draw.rectangle([top_left, bottom_right], outline="red", width=2)

            # Add the name label above the bounding box using textbbox()
            text = f"{name} ({confidence:.2f})"
            text_position = (min_x, max(min_y - 20, 0))  # Position text above the box

            # Calculate text size using textbbox()
            text_bbox = draw.textbbox(text_position, text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Draw a filled rectangle behind the text for better visibility
            draw.rectangle(
                [text_position, (text_position[0] + text_width, text_position[1] + text_height)],
                fill="red"
            )

            # Draw the text over the rectangle
            draw.text(text_position, text, fill="white", font=font)

    # Save the annotated image
    annotated_image_path = os.path.join(output_dir, annotated_image_name)
    img.save(annotated_image_path)
    return img  # Return the annotated image for PDF compilation

def save_annotated_pdf(annotated_images, output_dir='output', annotated_pdf_name='annotated_document.pdf'):
    """
    Save a list of annotated images as a single PDF.

    Args:
        annotated_images (list of PIL.Image.Image): List of annotated PIL Image objects.
        output_dir (str): Directory where the PDF will be saved.
        annotated_pdf_name (str): Name of the annotated PDF file.
    """
    if not annotated_images:
        print("No annotated images to save as PDF.")
        return

    # Ensure all images are in RGB mode
    rgb_images = [img.convert('RGB') for img in annotated_images]

    # Save as PDF
    annotated_pdf_path = os.path.join(output_dir, annotated_pdf_name)
    rgb_images[0].save(annotated_pdf_path, save_all=True, append_images=rgb_images[1:])
    print(f"Annotated PDF saved at: {annotated_pdf_path}")

def process_image(input_image, logger, model_name, output_dir):
    """
    Process a single image: extract text, perform NER, map entities, draw bounding boxes, and return annotated image.

    Args:
        input_image (PIL.Image.Image): PIL Image object.
        logger (logging.Logger): Logger object for logging messages.
        model_name (str): Hugging Face model name for NER.
        output_dir (str): Directory where outputs will be saved.

    Returns:
        PIL.Image.Image: Annotated PIL Image object.
    """
    image_width, image_height = input_image.size

    # Step 1: Extract Text and Bounding Boxes using EasyOCR
    logger.info("Extracting text and bounding boxes from the image...")
    ocr_results = extract_text_with_bboxes(input_image)

    # Combine text pieces into one string for display
    extracted_text = ' '.join([result[1].strip() for result in ocr_results if result[1].strip()])
    logger.info("\n--- Original Extracted Text ---\n")
    logger.info(extracted_text)

    # Step 2: Filter OCR Results
    logger.info("\nFiltering OCR results to include only Hindi text...")
    filtered_ocr = filter_ocr_results(ocr_results, image_width, image_height)

    if not filtered_ocr:
        logger.info("No Hindi text detected after filtering.")
        return input_image  # Return original image if no text detected

    # Step 3: Preprocess the Extracted Text
    logger.info("\nPreprocessing the extracted text...")
    cleaned_text, word_info_list = preprocess_text(filtered_ocr)
    logger.info("\n--- Cleaned and Preprocessed Text ---\n")
    logger.info(cleaned_text)

    # Step 4: Perform Named Entity Recognition (NER)
    logger.info("\nPerforming Named Entity Recognition to detect person names...")
    person_entities = perform_ner(cleaned_text, model_name=model_name, logger=logger)

    # Step 5: Map Entities to Bounding Boxes
    logger.info("\nMapping detected entities to bounding boxes...")
    mapped_entities = map_entities_to_bboxes(person_entities, word_info_list)

    # Step 6: Draw Bounding Boxes on the Image
    if mapped_entities:
        logger.info("\n--- Detected Person Names with Bounding Boxes ---\n")
        for idx, entity in enumerate(mapped_entities, start=1):
            name = entity["name"]
            confidence = entity["confidence"]
            bboxes = entity["bounding_boxes"]
            logger.info(f"Text: {name}")
            for bbox in bboxes:
                logger.info(f"Bounding Box: ((np.float64({bbox[0][0]}), np.float64({bbox[0][1]})), "
                            f"(np.float64({bbox[1][0]}), np.float64({bbox[1][1]})))")
            logger.info("")  # Add an empty line for better readability

        # Draw bounding boxes on the image
        logger.info("Drawing bounding boxes on the image...")
        annotated_image = draw_bounding_boxes(input_image, mapped_entities, image_width, image_height, output_dir)
    else:
        logger.info("\nNo person names detected in the text.")
        annotated_image = input_image  # Return original image if no entities detected

    return annotated_image

def main():
    # -----------------------
    # Configuration
    # -----------------------
    # Replace this path with your actual file path (image or PDF)
    input_file = 'adhaar.pdf'  # e.g., 'documents/sample.pdf' or 'images/sample.jpg'

    # Specify the output directory and log file name
    output_dir = 'output'
    log_file = 'results.log'
    annotated_pdf_name = 'annotated_document.pdf'

    # Setup logging
    logger = setup_logging(output_dir, log_file)

    # Check if the input file exists
    if not os.path.isfile(input_file):
        logger.error(f"Input file '{input_file}' does not exist. Please provide a valid file path.")
        sys.exit(1)

    # Determine file type
    file_extension = os.path.splitext(input_file)[1].lower()

    # Specify the NER model name. Replace with a valid model if 'ai4bharat/IndicNER' is unavailable.
    model_name = "ai4bharat/IndicNER"

    annotated_images = []  # To store annotated images for PDF

    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        # Handle image files
        logger.info(f"Processing image file: {input_file}")
        try:
            with Image.open(input_file) as img:
                annotated_image = process_image(img, logger, model_name, output_dir)
                annotated_images.append(annotated_image)
                
                # Save annotated image
                annotated_image_path = os.path.join(output_dir, 'annotated_image.jpg')
                annotated_image.save(annotated_image_path)
                logger.info(f"Annotated image saved at: {annotated_image_path}")
        except Exception as e:
            logger.error(f"Error processing image file '{input_file}': {e}")
            sys.exit(1)

    elif file_extension == '.pdf':
        # Handle PDF files
        logger.info(f"Processing PDF file: {input_file}")
        try:
            # Convert PDF pages to images
            pages = convert_from_path(input_file)
            logger.info(f"Total pages found in PDF: {len(pages)}")

            for page_number, page in enumerate(pages, start=1):
                logger.info(f"\n--- Processing Page {page_number} ---\n")
                annotated_image = process_image(page, logger, model_name, output_dir)
                annotated_images.append(annotated_image)
                
                # Save annotated image for the page
                annotated_image_path = os.path.join(output_dir, f'annotated_page_{page_number}.jpg')
                annotated_image.save(annotated_image_path)
                logger.info(f"Annotated page {page_number} saved at: {annotated_image_path}")

            # After processing all pages, compile annotated images into a single PDF
            logger.info("\nCompiling annotated images into a single PDF...")
            save_annotated_pdf(annotated_images, output_dir, annotated_pdf_name)
        except Exception as e:
            logger.error(f"Error processing PDF file '{input_file}': {e}")
            sys.exit(1)

    else:
        logger.error("Unsupported file format. Please provide an image file (e.g., .jpg, .png) or a PDF file.")
        sys.exit(1)

    # End of script
    logger.info("\nProcessing completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
