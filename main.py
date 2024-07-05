from config import dp
from aiogram.utils import executor
import logging
from handlers import comands, echo

comands.register_commands(dp)

#this is echo function you must call it only at the end
echo.register_commands(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)