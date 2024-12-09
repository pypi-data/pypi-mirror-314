import os
import sys
import pikepdf
from PIL import Image
from datetime import datetime, timedelta
import subprocess
from pypdf import PdfReader, PdfWriter


class FileEase:
    _allowed_file_types: list[str] = ["doc", "docx", "ppt", "pptx"]
    _allowed_image_file_types: list[str] = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]

    def __init__(self):
        self.libreoffice_path = os.getenv("LIBREOFFICE_PATH")
        if self.libreoffice_path is None:
            self.libreoffice_path: str = "libreoffice"
        if sys.platform == "win32":
            self.libreoffice_path: str = self.__get_libreoffice_path()


    def __convert_to_pdf(self, input_file: str, output_folder: str, output_file_name: str = None) -> bool:
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        if not os.path.isdir(output_folder):
            raise FileNotFoundError(f"Output folder '{output_folder}' not found.")
        if os.path.splitext(input_file)[1][1:] not in self._allowed_file_types or not os.path.isfile(input_file):
            raise ValueError(f"Input file '{input_file}' is not a valid document file.")
        try:
            subprocess.run(
                [self.libreoffice_path, "--headless", "--convert-to", "pdf", input_file, "--outdir", output_folder],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if output_file_name is not None:
                os.rename(os.path.join(output_folder, os.path.basename(input_file)), os.path.join(output_folder, output_file_name))
            return True
        except (FileNotFoundError, Exception):
            return False

    @staticmethod
    def __parse_pdf_date(date_string: str) -> datetime:
        if date_string.startswith("D:"):
            date_string: str = date_string[2:]
        if date_string.endswith("Z"):
            return datetime.strptime(date_string, "%Y%m%d%H%M%SZ")
        else:
            main_part: str = date_string[:14]
            tz_part: str = date_string[14:]
            dt = datetime.strptime(main_part, "%Y%m%d%H%M%S")
            if tz_part:
                sign: int = 1 if tz_part[0] == '+' else -1
                hours: int = int(tz_part[1:3])
                minutes: int = int(tz_part[4:6])
                offset: timedelta = timedelta(hours=hours, minutes=minutes)
                dt -= sign * offset
            return dt

    def get_pdf_info(self, file_path: str) -> dict:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Input file '{file_path}' not found.")
        reader = PdfReader(file_path)
        metadata = reader.metadata
        num_pages = len(reader.pages)
        pdf_info = {
            "title": metadata.get("/Title", "Unknown"),
            "author": metadata.get("/Author", "Unknown"),
            "subject": metadata.get("/Subject", "Unknown"),
            "creator": metadata.get("/Creator", "Unknown"),
            "producer": metadata.get("/Producer", "Unknown"),
            "created_on": self.__parse_pdf_date(metadata.get("/CreationDate", "Unknown")),
            "modified_on": self.__parse_pdf_date(metadata.get("/ModDate", "Unknown")),
            "pages": num_pages
        }
        return pdf_info

    @staticmethod
    def __get_libreoffice_path() -> str:
        for path in os.getenv("PATH").split(os.pathsep):
            full_path: str = os.path.join(path, "soffice.exe")
            if os.path.isfile(full_path):
                return full_path
        return ""

    def images_to_pdf(self, input_path: list[str], output_path: str, output_pdf_name: str) -> bool:
        images: list[Image] = []
        if not output_pdf_name:
            output_pdf_name = "output"
        for img_path in input_path:
            if os.path.splitext(img_path)[1][1:] not in self._allowed_image_file_types:
                raise ValueError(f"Input file '{img_path}' is not a valid image file.")
            img: Image = Image.open(img_path)
            if img.mode != "RGB":
                img: Image = img.convert("RGB")
            images.append(img)
        images[0].save(output_path + os.path.basename(output_pdf_name) + ".pdf", save_all=True, append_images=images[1:], resolution=100.0, quality=95)
        return True

    def doc_to_pdf(self, input_file: str, output_folder: str) -> bool:
        """
            Converts a document file to a PDF file. Supported formats: `doc`, `docx`.
            :param input_file: The path to the input document file.
            :param output_folder: The path to the output folder.
            :return: True if the conversion was successful, False otherwise.
        """
        return self.__convert_to_pdf(input_file, output_folder)

    def ppt_to_pdf(self, input_file: str, output_folder: str) -> bool:
        """
            Converts a Presentation file to a PDF file. Supported formats: `ppt`, `pptx`.
            :param input_file: The path to the input document file.
            :param output_folder: The path to the output folder.
            :return: True if the conversion was successful, False otherwise.
        """
        return self.__convert_to_pdf(input_file, output_folder)

    @staticmethod
    def merge_pdfs(input_files: list[str], output_path: str, output_pdf_name: str = "") -> bool:
        """
            Merges multiple PDF files into a single PDF file.
            :param input_files: A list of input PDF files.
            :param output_path: The path to the output folder.
            :param output_pdf_name: The name of the output PDF file.
            :return: True if the merging was successful, False otherwise.
        """
        if not output_pdf_name:
            output_pdf_name = "merged_" + os.path.basename(input_files[0])
        merger = PdfWriter()
        for file in input_files:
            if not os.path.isfile(file) or os.path.splitext(file)[1][1:] != "pdf":
                raise ValueError(f"Input file '{file}' is not a valid document file.")
            merger.append(file)
        merger.write(output_path + os.path.basename(output_pdf_name) + ".pdf")
        merger.close()
        return True

    @staticmethod
    def compress_pdfs(input_file: list[str], output_path: str, output_pdf_name: str = "") -> bool:
        """
            Compresses multiple PDF files into a single PDF file.
            :param input_file: A list of input PDF files.
            :param output_path: The path to the output folder.
            :param output_pdf_name: The name of the output PDF file.
            :return: True if the compression was successful, False otherwise.

        """
        for file in input_file:
            if not os.path.isfile(file) or os.path.splitext(file)[1][1:] != "pdf":
                raise ValueError(f"Input file '{file}' is not a valid document file.")
            try:
                with pikepdf.open(file) as pdf:
                    if not output_pdf_name:
                        output_pdf_name = "compressed_" + os.path.basename(file)
                    pdf.save(output_path + os.path.basename(output_pdf_name) + ".pdf")
                    return True
            except Exception as e:
                return False