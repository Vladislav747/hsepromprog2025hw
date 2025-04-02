#!/bin/bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input_folder)
      INPUT_FOLDER="$2"
      shift 2
      ;;
    --extension)
      EXTENSION="$2"
      shift 2
      ;;
    --backup_folder)
      BACKUP_FOLDER="$2"

      shift 2
      ;;
    --backup_archive_name)
      BACKUP_ARCHIVE_NAME="$2"
      shift 2
      ;;
    *)
      echo "Неизвестный параметр: $1"
      exit 1
      ;;
  esac
done


if [[ -z "$INPUT_FOLDER" || -z "$EXTENSION" || -z "$BACKUP_FOLDER" || -z "$BACKUP_ARCHIVE_NAME" ]]; then
  echo "Ошибка: не все параметры переданы!"
  echo "Использование: ./run.sh --input_folder <путь> --extension <расширение> --backup_folder <папка> --backup_archive_name <архив.tar.gz>"
  exit 1
fi

if [[ -d "$BACKUP_FOLDER" ]]; then
  rm -rf "$BACKUP_FOLDER"
fi

mkdir -p "$BACKUP_FOLDER"

find "$INPUT_FOLDER" -type f -name "*.$EXTENSION" -exec cp {} "$BACKUP_FOLDER" \;

if [[ -f "$BACKUP_ARCHIVE_NAME" ]]; then
  rm "$BACKUP_ARCHIVE_NAME"
fi

tar -czf "$BACKUP_ARCHIVE_NAME" "$BACKUP_FOLDER"

echo "done"