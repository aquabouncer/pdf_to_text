import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import PIL.Image
import pytesseract
from wand.image import Image as wi

directory = os.getcwd()
pdf_path = os.path.join(directory, 'pdf_here')
text_path = os.path.join(directory, 'text_output')


def getTxt(filename):
    # uses PyPDF2 to read the contents of a pdf file
    pdf = PdfFileReader(filename)
    with open(filename, "r", encoding='UTF-8') as f:
        for page in range(pdf.numPages):
            page_obj = pdf.getPage(page)
            txt = page_obj.extractText()
            return txt


def image_recognition(filename, clean_file_name):
    # takes a picture of the pdf with wand and then uses pytesseract to turn the image into text and returns the text

    # this is a config setting for the image recognition. 6 seems to work best for general pdf files. you can test
    # whatever you want with the numbers range 1-12. you can google pytesseract config settings for the psm.
    # do not bother changing oem
    myconfig = r"--psm 6 --oem 3"

    # changing the resolution for the pdf file image does increase results 800 seems to do ok but larger
    # resolution takes more time. tinker with it to find the best results for your needs
    pdf_file = wi(filename=filename, resolution=800)

    for img in pdf_file.sequence:
        process_image = wi(image=img)
        output_file_name = f"{clean_file_name}.jpg"
        process_image.save(filename=output_file_name)
        text = pytesseract.image_to_string(PIL.Image.open(output_file_name), config=myconfig)
        os.remove(output_file_name)
        return text


def main():
    # makes folder if it does not exist
    if not os.path.exists("pdf_here"):
        os.mkdir("pdf_here")

    if not os.path.exists("text_output"):
        os.mkdir("text_output")

    for filename in os.listdir(pdf_path):
        os.chdir(pdf_path)
        # remove pdf file extension and get clean file name
        # you could also get the file extension with the index of 1 if needed
        clean_file_name = os.path.splitext(filename)[0]

        # calling function to extract pdf text
        got_txt = getTxt(filename)

        # if the pdf file contents were empty we call the image recognition function
        if len(got_txt) == 0:
            ir = image_recognition(filename, clean_file_name)
            os.chdir(text_path)
            with open(f'{clean_file_name}.txt', 'w', encoding='UTF-8') as f:
                f.write(ir)

        else:
            os.chdir(text_path)
            with open(f'{clean_file_name}.txt', 'w', encoding='UTF-8') as f:
                f.write(got_txt)


if __name__ == '__main__':
    main()
