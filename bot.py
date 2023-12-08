import tempfile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InputFile
from configs import LoadConfigs, GetToken
from io import BytesIO
import logging, qrcode
from PIL import Image, ImageDraw
from qrcode.image import svg
import base64
from qrcode.image.svg import SvgPathImage
import svgwrite

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.svg import SvgPathSquareDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from decimal import *

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Configurazione di logging base
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def generaQR(link : str) -> InputFile:    

    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Usa SvgPathImage per generare un QR code in formato SVG
    img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="./images/ateneo.png", fill_color="black", back_color="Transparent",)
    
    img_byte_array = BytesIO()
    
    # Salva il contenuto SVG in un BytesIO
    img.save(img_byte_array)
    img_byte_array.seek(0)

    # Opzionalmente, puoi anche scrivere il contenuto SVG in un file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file.write(img_byte_array.getvalue())

    # Restituisci l'oggetto BytesIO contenente il contenuto SVG
    return InputFile(open(temp_file.name, 'rb'), filename="TuoQRCode.png")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ciao! Usa /creaqr <link> per creare un QR code!")

async def creaQR(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:

        link = context.args[0]
        input_file : InputFile = generaQR(link=link) 

        await update.message.reply_document(
            document=input_file,
            caption="Ecco a te il tuo QR code!"
        )

    except (IndexError, ValueError):

        await update.effective_message.reply_text("Uso: /creaqr <link>")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    LoadConfigs()
    application = Application.builder().token(GetToken()).build()

    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CommandHandler("creaqr", creaQR))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()