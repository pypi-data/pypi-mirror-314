import os
import subprocess
import sys


def set_video_thumbnail():
    """
    Устанавливает изображение как обложку для видео с использованием ffmpeg.
    """
    # Получаем путь к видео файлу
    video_path = input("Введите путь к видео файлу: ")
    if not os.path.exists(video_path):
        print("Ошибка: Видео файл не найден.")
        return

    # Получаем путь к изображению для обложки
    image_path = input("Введите путь к изображению для обложки: ")
    if not os.path.exists(image_path):
        print("Ошибка: Файл изображения не найден.")
        return

    # Получаем имя выходного файла
    output_filename = input("Введите имя выходного файла (с расширением): ")

    # Формируем команду ffmpeg
    command = [
        "ffmpeg",
        "-i", video_path,
        "-i", image_path,
        "-map", "0",
        "-map", "1",
        "-c", "copy",
        "-disposition:v:1", "attached_pic",
        output_filename
    ]

    # Выполняем команду
    try:
        subprocess.run(command, check=True)
        print(f"Обложка успешно установлена. Файл сохранен как {output_filename}")
    except subprocess.CalledProcessError:
        print("Произошла ошибка при выполнении команды ffmpeg.")
    except FileNotFoundError:
        print("Ошибка: ffmpeg не найден. Убедитесь, что ffmpeg установлен и доступен в системном пути.")


def main():
    """
    Основная функция запуска скрипта.
    """
    print("Made By Avinion")
    print("Telegram: @akrim")

    # Выбор языка
    language = input("English (E) or Russian (R)? ").upper()
    if language not in ["E", "R"]:
        print("Invalid input. Exiting.")
        sys.exit()

    # Запуск основного процесса
    while True:
        set_video_thumbnail()
        continue_script = input("Do you want to continue? (Y/N) ").upper()
        if continue_script == "N":
            print("Goodbye!")
            break
        elif continue_script == "Y":
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
