import os
from loguru import logger
class Helper:
    def get_font_names(self,fonts_folder="./utils/fonts"):
        """
        Returns a list of font names from the specified in the fonts folder.
        :param fonts_folder: Path to the folder containing font files (default: 'fonts').
        :return: List of font names.
        """
        logger.info("fetching available fonts ")
        font_extensions = ['.ttf', '.otf', '.woff', '.woff2']
        if not os.path.exists(fonts_folder):
            raise FileNotFoundError(f"The folder '{fonts_folder}' does not exist.")
        font_files = os.listdir(fonts_folder)
        font_names = []
        for file_name in font_files:
            if any(file_name.lower().endswith(ext) for ext in font_extensions):
                font_name = os.path.splitext(file_name)[0]
                font_names.append(font_name)
        print(font_names)
        return font_names