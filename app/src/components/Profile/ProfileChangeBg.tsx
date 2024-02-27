import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import styles from '@/pages/Profile/Proflie.module.sass';
import ChangePhoto from '../SVG/ChangePhoto';
import { useRef, useState } from 'react';
import userService from '@/service/user.service';
import { useDropzone } from 'react-dropzone';
import AvatarEditor from 'react-avatar-editor';
import base64toFile from '@/functions/base64toFile';

export default function ChangeProfileBg() {
  const EditorBgRef = useRef(null);
  const [selectedBgPhoto, setSelectedBgPhoto] = useState<any>('');

  async function changeBg() {
    setSelectedBgPhoto(null);
    const canvas = EditorBgRef.current.getImageScaledToCanvas();
    const image = canvas.toDataURL();
    console.log(image);
    userService.setBgPhoto(base64toFile(image, 'bg.png'));
  }

  const {
    acceptedFiles: acceptedBgFiles,
    getRootProps: getRootBgProps,
    getInputProps: getInputBgProps,
  } = useDropzone({
    accept: 'image/*',
    onDrop: (acceptedFiles) => {
      setSelectedBgPhoto(acceptedFiles[0]);
    },
  });

  return (
    <AlertDialog>
          <AlertDialogTrigger
            className={`${styles.profile__top_bg_trigger} ${styles.profile__top_change}`}
          >
            <ChangePhoto />
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle></AlertDialogTitle>
              <AlertDialogDescription>
                {!selectedBgPhoto && (
                  <div
                    {...getRootBgProps({ className: 'dropzone' })}
                    className={styles.dropzone}
                  >
                    <input {...getInputBgProps()} />
                    <p className={styles.dropzone__text}>
                      Перетащите cюда сюда или нажмите, чтобы выбрать файлы
                    </p>
                  </div>
                )}
                {selectedBgPhoto && (
                  <AvatarEditor
                    ref={EditorBgRef}
                    width={1080}
                    height={250}
                    border={50}
                    scale={1.2}
                    className={styles.edit}
                    image={selectedBgPhoto}
                  />
                )}
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel
                onClick={() => {
                  setSelectedBgPhoto(null);
                }}
              >
                Отмена
              </AlertDialogCancel>
              <AlertDialogAction onClick={() => changeBg()}>
                Выберите изображение
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
  )
}
